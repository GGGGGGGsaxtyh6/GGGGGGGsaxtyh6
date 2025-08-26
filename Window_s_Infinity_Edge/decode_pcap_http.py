#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

PCAP_STRINGS_PATH = Path(__file__).with_name("pcap.strings")
ASPX_PATH = Path(__file__).with_name("shell_uploaded.aspx")

HTTP_OK_RE = re.compile(r"^HTTP/1\.1 200 OK\b")
CONTENT_LENGTH_RE = re.compile(r"^Content-Length:\s*(\d+)\s*$", re.IGNORECASE)
B64_LINE_RE = re.compile(r"^[A-Za-z0-9+/=]+$")


def extract_key_iv_from_aspx(aspx_text: str) -> tuple[str, str]:
	# Key is hex string from: string p = "..." possibly multi-line
	m = re.search(r"string\s+p\s*=\s*\"([0-9a-fA-F\s\n\r]+)\";", aspx_text, re.MULTILINE)
	if not m:
		raise RuntimeError("No se pudo extraer la clave hex del ASPX")
	keyhex = re.sub(r"\s+", "", m.group(1))
	# IV is ASCII 'infinity_edgehtb'
	iv_ascii = "infinity_edgehtb"
	ivhex = iv_ascii.encode().hex()
	return keyhex, ivhex


def openssl_aes256cbc_decrypt_b64(b64_data: str, keyhex: str, ivhex: str) -> bytes | None:
	try:
		p = subprocess.run(
			[
				"openssl",
				"enc",
				"-aes-256-cbc",
				"-d",
				"-K",
				keyhex,
				"-iv",
				ivhex,
				"-a",
			],
			input=b64_data.encode(),
			stdout=subprocess.PIPE,
			stderr=subprocess.DEVNULL,
			check=False,
		)
		if p.returncode == 0 and p.stdout:
			return p.stdout
		return None
	except FileNotFoundError:
		raise RuntimeError("openssl no está disponible en el sistema")


def main() -> None:
	if not PCAP_STRINGS_PATH.exists():
		raise SystemExit(f"No existe {PCAP_STRINGS_PATH}. Genere primero con: strings -n 5 <pcap> > pcap.strings")
	aspx_text = ASPX_PATH.read_text(encoding="utf-8", errors="ignore")
	keyhex, ivhex = extract_key_iv_from_aspx(aspx_text)

	results: list[tuple[int, int, str, bytes]] = []  # (line_idx, content_len, b64, plaintext)
	with PCAP_STRINGS_PATH.open("r", encoding="utf-8", errors="ignore") as f:
		in_resp = False
		capturing = False
		need_len = 0
		cur_b64_parts: list[str] = []
		line_idx = 0
		start_line_for_resp = 0
		for raw_line in f:
			line_idx += 1
			line = raw_line.rstrip("\r\n")
			if HTTP_OK_RE.match(line):
				in_resp = True
				capturing = False
				need_len = 0
				cur_b64_parts.clear()
				start_line_for_resp = line_idx
				continue
			if line.startswith("HTTP/") and not HTTP_OK_RE.match(line):
				in_resp = False
				capturing = False
				need_len = 0
				cur_b64_parts.clear()
				continue
			if not in_resp:
				continue
			m = CONTENT_LENGTH_RE.match(line)
			if m:
				need_len = int(m.group(1))
				capturing = True
				cur_b64_parts.clear()
				continue
			if capturing:
				if B64_LINE_RE.match(line) and ":" not in line:
					cur_b64_parts.append(line.strip())
					total_len = sum(len(x) for x in cur_b64_parts)
					# If we reached at least the declared length, try with exactly 'need_len' chars
					if total_len >= need_len > 0:
						joined = "".join(cur_b64_parts)
						b64_exact = joined[:need_len]
						pt = openssl_aes256cbc_decrypt_b64(b64_exact, keyhex, ivhex)
						if pt is not None:
							results.append((start_line_for_resp, need_len, b64_exact, pt))
						capturing = False
						need_len = 0
						cur_b64_parts.clear()
						continue
				else:
					# Non-base64 line ends capture attempt
					capturing = False
					need_len = 0
					cur_b64_parts.clear()

	# Output results
	out_path = Path(__file__).with_name("decoded_http.txt")
	with out_path.open("wb") as out:
		for (idx, clen, b64s, pt) in results:
			out.write(f"==== resp_at_line={idx} len={clen}\n".encode())
			out.write(pt)
			if not pt.endswith(b"\n"):
				out.write(b"\n")
			out.write(b"----\n")

	# Also print lines containing HTB or flag patterns
	lower = b"\n".join(pt for (_, _, _, pt) in results).lower()
	for marker in [b"htb{", b"flag", b"ctf{"]:
		if marker in lower:
			print(f"[+] Encontrado marcador: {marker.decode(errors='ignore')}")
	print(str(out_path))


if __name__ == "__main__":
	main()
NSA Backdoor — picoCTF (Crypto)

Solución breve

- Descarga de artefactos:
  - gen.py, output.txt
- Observación: gen.py genera p, q tales que p−1 y q−1 son muy suaves (smooth). Se cifra FLAG como c = 3^m mod n con n = p·q.
- Enfoque: factorizar n con Pollard p−1; calcular logs discretos mod p y mod q con Pohlig–Hellman; combinar con CRT; decodificar ASCII.

Comandos clave

```bash
cd /workspace/ctf/picoctf/nsa_backdoor
python3 solve.py
```

Salida (flag)

```text
picoCTF{b3w4r3_0f_c0mp0s1t3_m0dul1_99f38837}
```

Notas técnicas

- Pollard p−1: incrementa B y cambia bases; hace gcd tras cada potencia prima para evitar el caso degenerado.
- Pohlig–Hellman: factoriza p−1 y q−1 por división de prueba; reduce a BSGS en subgrupos; restringe factores al orden real de 3 en cada campo; CRT para recomponer el exponente global.


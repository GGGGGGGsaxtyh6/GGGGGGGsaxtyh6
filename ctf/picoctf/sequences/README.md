Sequences — picoCTF (Crypto)

Resumen

- Recurrencia: m(i) = 55692·m(i-4) - 9549·m(i-3) + 301·m(i-2) + 21·m(i-1)
- ITERS = 2e7. Se requiere acelerar: exposición de matriz (4x4) y exponenciación binaria mod 10**10000.
- Se valida por MD5 y se usa SHA-256 del string para XOR del flag.

Uso

```bash
cd /workspace/ctf/picoctf/sequences
python3 solve_sequences.py
```

Flag

```text
picoCTF{b1g_numb3rs_3956e6c2}
```

Detalles técnicos

- Matriz compañera M para estado S(k) = [m(k), m(k-1), m(k-2), m(k-3)] y S(k+1)=M·S(k).
- Potenciación de matrices por exponenciación binaria O(4^3 log n).
- Cálculo mod 10**10000 para mantener congruencia con verificación.
- Ajuste de sys.set_int_max_str_digits para formar el string de m(ITERS) de forma segura.


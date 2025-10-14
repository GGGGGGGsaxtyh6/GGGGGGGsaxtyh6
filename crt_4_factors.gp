\\ Combinar solo los primeros 4 factores

moduli = [10124460123717732576, 12017858281002457600, 15013023439701145678, 17297082179958074002];

solutions = [3223629359291819296, 1228725530983745536, 6290194781419687575, 10304742720644704896];

print("Aplicando CRT con los primeros 4 factores...");

result = chinese(Mod(solutions[1], moduli[1]), Mod(solutions[2], moduli[2]));
print("Paso 1 (factores 1 y 2): ", result);

result = chinese(result, Mod(solutions[3], moduli[3]));
print("Paso 2 (+ factor 3): ", result);

result = chinese(result, Mod(solutions[4], moduli[4]));
print("Paso 3 (+ factor 4): ", result);

print("\nResultado final: ", lift(result));
print("Módulo: ", component(result, 2));

quit;

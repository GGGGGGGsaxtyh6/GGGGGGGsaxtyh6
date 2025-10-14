\\ Combinar soluciones usando CRT de PARI/GP

moduli = [10124460123717732576, 12017858281002457600, 15013023439701145678, 17297082179958074002, 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557982];

solutions = [3223629359291819296, 1228725530983745536, 6290194781419687575, 10304742720644704896, 3211601144168823063660325182627965063424375272749939797167821710437699545321512246244144924085204163005433281006573494394324809673180362031805359920118];

print("Aplicando CRT chino...");

\\ chinese() combina congruencias incluso con módulos no coprimos
result = chinese(Mod(solutions[1], moduli[1]), Mod(solutions[2], moduli[2]));
print("Paso 1 (factores 1 y 2): ", result);

result = chinese(result, Mod(solutions[3], moduli[3]));
print("Paso 2 (+ factor 3): ", result);

result = chinese(result, Mod(solutions[4], moduli[4]));
print("Paso 3 (+ factor 4): ", result);

result = chinese(result, Mod(solutions[5], moduli[5]));
print("Paso 4 (+ factor 5): ", result);

print("Resultado final: ", lift(result));
print("Módulo: ", component(result, 2));

quit;

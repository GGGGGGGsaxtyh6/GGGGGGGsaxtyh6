// Intentar ejecutar solo la última parte del código JSFuck que debería devolver algo útil
// El código termina con [!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([][[]]+[])[!+[]+!+[]])
// Esto parece estar construyendo un número seguido de algo más

// Evaluar expresiones JSFuck básicas
console.log("Testing JSFuck decoding:");
console.log("[!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]] =", [!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]);
console.log("([][[]]+[]) =", ([][[]]+[]));
console.log("([][[]]+[])[!+[]+!+[]] =", ([][[]]+[])[!+[]+!+[]]);

// Evaluar la última parte
const lastPart = [!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]+([][[]]+[])[!+[]+!+[]];
console.log("Last part:", lastPart);

// Probar decodificar algunas partes más
console.log("\n(![]+[]) =", (![]+[]));
console.log("(!![]+[]) =", (!![]+[]));
console.log("(+[![]]) =", (+[![]]));
console.log("([]+[]) =", ([]+[]));

// Intentar obtener "constructor"
console.log("\nGetting 'constructor':");
const constructor_word = [][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]];
console.log("Result:", constructor_word);

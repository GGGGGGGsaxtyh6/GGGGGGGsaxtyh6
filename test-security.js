// SCRIPT DE PRUEBAS DE SEGURIDAD
// Verifica que el servicio reforzado bloquea los ataques

import fetch from 'node-fetch'

const SECURE_API = 'http://localhost:3001/transform'

console.log("╔════════════════════════════════════════════════════════════╗")
console.log("║  PRUEBAS DE SEGURIDAD - SERVICIO REFORZADO               ║")
console.log("╚════════════════════════════════════════════════════════════╝\n")

let passedTests = 0
let failedTests = 0

async function test(name, payload, shouldBlock = true) {
  try {
    const response = await fetch(SECURE_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    const result = await response.json()
    
    if (shouldBlock) {
      if (response.status >= 400) {
        console.log(`✓ BLOQUEADO: ${name}`)
        console.log(`  Estado: ${response.status}`)
        console.log(`  Razón: ${result.message}\n`)
        passedTests++
      } else {
        console.log(`✗ FALLÓ: ${name}`)
        console.log(`  ⚠️  El ataque NO fue bloqueado\n`)
        failedTests++
      }
    } else {
      if (response.status === 200 && result.success) {
        console.log(`✓ PERMITIDO: ${name}`)
        console.log(`  Resultado: ${JSON.stringify(result.result)}\n`)
        passedTests++
      } else {
        console.log(`✗ FALLÓ: ${name}`)
        console.log(`  ⚠️  La expresión legítima fue bloqueada incorrectamente\n`)
        failedTests++
      }
    }
  } catch (error) {
    console.log(`✗ ERROR: ${name}`)
    console.log(`  ${error.message}\n`)
    failedTests++
  }
}

async function runTests() {
  console.log("⚠️  Asegúrate de que el servicio reforzado esté corriendo")
  console.log("   (ejecuta: npm run secure)\n")
  
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  console.log("═══════════════════════════════════════════════════════════")
  console.log("PRUEBAS DE ATAQUES (deben ser bloqueados)")
  console.log("═══════════════════════════════════════════════════════════\n")
  
  // Test 1: Prototype Pollution
  await test(
    "Prototype Pollution",
    {
      expression: "$.__proto__.polluted := 'evil'",
      input: {}
    },
    true
  )
  
  // Test 2: Constructor access
  await test(
    "Acceso a Constructor",
    {
      expression: "$constructor := $.__proto__.constructor",
      input: {}
    },
    true
  )
  
  // Test 3: Process access
  await test(
    "Acceso a Process",
    {
      expression: "process.env",
      input: {}
    },
    true
  )
  
  // Test 4: Global context
  await test(
    "Acceso a Contexto Global",
    {
      expression: "$$.env",
      input: {}
    },
    true
  )
  
  // Test 5: Function constructor
  await test(
    "Function Constructor",
    {
      expression: "Function('return process')().env",
      input: {}
    },
    true
  )
  
  // Test 6: Expresión muy larga (DoS)
  await test(
    "Expresión Excesivamente Larga",
    {
      expression: "a".repeat(2000),
      input: {}
    },
    true
  )
  
  // Test 7: Entrada con __proto__
  await test(
    "Entrada con __proto__",
    {
      expression: "data.value",
      input: { "__proto__": { polluted: true }, value: 42 }
    },
    true
  )
  
  console.log("═══════════════════════════════════════════════════════════")
  console.log("PRUEBAS DE EXPRESIONES LEGÍTIMAS (deben ser permitidas)")
  console.log("═══════════════════════════════════════════════════════════\n")
  
  // Test 8: Mapeo simple
  await test(
    "Mapeo Simple",
    {
      expression: "users.name",
      input: { users: [{ name: "Juan" }, { name: "María" }] }
    },
    false
  )
  
  // Test 9: Filtrado
  await test(
    "Filtrado",
    {
      expression: "products[price < 100]",
      input: { products: [{ name: "A", price: 50 }, { name: "B", price: 150 }] }
    },
    false
  )
  
  // Test 10: Suma
  await test(
    "Agregación con $sum",
    {
      expression: "$sum(numbers)",
      input: { numbers: [1, 2, 3, 4, 5] }
    },
    false
  )
  
  // Test 11: Transformación compleja
  await test(
    "Transformación de Objeto",
    {
      expression: "{ 'total': $sum(items.price), 'count': $count(items) }",
      input: { items: [{ price: 10 }, { price: 20 }, { price: 30 }] }
    },
    false
  )
  
  console.log("═══════════════════════════════════════════════════════════")
  console.log("RESULTADOS FINALES")
  console.log("═══════════════════════════════════════════════════════════")
  console.log(`✓ Pruebas exitosas: ${passedTests}`)
  console.log(`✗ Pruebas fallidas: ${failedTests}`)
  console.log(`  Total: ${passedTests + failedTests}`)
  
  if (failedTests === 0) {
    console.log("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    console.log("   El servicio está correctamente reforzado.\n")
  } else {
    console.log("\n⚠️  Algunas pruebas fallaron.")
    console.log("   Revisa la configuración de seguridad.\n")
  }
}

runTests().catch(console.error)

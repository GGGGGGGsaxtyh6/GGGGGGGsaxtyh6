// SERVICIO VULNERABLE - NO USAR EN PRODUCCIÓN
// Este código demuestra CVE-2024-27307 y vulnerabilidades de inyección JSONata

import express from "express"
import jsonata from "jsonata"

const app = express()
app.use(express.json())

// ⚠️ VULNERABILIDAD CRÍTICA: Evaluación directa de expresiones no confiables
app.post("/transform", async (req, res) => {
  try {
    const { expression, input } = req.body
    
    // Sin validación ni sanitización - acepta cualquier expresión JSONata
    const result = await jsonata(expression).evaluate(input)
    
    res.json({ result })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.listen(3000, () => {
  console.log("⚠️  SERVICIO VULNERABLE corriendo en puerto 3000")
  console.log("⚠️  NO USAR EN PRODUCCIÓN")
})

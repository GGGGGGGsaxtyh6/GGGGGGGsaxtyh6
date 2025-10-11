const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Intentar obtener directamente lo que valida el formulario  
  const details = await page.evaluate(() => {
    // En lugar de ejecutar el formulario, interceptar la función antes que se ejecute
    // y analizar su código fuente para buscar patrones
    
    const form = document.getElementById('login');
    const onsubmitString = form.onsubmit.toString();
    
    // Intentar encontrar cualquier string que parezca username o password
    // Buscar patrones comunes en el código
    
    // También intentar ejecutar partes del código de manera segura
    try {
      // El código JSFuck al final parece generar alguna cadena como "7d"
      // Intentemos ejecutar solo esa parte
      const result = ([][[]]+[])[!+[]+!+[]];
      
      return {
        codeLength: onsubmitString.length,
        lastPart: result,
        // Intentar ejecutar el constructor que genera
        attempt: 'Analyzing...'
      };
    } catch(e) {
      return { error: e.toString() };
    }
  });
  
  console.log(JSON.stringify(details, null, 2));
  
  // Ahora intentar ejecutar la validación con diferentes combinaciones
  // para ver si podemos obtener alguna pista basándonos en el comportamiento
  
  await browser.close();
})();

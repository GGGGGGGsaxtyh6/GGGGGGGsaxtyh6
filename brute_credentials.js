const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // El código ofuscado probablemente compara el username y password con valores hardcodeados
  // Vamos a intentar obtener esos valores interceptando la comparación
  
  const result = await page.evaluate(() => {
    // Sobrescribir los inputs para poder interceptar las comparaciones
    const originalValue = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
    let capturedValues = [];
    
    // Intentar ejecutar la función onsubmit y capturar lo que compara
    try {
      const form = document.getElementById('login');
      const username = document.getElementById('username');
      const password = document.getElementById('password');
      
      // Set dummy values
      username.value = 'test_user';
      password.value = 'test_pass';
      
      // Intentar obtener información del código antes de ejecutarlo
      // La función onsubmit debe tener alguna lógica de validación
      
      // Ejecutar y capturar errores que puedan revelar info
      try {
        form.onsubmit();
      } catch(e) {
        return {
          error: e.message,
          stack: e.stack,
          hint: 'Error during execution'
        };
      }
      
      return { status: 'No error, returned false' };
      
    } catch(e) {
      return { error: e.toString() };
    }
  });
  
  console.log(JSON.stringify(result, null, 2));
  
  await browser.close();
})();

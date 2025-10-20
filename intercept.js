const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Intercept console logs
  page.on('console', msg => {
    console.log('BROWSER LOG:', msg.text());
  });
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Intentemos enviar el formulario con valores de prueba y capturar qué hace
  const testResult = await page.evaluate(() => {
    // Intentar obtener lo que el código ofuscado genera
    try {
      const form = document.getElementById('login');
      const username = document.getElementById('username');
      const password = document.getElementById('password');
      
      // Establecer valores de prueba
      username.value = 'test';
      password.value = 'test';
      
      // Capturar la función antes de ejecutarla
      const onsubmitCode = form.onsubmit.toString();
      
      return {
        success: true,
        onsubmitCode: onsubmitCode
      };
    } catch(e) {
      return {
        success: false,
        error: e.toString()
      };
    }
  });
  
  console.log(JSON.stringify(testResult, null, 2));
  
  await browser.close();
})();

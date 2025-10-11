const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  //Intercept network requests to see what happens
  page.on('request', request => {
    console.log('REQUEST:', request.url(), request.method());
  });
  
  page.on('response', response => {
    console.log('RESPONSE:', response.url(), response.status());
  });
  
  // Intercept console logs
  page.on('console', msg => {
    console.log('CONSOLE:', msg.text());
  });
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Test with various username/password combinations
  const result = await page.evaluate(() => {
    // Try to extract the validation logic
    const form = document.getElementById('login');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    
    // Set test values
    username.value = 'admin';
    password.value = 'admin123';
    
    // Try to trigger the form submission and catch any errors
    try {
      // Call the onsubmit function directly
      const result = form.onsubmit();
      return { success: true, result: result };
    } catch(e) {
      return { success: false, error: e.toString(), message: e.message };
    }
  });
  
  console.log('RESULT:', JSON.stringify(result, null, 2));
  
  await browser.close();
})();

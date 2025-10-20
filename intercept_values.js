const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Intercept console
  const logs = [];
  page.on('console', msg => {
    logs.push(msg.text());
    console.log('BROWSER:', msg.text());
  });
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Inject code to monitor the form submission
  const result = await page.evaluate(() => {
    try {
      // Override alert to capture the output
      const originalAlert = window.alert;
      let capturedAlert = '';
      window.alert = function(msg) {
        capturedAlert = msg;
        console.log('ALERT CAPTURED:', msg);
      };
      
      // Try to extract any hardcoded credentials or validation logic
      const form = document.getElementById('login');
      const originalOnSubmit = form.onsubmit;
      
      // Test with empty values to see what happens
      document.getElementById('username').value = '';
      document.getElementById('password').value = '';
      
      // Try to intercept the validation
      let intercepted = false;
      form.onsubmit = function() {
        try {
          // Call original and capture
          const result = originalOnSubmit.call(this);
          return result;
        } catch(e) {
          return { error: e.toString(), message: e.message };
        }
      };
      
      // Try with various test values
      const testCases = [
        ['admin', 'admin'],
        ['user', 'password'],
        ['test', 'test'],
        ['', '']
      ];
      
      let results = {};
      for (let [user, pass] of testCases) {
        document.getElementById('username').value = user;
        document.getElementById('password').value = pass;
        try {
          const r = originalOnSubmit.call(form);
          results[`${user}:${pass}`] = { success: true, result: r };
        } catch(e) {
          results[`${user}:${pass}`] = { success: false, error: e.toString() };
        }
      }
      
      return {
        success: true,
        capturedAlert,
        results
      };
    } catch(e) {
      return {
        success: false,
        error: e.toString(),
        message: e.message,
        stack: e.stack
      };
    }
  });
  
  console.log('\n=== RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  
  console.log('\n=== LOGS ===');
  logs.forEach(log => console.log(log));
  
  await browser.close();
})();

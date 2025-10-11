const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Patch the validation to extract credentials
  const result = await page.evaluate(() => {
    try {
      // Override the form submission to intercept comparisons
      const username = document.getElementById('username');
      const password = document.getElementById('password');
      const form = document.getElementById('login');
      
      // Monkey patch string comparison and properties
      let capturedComparisons = [];
      
      // Try to intercept property access
      const originalValue = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
      
      Object.defineProperty(username, 'value', {
        get: function() {
          const val = originalValue.get.call(this);
          console.log('[USERNAME.VALUE GET]:', val);
          return val;
        },
        set: function(val) {
          console.log('[USERNAME.VALUE SET]:', val);
          originalValue.set.call(this, val);
        }
      });
      
      Object.defineProperty(password, 'value', {
        get: function() {
          const val = originalValue.get.call(this);
          console.log('[PASSWORD.VALUE GET]:', val);
          return val;
        },
        set: function(val) {
          console.log('[PASSWORD.VALUE SET]:', val);
          originalValue.set.call(this, val);
        }
      });
      
      // Test with dummy values
      username.value = 'test123';
      password.value = 'pass456';
      
      // Trigger the onsubmit
      form.onsubmit();
      
      return { success: true };
    } catch(e) {
      return { success: false, error: e.toString(), stack: e.stack };
    }
  });
  
  console.log(JSON.stringify(result, null, 2));
  
  await browser.close();
})();

const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  await page.goto('https://f9a8257876869370.247ctf.com/');
  
  // Try to inspect the generated code
  const result = await page.evaluate(() => {
    try {
      const form = document.getElementById('login');
      const onsubmitCode = form.onsubmit.toString();
      
      // Try to find patterns in the code
      // Look for comparisons, hardcoded values, etc.
      const lines = onsubmitCode.split('\n');
      
      // Try to extract the validation logic
      // The code might be checking this.username.value == "something"
      
      return {
        success: true,
        codeLength: onsubmitCode.length,
        firstLines: lines.slice(0, 10).join('\n'),
        lastLines: lines.slice(-10).join('\n'),
        fullCode: onsubmitCode
      };
    } catch(e) {
      return {
        success: false,
        error: e.toString()
      };
    }
  });
  
  if (result.success) {
    console.log('Code Length:', result.codeLength);
    console.log('\n=== FIRST LINES ===');
    console.log(result.firstLines);
    console.log('\n=== LAST LINES ===');
    console.log(result.lastLines);
    
    // Save full code to file
    const fs = require('fs');
    fs.writeFileSync('/workspace/validation_code.js', result.fullCode);
    console.log('\nFull code saved to validation_code.js');
  } else {
    console.log('Error:', result.error);
  }
  
  await browser.close();
})();

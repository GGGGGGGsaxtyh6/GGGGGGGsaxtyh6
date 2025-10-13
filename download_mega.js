const fs = require('fs');
const path = require('path');
const { File } = require('megajs');

async function main() {
  const [,, url, destDir] = process.argv;
  if (!url || !destDir) {
    console.error('Usage: node download_mega.js <url> <dest_dir>');
    process.exit(1);
  }
  try {
    const file = File.fromURL(url);
    await file.loadAttributes();
    const outPath = path.join(destDir, file.name);
    await new Promise((resolve, reject) => {
      const writeStream = fs.createWriteStream(outPath);
      file.download().on('error', reject).pipe(writeStream);
      writeStream.on('finish', resolve);
      writeStream.on('error', reject);
    });
    console.log(outPath);
  } catch (err) {
    console.error('Download error:', err);
    process.exit(2);
  }
}

main();

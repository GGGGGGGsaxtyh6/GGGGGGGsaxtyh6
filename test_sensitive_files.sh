#!/bin/bash
echo "[*] Testing for sensitive files..."
for file in .git/config .git/HEAD .env .env.local settings.php sites/default/settings.php backup.sql dump.sql database.sql www.tar.gz backup.tar.gz config.php wp-config.php .DS_Store phpinfo.php info.php test.php; do
  echo "Testing /$file"
  curl -s "https://www.esic.edu/$file" -I --max-time 3 | head -1
done

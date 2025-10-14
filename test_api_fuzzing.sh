#!/bin/bash
echo "[*] Fuzzing API ESIC..."

# Test different parameter names
for param in center CENTER Centre CENTRE campus Campus location Location; do
  echo "Testing parameter: $param"
  curl -s "https://api.esic.edu/?$param=madrid" --max-time 3 | head -3
  echo ""
done

# Test parameter in different positions
echo "Testing Center in body (form-data):"
curl -s -X POST "https://api.esic.edu/" -d "Center=madrid" --max-time 3 | head -3
echo ""

echo "Testing Center as header:"
curl -s "https://api.esic.edu/" -H "Center: madrid" --max-time 3 | head -3
echo ""

echo "Testing with XML:"
curl -s -X POST "https://api.esic.edu/" -H "Content-Type: application/xml" -d '<request><Center>madrid</Center></request>' --max-time 3 | head -3
echo ""

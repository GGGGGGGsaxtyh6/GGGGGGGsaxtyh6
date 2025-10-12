#!/bin/bash
# Script para analizar el stack en gdb

cat > /tmp/gdb_commands.txt <<'EOF'
set disable-randomization off
break vuln
run <<< "1
TESTNAME
3
FEEDBACK"
info frame
x/40gx $rbp-750
x/10gx $rbp
quit
EOF

timeout 10 gdb -batch -x /tmp/gdb_commands.txt ./handoff 2>&1

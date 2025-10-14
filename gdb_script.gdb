set pagination off
set confirm off
break *main
run
# Saltar las llamadas a a1() y a2()
set $rip = 0x555555555000 + 0x127d
# Establecer index1 a un valor arbitrario
set *(long*)0x5555555583f8 = 1
continue
quit

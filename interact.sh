#!/bin/bash
(
echo "My_Passw@rd_@1234"
sleep 1
echo "DEFCON"
sleep 1
echo "John Draper"
sleep 1
echo "sudo -l"
sleep 3
) | nc tethys.picoctf.net 59853

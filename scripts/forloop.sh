#!/bin/sh

while true
do
  echo "`hostname`: `date`" >> /var/hehe.txt
  echo "`hostname`: `date`" >> /home/hehe.txt
  sleep 5
  ls -l /home/hehe.txt
done

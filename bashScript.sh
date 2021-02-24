#!/bin/bash

runtime="15 minute"
endtime=$(date -ud "$runtime" +%s)

iterator=1
while [[ $(date -u +%s) -le $endtime ]]
do 	
	sleep 1m
	name="checkpoint${iterator}"
	docker checkpoint create  --leave-running=true cr $name
	iterator++
	
done
#!/bin/bash
cd /app
#echo INVERTER_IP $INVERTER_IP
#echo INVERTER_PORT $INVERTER_PORT
#echo IDM_IP $IDM_IP
#echo IDM_PORT $IDM_PORT
#echo FEED_IN_LIMIT $FEED_IN_LIMIT
python3 kostal_idm.py

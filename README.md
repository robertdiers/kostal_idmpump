# kostal_idmpump
send feed-in value from Kostal Plenticore to iDM heat pump

# kostal_idmpump
using TCP Modbus to send fed-in energy from Kostal Plenticore 10 to iDM AERO SLM 6-17
(iDM Option "TCP Modbus" or "Gebäudeleittechnik/Smartfox" in German Version)

### Linux usage (you might want to use directly with cron)
i
adjust IPs in kostal_idm.py file

```python3 kostal_idm.py```

### Docker usage
adjust IPs in kostal_idm.py file

adjust execution in kostal_idm_cron file

```sudo docker build -f Dockerfile -t kostal_idm:1.0 .```

```sudo docker run -d --name kostal_idm --restart=always kostal_idm:1.0```

```sudo docker logs kostal_idm```

```sudo docker rm -f kostal_idm```


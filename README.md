# kostal_idmpump
using TCP Modbus to send fed-in energy from Kostal Plenticore 10 to iDM AERO SLM 6-17
(iDM Option "TCP Modbus" or "Gebaedeleittechnik/Smartfox" in German Version)

### Defaults
plaese check IPs in kostal_idm.ini file, could be overridden by Docker env variables

Graphite usage is optional (metrics)

### Docker usage
https://hub.docker.com/repository/docker/robertdiers/kostalidm

### Development
Please start Visual Studio Code Server using script vsc_start.sh, open http://localhost:8080 to code.

### Blog
https://robertdiers.medium.com/solar-energy-sending-feed-in-energy-amount-from-kostal-inverter-to-idm-heat-pump-using-tcp-modbus-d406ba1202c8

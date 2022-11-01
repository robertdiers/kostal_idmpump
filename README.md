# kostal_idmpump
using TCP Modbus to send fed-in energy from Kostal Plenticore 10 to iDM AERO SLM 6-17
(iDM Option "TCP Modbus" or "Gebaedeleittechnik/Smartfox" in German Version)

### Defaults
plaese check IPs in kostal_idm.ini file, could be overridden by Docker env variables

### Docker usage
https://hub.docker.com/repository/docker/robertdiers/kostalidm

### create Docker image for your architecture
./image.sh

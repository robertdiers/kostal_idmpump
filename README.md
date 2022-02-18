# kostal_idmpump
using TCP Modbus to send fed-in energy from Kostal Plenticore 10 to iDM AERO SLM 6-17
(iDM Option "TCP Modbus" or "Gebaedeleittechnik/Smartfox" in German Version)

### Defaults
plaese check IPs in kostal_idm.ini file, could be overridden by Docker env variables

TimescaleDB usage is optional (metrics)

### Docker usage
https://hub.docker.com/repository/docker/robertdiers/kostalidm

### Development
Please start Visual Studio Code Server using script vsc_start.sh, open http://localhost:8080 to code.

### Blog
https://robertdiers.medium.com/solar-energy-sending-feed-in-energy-amount-from-kostal-inverter-to-idm-heat-pump-using-tcp-modbus-d406ba1202c8

### TimescaleDB
CREATE  TABLE solar_kostal_battery ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_battery', 'time');

ALTER TABLE solar_kostal_battery SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_battery', INTERVAL '1 days');

CREATE  TABLE solar_kostal_batterypercent ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_batterypercent', 'time');

ALTER TABLE solar_kostal_batterypercent SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_batterypercent', INTERVAL '1 days');

CREATE  TABLE solar_kostal_batteryflag ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_batteryflag', 'time');

ALTER TABLE solar_kostal_batteryflag SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_batteryflag', INTERVAL '1 days');

CREATE  TABLE solar_kostal_inverter ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_inverter', 'time');

ALTER TABLE solar_kostal_inverter SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_inverter', INTERVAL '1 days');

CREATE  TABLE solar_kostal_powertogrid ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_powertogrid', 'time');

ALTER TABLE solar_kostal_powertogrid SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_powertogrid', INTERVAL '1 days');

CREATE  TABLE solar_idm_feedin ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );
 
SELECT create_hypertable('solar_idm_feedin', 'time');

ALTER TABLE solar_idm_feedin SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_idm_feedin', INTERVAL '1 days');

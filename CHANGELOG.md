# Changelog

## v0.1.21

- [BREAKING CHANGE]: Rename `sensor.ims_rain` sensor to `sensor.ims_is_raining`
- Add Precipitation and Precipitation Chance sensors
- Fix _deprecated constant_ usage and log warning
- Code styling according to standards
- Fix gaps in hourly missing data in daily sensors
- In ConfigFlow - select which sensors to create

## v0.1.20

_Minimum HA Version: 2024.1.0b0_


#### Adjust code to HA 2024.1.0:

- Fix usage of Constants according to deprecation
- Fix Metaclass error, failing to create ImsSensor
  
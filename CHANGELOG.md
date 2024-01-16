# Changelog

## v0.1.21

- [BREAKING CHANGE]: Rename `sensor.ims_rain` sensor to `sensor.ims_is_raining`
- Add Precipitation and Precipitation Chance sensors
- Fix _deprecated constant_ usage and log warning

## v0.1.20

_Minimum HA Version: 2024.1.0b0_


#### Adjust code to HA 2024.1.0:

- Fix usage of Constants according to deprecation
- Fix Metaclass error, failing to create ImsSensor
  
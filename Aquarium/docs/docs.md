# Notes

This document will specify all the components of the Acuatech fish tank.

## Sensors

- `DHT11` Ambient temperature and humidity
- `NTC3950` Water-proof thermoresistor to measure temperature inside the fish tank
- `WS-9525` Water level sensor
- `SKU_SEN0189` DFRobot sensor for measuring water turbidity

## Actuators

- `NeoPixel_THT` NeoPixel shield by Adafruit that controls ambience lights
- `4 Relay Module` Module of 4 relays that work on 3.3V, they control the water filter, thermostat and ligths that operate on higher voltage currents

## Power Source

- `LD1117V33` 3.3V voltage regulator to accomodate the ESP32's output voltage
- `Battery` 5V battery to power the ESP32

## Database

This project makes use of InfluxDB to store all of the sensors' readings, these are linked to each user's account and keep track of insertion time by default

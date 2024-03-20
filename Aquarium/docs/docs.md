# Notes

The Acuatech fish tank is powered by the Espressif System's ESP32 Dev Board, this board is powered from its micro USB port and it powers all of the components, it then communicates with our servers via InfluxDB and MQTT.

## Components

The following table shows all the components that are connected to the board

| Tag        | Component   | Description                                 | Pin |
| ---------- | ----------- | ------------------------------------------- | --- |
| WTEMP      | NTC3950     | Waterproof thermistor for water temperature | A4  |
| TURBIDITY  | SKU_SEN0189 | Water turbidity sensor                      | A6  |
| WLEVEL     | WS-9525     | Water height sensor                         | A7  |
| THERMOSTAT | THERMOSTAT  | Water temperature controller                | 4   |
| FILTERS    | FILTERS     | Controllable water filters                  | 5   |
| DHTPIN     | DHT11       | Relative temperature and humidity sensor    | 13  |
| SERVO      | SG90        | A PWM servo-motor for controlled angles     | 14  |
| LIGHTS     | LIGHTS      | Controllable light bulbs                    | 15  |
| NEOLIGHT2  | WS2812      | Configurable colored light strip of 24 LEDs | 18  |
| NEOLIGHT1  | WS2812      | Configurable colored light strip of 12 LEDs | 19  |

## Storage

This project makes use of an InfluxDB server to store all of the sensors' readings, these are linked to each user's account and keep track of insertion time by default.

The system also makes use of the board's EEPROM, a Flash memory that keeps data persistant used for storing the aquarium's configuration parameters like Wi-Fi credentials, automatic feeding times, etc.

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

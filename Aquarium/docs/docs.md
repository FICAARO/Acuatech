# Acuatech's IoT Aquarium

The Acuatech fish tank is powered by the Espressif System's ESP32 Dev Board, this board is powered from a 5V battery that also powers all of its components, it then communicates with our servers via HTTP.

## Components

The following table shows all the components that are connected to the board

| Tag        | Component  | Description                                 | Pin | Type        |
| ---------- | ---------- | ------------------------------------------- | --- | ----------- |
| WTEMP      | DS18B20    | Waterproof thermistor for water temperature | A4  | Digital Bi  |
| TURBIDITY  | SEN0189    | Water turbidity sensor                      | A6  | Analog In   |
| WLEVEL     | WS-9525    | Water height sensor                         | A7  | Analog In   |
| BOOT       | BUTTON     | Button to start the config web server       | 0   | Digital In  |
| LIGHTS     | LIGHTS     | Controllable light bulbs                    | 2   | Digital Out |
| THERMOSTAT | THERMOSTAT | Water temperature controller                | 4   | Digital Out |
| FILTERS    | FILTERS    | Controllable water filters                  | 5   | Digital Out |
| DHTPIN     | DHT11      | Relative temperature and humidity sensor    | 13  | Digital Bi  |
| SERVO      | SG90       | A PWM servo-motor for controlled angles     | 15  | PWM Out     |
| NEOLIGHT2  | WS2812     | Configurable colored light strip of 24 LEDs | 18  | Digital Out |
| NEOLIGHT1  | WS2812     | Configurable colored light strip of 12 LEDs | 19  | Digital Out |

## Storage

The system also use of the board's EEPROM, a Flash memory that keeps vital information such as Wi-Fi credentials and Acuatech user tokens always at hand, the board then uses this information to communicate with our databases.

## Database

This project makes use of InfluxDB to store all of the sensors' readings, these are linked to each user's account and keep track of insertion time by default, the configuration of a user's aquarium is stored in Django's SQLite database

## Sensors

- `DHT11` Ambient temperature and humidity
- `DS18B20` Water-proof thermoresistor to measure temperature inside the fish tank
- `WS-9525` Water level sensor
- `SEN0189` DFRobot sensor for measuring water turbidity

## Actuators

- `WS2812` NeoPixel shield by Adafruit that controls ambience lights
- `SG90` PWM Servo-Motor that controls the automatic feeder
- `4 Relay Module` Module of 4 relays that work on 3.3V, they control the water filter, thermostat and ligths that operate on higher voltage currents

## Power Source

- `Battery` 5V battery to power the ESP32

// Libraries CM4
#include <WiFi.h>
#include <DHT.h>                // "DHT sensor library" by "Adafruit": v1.4.6
#include <DallasTemperature.h>  // "DallasTemperature" by "Miles Burton": v3.9.0
#include <InfluxDbClient.h>     // "ESP8266 Influxdb" by "Tobias Schürg" v3.13.1
#include <InfluxDbCloud.h>
#include "DhtSensor.h"
#include "DallasSensor.h"
#include "GenericSensor.h"
#include "Influx.h"
#include "Secrets.h"

// Pin I/O
#define BOOT 0        // Built-in boot button
#define THERMOSTAT 4  // Thermostat actuator (D4)
#define FILTERS 5     // Filters actuator (D5)
#define DHTPIN 13     // DHT11 sensor (D13)
#define LIGHTS 16     // Lights actuator (D16)
#define WTEMP 32      // Water temperature sensor (A4)
#define TURBIDITY 34  // Turbidity sensor (A6)
#define WLEVEL 35     // Water level sensor (A7)
#define NEOLIGHT1 19  // Neopixel strip 1 (D19)
#define NEOLIGHT2 18  // Neopixel strip 2 (D18)

// Constants
#define WIFI_TIMEOUT 10000      // Limit time on WiFi disconnection
#define FLUX_SEND_TIMEOUT 5000  // Interval time for sending data to database
#define READ_TIMEOUT 2000       // Interval time for reading all the sensors

#define DHTTYPE DHT11     // Type of the DHT sensor
#define TURB_ANALOG true  // Whether the turbidity sensor is ADC
#define PIXELS1 12        // Amount of pixels in Neopixel strip 1
#define PIXELS2 24        // Amount of pixels in Neopixel strip 2

// Variables
bool wifiConnected = false;
bool disconnectWarn = false;
DhtSensor dht(DHTPIN, DHTTYPE);
DallasSensor dallas(WTEMP);
GenericSensor wlevel(WLEVEL, true);
GenericSensor turbidity(TURBIDITY, TURB_ANALOG);
Influx influx(FLUX_URL, FLUX_ORG, FLUX_BUCKET, FLUX_TOKEN, InfluxDbCloud2CACert, "test");

// Time variables
unsigned long currTime = 0;          // Current relative time of the program
unsigned long lastConnected = 0;     // Last relative time with WiFi connection
unsigned long lastReconnection = 0;  // Last relative time attepting reconnection
unsigned long lastRead = 0;          // Last relative time reading sensors
unsigned long lastDataSend = 0;      // Last relative time sending data

// Subroutines
float analogPercentage(int value) {
  return value * 100 / 4095;
}

void printData() {
  dht.print();
  dallas.print();
  wlevel.print("WaterLevel");
  turbidity.print("Turbidity", "%");
}

// Main routines
void setup() {
  // Pin definition
  pinMode(BOOT, INPUT);
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(LIGHTS, OUTPUT);
  pinMode(THERMOSTAT, OUTPUT);
  pinMode(FILTERS, OUTPUT);

  // Output clearing
  digitalWrite(BUILTIN_LED, LOW);
  digitalWrite(LIGHTS, LOW);
  digitalWrite(THERMOSTAT, LOW);
  digitalWrite(FILTERS, LOW);

  // Comms
  Serial.begin(115200);

  // Sensors
  dht.begin();
  dallas.begin();
  wlevel.begin();
  if (TURB_ANALOG) turbidity.begin(analogPercentage);
  else turbidity.begin();

  // WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
}

void loop() {
  currTime = millis();

  // Reconnect WiFi
  wifiConnected = WiFi.status() == WL_CONNECTED;
  if (wifiConnected) {
    if (!influx.connected) influx.connect(TZ_INFO);
    lastConnected = currTime;
  }

  // Launch AP on no WiFi or BOOT button press
  if ((currTime - lastConnected >= WIFI_TIMEOUT || !digitalRead(BOOT)) && !disconnectWarn) {
    Serial.println("Launching AP...");
    digitalWrite(BUILTIN_LED, HIGH);
    disconnectWarn = true;
    // ...Launch AP
  }

  // Update the sensor readings
  if (currTime - lastRead >= READ_TIMEOUT) {
    Serial.println("Reading sensors...");
    dht.readSensor(0b11);
    dallas.readSensor();
    wlevel.readSensor();
    turbidity.readSensor();
    lastRead = currTime;
  }

  // Communicate data to InfluxDB
  if (currTime - lastDataSend >= FLUX_SEND_TIMEOUT && wifiConnected) {
    // Read sensors
    influx.sensor.clearFields();

    influx.sensor.addField("temp", dht.temp);
    influx.sensor.addField("hum", dht.hum);
    influx.sensor.addField("wtemp", dallas.wtemp);
    influx.sensor.addField("wlevel", wlevel.value);
    influx.sensor.addField("turbp", turbidity.scaled);

    // Send data
    influx.printLineProtocol();
    influx.write();
    lastDataSend = currTime;
  }
}

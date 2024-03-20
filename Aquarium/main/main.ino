
// Libraries
#include <WiFi.h>
#include <WiFiUdp.h>
#include <EEPROM.h>
#include <DHT.h>                // "DHT sensor library" by "Adafruit" v1.4.6
#include <DallasTemperature.h>  // "DallasTemperature" by "Miles Burton" v3.9.0
#include <InfluxDbClient.h>     // "ESP8266 Influxdb" by "Tobias Schürg" v3.13.1
#include <InfluxDbCloud.h>
#include <NTPClient.h>          // "NTPClient" by "Fabrice Weinberg" v3.2.1
#include <Adafruit_NeoPixel.h>  // "Adafruit NeoPixel" by "Adafruit" v1.12.0
#include "DhtSensor.h"
#include "DallasSensor.h"
#include "GenericSensor.h"
#include "Influx.h"
#include "AccessPoint.h"
#include "NeoPixel.h"
#include "Secrets.h"

// Pin I/O
#define BOOT 0        // Built-in boot button (D0)
#define THERMOSTAT 4  // Thermostat actuator (D4)
#define FILTERS 5     // Filters actuator (D5)
#define DHTPIN 13     // DHT11 sensor (D13)
#define LIGHTS 15     // Lights actuator (D15)
#define WTEMP 32      // Water temperature sensor (A4)
#define TURBIDITY 34  // Turbidity sensor (A6)
#define WLEVEL 35     // Water level sensor (A7)
#define NEOLIGHT1 19  // Neopixel strip 1 (D19)
#define NEOLIGHT2 18  // Neopixel strip 2 (D18)

// Constants
const char* AP_SSID = "CUSTOM_SSID";      // SSID of the access point Wi-Fi network
const char* AP_PASS = "CUSTOM_PASSWORD";  // Password of the access point Wi-Fi network
#define WIFI_TIMEOUT 10000                // Limit time on WiFi disconnection

#define GMT_OFFSET -18000                 // Timezone offset compared to GMT
#define DAYLIGHT_OFFSET 0                 // Daylight savings offset
#define NTP_SERVER "pool.ntp.org"         // NTP default server
#define TIME_UPDT_TIMEOUT 1000            // Interval for reading the time

#define FLUX_URL ""             // InfluxDB URL
#define FLUX_ORG ""             // InfluxDB organization ID
#define FLUX_BUCKET ""          // InfluxDB bucket/table name
#define TZ_INFO ""              // Server timezone
#define FLUX_SEND_TIMEOUT 5000  // Interval time for sending data to database

#define DHTTYPE DHT11      // Type of the DHT sensor
#define TURB_ANALOG true   // Whether the turbidity sensor is ADC
#define READ_TIMEOUT 2000  // Interval time for reading all the sensors
#define PIXELS1 12         // Amount of pixels in Neopixel strip 1
#define PIXELS2 24         // Amount of pixels in Neopixel strip 2

uint8_t FEED_TIMES[3] = { 7, 14, 21 };
uint8_t COLOR_TIMES[5] = { 7, 10, 14, 18, 21 };  // TODO: Make configurable
uint8_t COLORS[5][8] = {
  {   0,   0,   0,   0,   0,   0,   0, 0 },
  { 255, 255, 255,   0,   0, 255,  50, 3 },
  { 255, 255, 255,   0,   0, 255, 100, 0 },
  { 255, 255, 255, 255, 212,  92,  75, 3 },
  { 255, 255, 255,   0,   0, 255,  25, 2 }
};

// Variables
String wifiSSID = "";        // SSID of the Wi-Fi network (Set by EEPROM)
String wifiPass = "";        // Password of the Wi-Fi network (Set by EEPROM)
short hours = 0;             // The real time hour number
short oldHours = 0;
uint8_t color = -1;           // The color corresponding to the current hour
uint8_t oldColor = -1;        // The color that was chosen on the previous iteration
uint8_t feed = -1;
uint8_t oldFeed = -1;
bool wifiConnected = false;  // Flag of successful Wi-Fi connection
bool timeSetup = false;      // Flag of configured time from NTP server

DhtSensor dht(DHTPIN, DHTTYPE);
DallasSensor dallas(WTEMP);
GenericSensor wlevel(WLEVEL, true);
GenericSensor turbidity(TURBIDITY, TURB_ANALOG);
Influx influx(FLUX_URL, FLUX_ORG, FLUX_BUCKET, FLUX_TOKEN, InfluxDbCloud2CACert, "test");
AccessPoint ap(AP_SSID, AP_PASS, 80);
NeoPixel pixel1(PIXELS1, NEOLIGHT1);
NeoPixel pixel2(PIXELS2, NEOLIGHT2);

// Time variables
unsigned long currTime = 0;          // Current relative time of the program
unsigned long lastConnected = 0;     // Last relative time with WiFi connection
unsigned long lastReconnection = 0;  // Last relative time attepting reconnection
unsigned long lastRead = 0;          // Last relative time reading sensors
unsigned long lastDataSend = 0;      // Last relative time sending data
unsigned long lastTimeUpdt = 0;      // Last relative time reading real time
unsigned long lastColorUpdt = 0;     // Last relative time updating NeoPixel colors
unsigned long lastFeedUpdt = 0;

// Subroutines
float analogPercentage(int value) {
  return value * 100 / 4095;
}

int getHours() {
  struct tm timeInfo;
  if (!getLocalTime(&timeInfo)) return -1;

  char hour[3];
  strftime(hour, sizeof(hour), "%S", &timeInfo);
  return String(hour).toInt();
}

int getColor(int hour) {
  if (hour < COLOR_TIMES[0]) return 0;
  else if (hour < COLOR_TIMES[1]) return 1;
  else if (hour < COLOR_TIMES[2]) return 2;
  else if (hour < COLOR_TIMES[3]) return 3;
  else if (hour < COLOR_TIMES[4]) return 4;
  else return 0;
}

int getFeed(int hour) {
  if (hour < FEED_TIMES[0]) return 0;
  else if (hour < FEED_TIMES[1]) return 1;
  else if (hour < FEED_TIMES[2]) return 2;
  else return 0;
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
  EEPROM.begin(512);

  // Sensors
  dht.begin();
  dallas.begin();
  wlevel.begin();
  if (TURB_ANALOG) turbidity.begin(analogPercentage);
  else turbidity.begin();

  // Actuators
  pixel1.begin(50);
  pixel2.begin(50);

  // Wi-Fi
  EEPROM.get(0, wifiSSID);
  EEPROM.get(sizeof(wifiSSID), wifiPass);
  Serial.println("Using Credentials: " + wifiSSID + " :: " + wifiPass);

  WiFi.mode(WIFI_STA);
  WiFi.begin(wifiSSID, wifiPass);
}

void loop() {
  currTime = millis();

  // Track Wi-Fi connection
  wifiConnected = WiFi.status() == WL_CONNECTED;
  if (wifiConnected) {
    // Connect to InfluxDB once
    // if (!influx.connected) influx.connect(TZ_INFO);
    lastConnected = currTime;
  }

  // Launch AP on no WiFi or BOOT button press
  if (ap.launched) ap.handleClient();
  else if (digitalRead(BOOT) == LOW || currTime - lastConnected >= WIFI_TIMEOUT) {
    Serial.println("[ACCESS POINT]");
    ap.begin();
  }

  // Config time once
  if (!timeSetup && wifiConnected) {
    Serial.println("[CONFIG TIME]");
    configTime(GMT_OFFSET, DAYLIGHT_OFFSET, NTP_SERVER);
    hours = getHours();
    oldHours = hours;
    feed = getFeed(hours);
    oldFeed = feed;
    timeSetup = true;
  }

  // Update time
  if (currTime - lastTimeUpdt >= TIME_UPDT_TIMEOUT) {
    Serial.println("[UPDATE_TIME]");
    oldHours = hours;
    hours = getHours();
    lastTimeUpdt = currTime;
  }

  // Update the NeoPixel colors
  if (currTime - lastColorUpdt >= TIME_UPDT_TIMEOUT) {
    Serial.println("[LEDS]");
    oldColor = color;
    color = getColor(hours);

    Serial.println(hours);
    Serial.print(color);
    Serial.print(" :: ");
    Serial.println(oldColor);
    if (color != oldColor) {
      pixel1.configColor(COLORS[color]);
      pixel2.configColor(COLORS[color]);
    }

    pixel1.show();
    pixel2.show();
    lastColorUpdt = currTime;
  }

  // Trigger the servo if the time passes a new feeding time
  if (currTime - lastFeedUpdt >= TIME_UPDT_TIMEOUT) {
    Serial.println("[FEED]");
    oldFeed = feed;
    feed = getFeed(hours);

    Serial.print(feed);
    Serial.print(" :: ");
    Serial.println(oldFeed);

    if (feed != oldFeed) digitalWrite(BUILTIN_LED, HIGH);
    else digitalWrite(BUILTIN_LED, LOW);
    lastFeedUpdt = currTime;
  }

  // Update the sensor readings
  if (currTime - lastRead >= READ_TIMEOUT) {
    Serial.println("[SENSORS]");
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

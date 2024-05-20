// Libraries
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiUdp.h>
#include <Preferences.h>
#include <DHT.h>                // "DHT sensor library" by "Adafruit" v1.4.6
#include <DallasTemperature.h>  // "DallasTemperature" by "Miles Burton" v3.9.0
#include <NTPClient.h>          // "NTPClient" by "Fabrice Weinberg" v3.2.1
#include <Adafruit_NeoPixel.h>  // "Adafruit NeoPixel" by "Adafruit" v1.12.0
#include <ESP32Servo.h>         // "ESP32Servo" by "Kevin Harrington" v1.1.2
#include <ArduinoJson.h>        // "ArduinoJson" by "Benoit Blanchon" v7.0.4
#include "DhtSensor.h"
#include "DallasSensor.h"
#include "GenericSensor.h"
#include "AccessPoint.h"
#include "NeoPixel.h"
#include "Secrets.h"

// Pin I/O
#define BOOT 0        // Built-in boot button (D0)
#define LIGHTS 2      // Lights actuator (D2)
#define THERMOSTAT 4  // Thermostat actuator (D4)
#define FILTERS 5     // Filters actuator (D5)
#define DHTPIN 13     // DHT11 sensor (D13)
#define SERVO 15      // Lights actuator (D15)
#define WTEMP 32      // Water temperature sensor (A4)
#define TURBIDITY 35  // Turbidity sensor (A6)
#define WLEVEL 34     // Water level sensor (A7)
#define NEOLIGHT1 19  // Neopixel strip 1 (D19)
#define NEOLIGHT2 18  // Neopixel strip 2 (D18)

// Constants
const char* AP_SSID = "Acuatech SSID";  // SSID of the access point Wi-Fi network
const char* AP_PASS = "PASSWORD";      // Password of the access point Wi-Fi network
#define BACKEND_URL "BACKEND_ORIGIN"
#define BACKEND_DATA "BACKEND_ORIGIN/dashboard/data/"
#define HTTP_TIMEOUT 2000  // Limit time on WiFi disconnection
#define WIFI_TIMEOUT 10000  // Limit time on WiFi disconnection

#define GMT_OFFSET -18000          // Timezone offset compared to GMT
#define DAYLIGHT_OFFSET 0          // Daylight savings offset
#define NTP_SERVER "pool.ntp.org"  // NTP default server
#define TIME_UPDT_TIMEOUT 1000     // Interval for reading the time

#define DHTTYPE DHT11          // Type of the DHT sensor
#define TURB_ANALOG true       // Whether the turbidity sensor is ADC
#define READ_TIMEOUT 2000      // Interval time for reading all the sensors
#define PIXELS1 12             // Amount of pixels in Neopixel strip 1
#define PIXELS2 24             // Amount of pixels in Neopixel strip 2
#define VAL_UPDT_TIMEOUT 1500  // Interval for updating time related variables like colors and feeding times
#define FEED_LENGTH 1000

uint8_t FEED_TIMES[3] = { 7, 12, 18 };
uint8_t COLOR_TIMES[5] = { 7, 10, 14, 18, 21 };  // TODO: Make configurable
uint8_t COLORS[5][8] = {
  { 255, 255, 255, 127, 127, 255, 20,  2 },
  { 255, 255, 255, 0,   0,   255, 50,  3 },
  { 255, 255, 255, 0,   0,   255, 100, 0 },
  { 255, 255, 255, 255, 212, 92,  75,  3 },
  { 255, 255, 255, 0,   0,   255, 25,  2 }
};

// Variables
String wifiSSID = "";    // SSID of the Wi-Fi network 
String wifiPass = "";    // Password of the Wi-Fi network 
String aquariumId = "";  // The ID of this device's aquarium
short hours = 0;         // The real time hour number
short oldHours = 0;
uint8_t color = -1;     // The color corresponding to the current hour
uint8_t oldColor = -1;  // The color that was chosen on the previous iteration
uint8_t feed = -1;
uint8_t oldFeed = -1;
unsigned int size = 0;
bool wifiConnected = false;  // Flag of successful Wi-Fi connection
bool timeSetup = false;      // Flag of configured time from NTP server
bool closing = true;

DhtSensor dht(DHTPIN, DHTTYPE);
DallasSensor dallas(WTEMP);
GenericSensor wlevel(WLEVEL, true);
GenericSensor turbidity(TURBIDITY, TURB_ANALOG);
AccessPoint ap(AP_SSID, AP_PASS, 80);
NeoPixel pixel1(PIXELS1, NEOLIGHT1);
NeoPixel pixel2(PIXELS2, NEOLIGHT2);
Servo feeder;
Preferences preferences;
Preferences relays;
JsonDocument httpRes;
JsonDocument httpReq;

// Time variables
unsigned long currTime = 0;          // Current relative time of the program
unsigned long lastConnected = 0;     // Last relative time with WiFi connection
unsigned long lastReconnection = 0;  // Last relative time attepting reconnection
unsigned long lastRead = 0;          // Last relative time reading sensors
unsigned long lastDataSend = 0;      // Last relative time sending data
unsigned long lastTimeUpdt = 0;      // Last relative time reading real time
unsigned long lastColorUpdt = 0;     // Last relative time updating NeoPixel colors
unsigned long lastFeedUpdt = 0;
unsigned long lastFeedOpen = 0;

// Subroutines
float analogPercentage(int value) {
  return map(value, 650, 0, 0, 4095) * 100 / 4095;
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

void printJson(char* label, JsonDocument doc) {
  Serial.print(label);
  serializeJson(doc, Serial);
  Serial.println();
}

// Main routines
void setup() {
  // Pin definition
  pinMode(BOOT, INPUT);
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(THERMOSTAT, OUTPUT);
  pinMode(FILTERS, OUTPUT);


  // Comms
  Serial.begin(115200);
  Serial2.begin(115200);
  preferences.begin("credentials");
  relays.begin("relays");

  // Output clearing
  digitalWrite(BUILTIN_LED, relays.getBool("lights"));
  digitalWrite(THERMOSTAT, relays.getBool("thermo"));
  digitalWrite(FILTERS, relays.getBool("filter"));

  // Sensors
  dht.begin();
  dallas.begin();
  wlevel.begin();
  if (TURB_ANALOG) turbidity.begin(analogPercentage);
  else turbidity.begin();
  feeder.attach(SERVO);

  // Actuators
  pixel1.begin(50);
  pixel2.begin(50);

  // Preferences
  wifiSSID = preferences.getString("wifi-ssid");
  wifiPass = preferences.getString("wifi-pass");
  aquariumId = preferences.getString("token");

  // Wi-Fi
  Serial.println("Using Credentials: " + wifiSSID + " :: " + wifiPass);
  Serial.println("User Token: " + aquariumId);
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifiSSID, wifiPass);
}

void loop() {
  currTime = millis();

  // Track Wi-Fi connection
  wifiConnected = WiFi.status() == WL_CONNECTED;
  if (wifiConnected) {
    // Connect to InfluxDB once
    lastConnected = currTime;
  }

  // Launch AP on no WiFi or BOOT button press
  if (ap.launched) ap.handleClient();
  else if (digitalRead(BOOT) == LOW || currTime - lastConnected >= WIFI_TIMEOUT) {
    Serial.println("[ACCESS POINT]");
    digitalWrite(BUILTIN_LED, HIGH);
    ap.begin(&preferences);
  }

  // Config time once
  if (!timeSetup && wifiConnected) {
    Serial.println("[CONFIG NTP]");
    configTime(GMT_OFFSET, DAYLIGHT_OFFSET, NTP_SERVER);
    hours = getHours();
    oldHours = hours;
    feed = getFeed(hours);
    oldFeed = feed;
    timeSetup = true;
  }

  // Update time
  if (timeSetup && currTime - lastTimeUpdt >= TIME_UPDT_TIMEOUT) {
    Serial.println("[UPDATE NTP]");
    oldHours = hours;
    hours = getHours();
    lastTimeUpdt = currTime;
  }

  // Update the NeoPixel colors
  if (timeSetup && currTime - lastColorUpdt >= VAL_UPDT_TIMEOUT) {
    Serial.println("[UPDATE COLORS]");
    oldColor = color;
    color = getColor(hours);

    if (color != oldColor) {
      pixel1.configColor(COLORS[color]);
      pixel2.configColor(COLORS[color]);
    }

    pixel1.show();
    pixel2.show();
    lastColorUpdt = currTime;
  }

  // Trigger the servo if the time passes a new feeding time
  if (timeSetup && currTime - lastFeedUpdt >= VAL_UPDT_TIMEOUT) {
    Serial.println("[UPDATE SERVO]");
    oldFeed = feed;
    feed = getFeed(hours);

    if (feed != oldFeed) {
      feeder.write(90);
      lastFeedOpen = currTime;
      closing = true;
    }
    lastFeedUpdt = currTime;
  }

  if (timeSetup && closing && currTime - lastFeedOpen >= FEED_LENGTH) {
    feeder.write(0);
    closing = false;
  }

  // Update the sensor readings
  if (currTime - lastRead >= READ_TIMEOUT) {
    Serial.println("[READ SENSORS]");
    dht.readSensor(0b11);
    dallas.readSensor();
    wlevel.readSensor();
    turbidity.readSensor();
    lastRead = currTime;
    // printData();
  }

  // Communicate data to InfluxDB
  if (currTime - lastDataSend >= HTTP_TIMEOUT && wifiConnected) {
    // Fetch data from the backed
    HTTPClient http;

    Serial.print("[HTTP] ");
    Serial.println(BACKEND_DATA);
    http.begin(BACKEND_DATA);
    http.addHeader("X-Request-Source", "ESP32");
    http.addHeader("X-User-Token", aquariumId);

    int code = http.GET();
    if (code > 0) {
      String payload = http.getString();

      deserializeJson(httpRes, payload);
      printJson("[GET] res = ", httpRes);
    } else {
      Serial.printf("[HTTP] GET failed. Error: %s\n", http.errorToString(code).c_str());
    }
    http.end();

    // Update relays with received data
    bool lights = httpRes["lights"];
    bool filter = httpRes["filter"];
    bool thermo = httpRes["thermo"];

    digitalWrite(LIGHTS, lights);
    digitalWrite(FILTERS, filter);
    digitalWrite(THERMOSTAT, thermo);

    relays.putBool("lights", lights);
    relays.putBool("filter", filter);
    relays.putBool("thermo", thermo);

    // Send sensor data to backend
    http.begin(BACKEND_DATA);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    http.addHeader("X-Request-Source", "ESP32");
    http.addHeader("X-User-Token", aquariumId);

    String postPayload = "";
    httpReq["temp"] = dht.temp;
    httpReq["hum"] = dht.hum;
    httpReq["wtemp"] = dallas.wtemp;
    httpReq["turbp"] = turbidity.scaled;
    httpReq["wlevel"] = wlevel.value;

    serializeJson(httpReq, postPayload);
    printJson("[POST] req = ", httpReq);
    code = http.POST(postPayload);
    if (code > 0) {
      String payload = http.getString();

      deserializeJson(httpRes, payload);
      printJson("[POST] res = ", httpRes);
    } else {
      Serial.printf("[HTTP] GET failed. Error: %s\n", http.errorToString(code).c_str());
    }
    http.end();
    lastDataSend = currTime;
  }
}

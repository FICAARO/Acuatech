#ifndef DHTSENSOR_H
#define DHTSENSOR_H

#include <DHT.h>  // "DHT sensor library" by "Adafruit": v1.4.6

class DhtSensor {
private:
  DHT dht;

  float getHumidity() {
    float h = this->dht.readHumidity();
    if (isnan(h)) return -1;
    return h;
  }

  float getTemperature(bool f) {
    float t = this->dht.readTemperature(f);
    if (isnan(t)) return -1;
    return t;
  }
public:
  float hum;
  float temp;

  DhtSensor(uint8_t pin, uint8_t type)
    : dht(pin, type) {
    this->hum = 0;
    this->temp = 0;
  }

  void begin() {
    this->dht.begin();
  }

  void readSensor(uint8_t readings) {
    if (readings >> 0 & 1) this->hum = this->getHumidity();
    if (readings >> 1 & 1) this->temp = this->getTemperature(false);
  }

  void print() {
    Serial.print("Humidity: ");
    Serial.print(this->hum);
    Serial.print(", Temperature: ");
    Serial.println(this->temp);
  }
};
#endif
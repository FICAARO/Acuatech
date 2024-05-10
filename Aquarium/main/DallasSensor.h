#ifndef DALLASSENSOR_H
#define DALLASSENSOR_H

#include <DallasTemperature.h>  // "DallasTemperature" by "Miles Burton": v3.9.0

class DallasSensor {
private:
  OneWire wire;
  DallasTemperature sensor;
public:
  float wtemp;

  DallasSensor(uint8_t pin)
    : wire(pin), sensor(&wire) {
    this->wtemp = -1000.0;
  }

  void begin() {
    this->sensor.begin();
  }

  void readSensor() {
    this->sensor.requestTemperatures();
    float t = this->sensor.getTempCByIndex(0);
    if (t == DEVICE_DISCONNECTED_C) this->wtemp = -1000.0;
    else this->wtemp = t;
  }

  void print() {
    Serial.print("WaterTemperature: ");
    Serial.println(this->wtemp);
  }
};
#endif
#ifndef GENERICSENSOR_H
#define GENERICSENSOR_H

class GenericSensor {
private:
  const uint8_t pin;
  const bool analog;
  float (*scale)(int);
public:
  int value;
  float scaled;

  GenericSensor(uint8_t pin, bool analog)
    : pin(pin), analog(analog) {
    this->value = 0;
    this->scaled = 0;
  }

  void begin() {
    if (this->analog) return;
    pinMode(this->pin, INPUT);
  }

  void begin(float (*scale)(int)) {
    this->scale = scale;
    this->begin();
  }

  void readSensor() {
    this->value = this->analog ? analogRead(this->pin) : digitalRead(this->pin);
    if (this->value > 4000) {
      this->value = -1000;
      this->scaled = -1000;
      return;
    }
    if (this->scale == NULL) return;
    this->scaled = this->scale(this->value);
  }

  void print(const String& label) {
    Serial.print(label + ": ");
    Serial.println(this->value);
  }

  void print(const String& label, const String& scale) {
    Serial.print(label + ": ");
    Serial.print(this->value);
    Serial.print(", " + label + " (" + scale + "): ");
    Serial.println(this->scaled);
  }
};
#endif
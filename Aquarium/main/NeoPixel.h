#ifndef NEOPIXEL_H
#define NEOPIXEL_H

#include <Adafruit_NeoPixel.h>

class NeoPixel {
private:
  Adafruit_NeoPixel leds;

public:
  NeoPixel(uint16_t n, int16_t pin)
    : leds(n, pin) {}

  void begin(uint8_t level) {
    this->leds.begin();
    this->leds.setBrightness(level);
    this->leds.show();
  }

  void show() {
    this->leds.show();
  }

  void configColor(uint8_t clr[8]) {
    this->leds.clear();
    this->leds.setBrightness(clr[6]);
    for (uint8_t i = 0; i < this->leds.numPixels(); i++) {
      unsigned short c = 0;
      if (clr[7] > 0 && i % clr[7] == 0) c = 3;
      this->leds.setPixelColor(i, this->leds.Color(clr[c], clr[c+1], clr[c+2]));
    }
  }
};
#endif
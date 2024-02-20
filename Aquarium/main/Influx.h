#ifndef INFLUX_H
#define INFLUX_H

class Influx {
public:
  InfluxDBClient client;
  Point sensor;
  bool connected;
  bool writeStatus;

  Influx(const String& url, const String& org, const String& bucket, const String& token, const char* cert, const String& tag)
    : client(url, org, bucket, token, cert), sensor(tag) {
    this->connected = false;
    this->writeStatus = false;
  }

  void connect(const String& timezone) {
    if (this->connected) return;
    this->connected = true;
    
    this->sensor.addTag("device", "esp32_ns");
    timeSync(timezone.c_str(), "pool.ntp.org", "time.nis.gov");

    if (this->client.validateConnection()) {
      Serial.print("Connected to InfluxDB. URL: ");
      Serial.println(this->client.getServerUrl());
      this->connected = true;
    } else {
      Serial.print("Connection Failed. Error: ");
      Serial.println(this->client.getLastErrorMessage());
      this->connected = false;
    }
  }

  void printLineProtocol() {
    Serial.print("Writing: ");
    Serial.println(this->client.pointToLineProtocol(this->sensor));
  }

  void write() {
    this->writeStatus = this->client.writePoint(this->sensor);
    if (!this->writeStatus) {
      Serial.println("Failed to Write");
      Serial.println(this->client.getLastErrorMessage());
    }
  }
};
#endif
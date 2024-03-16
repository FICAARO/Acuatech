#ifndef ACCESS_POINT_H
#define ACCESS_POINT_H

#include <WiFi.h>
#include <EEPROM.h>

class AccessPoint {
private:
  WiFiServer server;  // Wi-Fi server instance
  const char* SSID;   // SSID of the access point Wi-Fi network
  const char* PASS;   // Password of the access point Wi-Fi network

  String header = "";  // Stores current request's header
  String line = "";    // Stores the header line by line

  // HTTP response for code 301 Moved Permanently
  char* res301 = "HTTP/1.1 301 Moved Permanently\n"
                 "Location: /?reset=1\n"
                 "Connection: close\n";
  // HTTP response for code 200 OK
  char* res200 = "HTTP/1.1 200 OK\n"
                 "Content-Type: text/html\n"
                 "Connection: close\n";

  // Global HTML head
  char* head = "<!DOCTYPE html>"
               "<html>"
               "<head>"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
               "<style>"
               "html, body { font-family: 'Segoe UI', Helvetica, sans-serif; color: white; margin: 0 auto; text-align: center; background: hsl(210, 5%, 5%); }"
               "h1 { font-weight: 500; color: white; }"
               "p { color: #cfcfcf; }"
               "form { flex-wrap: wrap; width: 35rem; max-width: 100%; margin: 0 auto; }"
               ".form-wrap { display: flex; justify-content: center; align-items: center; }"
               "input { margin: .5rem; padding: .5rem; background: transparent; color: #e0e0e0; flex-grow: 1; border: 1px solid #909090; border-radius: 6px; }"
               ".button { border: none; border-radius: 6px; color: white; padding: 1rem 2rem; text-decoration: none; margin: .25rem; cursor: pointer; }"
               ".button.on { background: hsl(190, 100%, 30%); }"
               ".button.off { background: hsl(210, 5%, 20%); }"
               "</style>"
               "</head>";
  // Main HTML body [pathname == "/"]
  char* bodyMain = "<body>"
                   "<h1> Aquarium Configuration </h1>"
                   "<form action=\"/setup/wifi\" method=\"post\">"
                   "<div class=\"form-wrap\">"
                   "<input id=\"wifi-ssid\" name=\"wifi-ssid\" placeholder=\"Wi-Fi SSID\" />"
                   "</div>"
                   "<div class=\"form-wrap\">"
                   "<input id=\"wifi-pass\" name=\"wifi-pass\" type=\"password\" placeholder=\"Wi-Fi Password\" />"
                   "</div>"
                   "<button class=\"button on\" type=\"submit\">Submit</button>"
                   "</form>"
                   "</body>"
                   "</html>\n";
  // Reset HTML body [pathname == "/restart"]
  char* body404 = "<body>"
                  "<h1> Go home man. </h1>"
                  "<a href=\"/\" class=\"button on\">Home</a>"
                  "</body>"
                  "</html>";
public:
  bool launched;

  AccessPoint(const char* ssidAP, const char* passAP, uint8_t port)
    : server(port), SSID(ssidAP), PASS(passAP) {
    // Program starts without AP
    this->launched = false;
  }

  void begin() {
    this->launched = true;                // Only launches once per program
    WiFi.softAP(this->SSID, this->PASS);  // Initialize AP

    // Retreive the IP
    IPAddress ip = WiFi.softAPIP();
    Serial.print("AP IPv4: ");
    Serial.println(ip);

    // Start the server
    this->server.begin();
  }

  void handleClient() {
    // Omit handling when no client was found
    WiFiClient client = this->server.available();
    if (!client) return;

    // Flag if the board needs to restart after the connection
    bool post = false;
    while (client.connected()) {
      if (!client.available()) {
        continue;
      };

      // Read the request line by line until the entire header is read
      this->line = client.readStringUntil('\n');
      if (this->line.startsWith("Content-Length")) post = true;
      this->header += this->line;
      Serial.println(this->line);

      // Keep reading until an empty line and its not in the middle of a POST request
      if (this->line.length() > 1) {
        continue;
      }
      else if (post) {
        post = false;
        this->header += client.readStringUntil('\n');
      }

      // On [/setup/wifi] extract the credentials and schedule a board restart
      if (this->header.indexOf("POST /setup/wifi") != -1) {
        String ssid = header.substring(header.indexOf("wifi-ssid=") + 10, header.indexOf("&"));
        String pass = header.substring(header.indexOf("wifi-pass=") + 10);

        // TODO: Decode URL
        ssid.replace('+', ' ');
        pass.replace('+', ' ');

        EEPROM.put(0, ssid);
        EEPROM.put(sizeof(ssid), pass);
        EEPROM.commit();

        Serial.print("New Credentials: ");
        Serial.print(ssid);
        Serial.print(" :: ");
        Serial.println(pass);

        client.println(this->res301);
      } else if (this->header.indexOf("GET /") != -1) {
        client.println(this->res200);
        client.println(this->head);
        client.println(this->bodyMain);

        if (this->header.indexOf("?reset=1") != -1) {
          delay(100);
          client.stop();
          ESP.restart();
          break;
        }
      } else {
        client.println(res200);
        client.println(head);
        client.println(body404);
      }

      client.stop();
      break;
    }
    // Clear the request and stop the client
    this->header = "";
    client.stop();
  }
};
#endif
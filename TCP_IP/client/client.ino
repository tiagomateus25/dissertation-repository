#include<ESP8266WiFi.h>

//byte num = 0;
float num = 1.234;
char* host = "192.168.56.237";
uint16_t port = 10000;
void setup()
{
  WiFi.begin("Tiago", "12345678");
  delay(3000);
}

void loop()
{ 
  WiFiClient client;
  client.connect(host, port);
  if(client.connected())
  {
    client.print(num);
    delay(10);
  }
}

#include "MMA7660.h"

MMA7660 accelemeter;
void setup()
{
  accelemeter.init();
  Serial.begin(115000);
}
void loop()
{
  int8_t x, y, z;
  char tmp[16];
  char incomingByte;

  if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
      if (incomingByte == 'G') {
        accelemeter.getXYZ(&x,&y,&z);
        sprintf(tmp, "%02X%02X%02X\n", (uint8_t)x, (uint8_t)y, (uint8_t)z);
        Serial.print(tmp);
      }
  }
}


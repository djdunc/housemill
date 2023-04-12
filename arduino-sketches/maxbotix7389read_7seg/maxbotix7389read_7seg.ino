/*
  AnalogReadSerial - Maxbotix MB7389 HRXL MaxSonar WR 
  5V
  GND
  pin 3 of MB7389 connected to AO

  7 seg connected to GND and 3.3V, SDA, SCL

  Duncan Wilson - April 2023

*/

#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_7segment matrix = Adafruit_7segment();

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // initialise 7 seg display
  matrix.begin(0x70);  
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0) * 5; // multiply by 5 since 5m sensor so range Vcc/5120 per 1mm
  Serial.println(sensorValue);
  matrix.print(sensorValue);
  matrix.writeDisplay();
  delay(1000);  // delay in between reads for stability
}

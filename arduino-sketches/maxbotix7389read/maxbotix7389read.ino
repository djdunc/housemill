/*
  AnalogReadSerial - Maxbotix MB7389 HRXL MaxSonar WR 
  5V
  GND
  pin 3 of MB7389 connected to AO

  Duncan Wilson - April 2023

*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0) * 5; // multiply by 5 since 5m sensor so range Vcc/5120 per 1mm
  Serial.println(sensorValue);
  delay(1000);  // delay in between reads for stability
}

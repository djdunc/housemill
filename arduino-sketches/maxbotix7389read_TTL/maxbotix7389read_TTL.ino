/*
  TTL ReadSerial - Maxbotix MB7389 HRXL MaxSonar WR 
  5V
  GND
  pin 5 of MB7389 connected to DO

  Duncan Wilson - April 2023

  https://maxbotix.com/blogs/blog/mb7389-x-arduino-tutorial-with-code-examples

*/
char buf[7];
static uint32_t msTimeout = 0;              // timestamp of recently found R
int distanceToWaterMM = 0;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial1.begin(9600); // RX pin D0
}

// the loop routine runs over and over again forever:
void loop() {
                                              // persists between calls of function
  while(Serial1.available()) {
    if ('R' == Serial1.peek()) {
      if (!msTimeout) msTimeout = millis();   // when new R found - store timestamp
      if (Serial1.available() >= 5) {         // already received a complete packet?
        memset(buf, 0x00, sizeof(buf));       // ensure properly terminated string
        Serial1.readBytes(buf, 6);            // read the packet
        distanceToWaterMM = atoi(&buf[1]);    // convert string following the R to integer
        msTimeout = 0;                        // prepare for next incoming R
        Serial.println(distanceToWaterMM);
      }
      else if(millis() - msTimeout > 1000) {  // current R is outdated
        Serial1.read();                       // flush R and move on
        msTimeout = 0;                        // prepare for next incoming R   
      }
    }
    else {
      Serial1.read();                        // flush "orphaned" bytes
    }
  }
    
}

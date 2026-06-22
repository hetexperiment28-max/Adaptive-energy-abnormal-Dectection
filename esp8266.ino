
//code to get esp data from electricity measurement sensor (for project used potentiometer to fake voltage currents data to show live on stage)
#define POT_PIN A0   // For ESP32 (use A0 for ESP8266)

void setup() {
  Serial.begin(115200); //remember baud rate for addig in python code. must be same on both side
}

void loop() {
  int rawValue = analogRead(POT_PIN);

  // Convert to simulated energy value (scale)
  float energyValue = (rawValue / 4095.0) * 50.0;  // 0–10 range

  Serial.println(energyValue);

  delay(3000);  // send every 3 second time stamp
}

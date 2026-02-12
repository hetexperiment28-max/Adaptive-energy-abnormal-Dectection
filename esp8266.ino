#define POT_PIN A0   // For ESP32 (use A0 for ESP8266)

void setup() {
  Serial.begin(115200);
}

void loop() {
  int rawValue = analogRead(POT_PIN);

  // Convert to simulated energy value (scale)
  float energyValue = (rawValue / 4095.0) * 50.0;  // 0–10 range

  Serial.println(energyValue);

  delay(5000);  // send every 1 second
}

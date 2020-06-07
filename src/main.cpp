#include <Arduino.h>
// ONLY used to let pio compile the libs successfuly

void setup() {
	pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
	digitalWrite(LED_BUILTIN, HIGH);
	delay(2000);
	digitalWrite(LED_BUILTIN, LOW);
	delay(1000);
}

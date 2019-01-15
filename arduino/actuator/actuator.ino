#include <Servo.h>
#include <Wire.h>

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif

// set I2C address
const int I2C_ADDR = 0x8;

// configure pin addresses
const int LED_PIN = LED_BUILTIN;

const int SERVO_PIN_0 = 5;
const int SERVO_PIN_1 = 6;
const int SERVO_PIN_2 = 9;
const int SERVO_PIN_3 = 10;
const int SERVO_PIN_4 = 11;

// initialize Servo
Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // initialize Meccano LED pin as an output
  pinMode(MECC_LED_PIN, OUTPUT);

  // initialize Servos
  servo0.attach(SERVO_PIN_0);
  servo1.attach(SERVO_PIN_1);
  servo2.attach(SERVO_PIN_2);
  servo3.attach(SERVO_PIN_3);
  servo4.attach(SERVO_PIN_4);

  Wire.begin(I2C_ADDR);
  
  #if defined(__AVR_ATmega168__) || defined(__AVR_ATmega8__) || defined(__AVR_ATmega328P__)
    // deactivate internal pull-ups for twi
    // as per note from atmega8 manual pg167
    cbi(PORTC, 4);
    cbi(PORTC, 5);
  #else
    // deactivate internal pull-ups for twi
    // as per note from atmega128 manual pg204
    cbi(PORTD, 0);
    cbi(PORTD, 1);
  #endif

  Wire.onReceive(receiveEvent); // register event handler

  Serial.begin(9600);
  
  delay(2000);
}

// the loop function runs over and over again forever
void loop() {
  // NOP
}

// action received for test (internal Ardino) LED
void actionTestLed(char setting) {
  if (setting == 0) {
    digitalWrite(LED_PIN, 0);
  } else {
    digitalWrite(LED_PIN, 1);
  }
}

// action received for servo
void actionServo(char id, char setting) {
  if (id == 0) {
    servo0.write(setting * 2);
  } else if (id == 1) {
    servo1.write(setting * 2);
  } else if (id == 2) {
    servo2.write(setting * 2);
  } else if (id == 3) {
    servo3.write(setting * 2);
  } else if (id == 4) {
    servo4.write(setting * 2);
  }
}

// process received event
void processEvent(char type, char id, char setting) {
  if (type == 'L') {
    actionTestLed(setting);
  } else if (type == 'S') {
    actionServo(id, setting);
  }
}

// executes when data is received from I2C master
// registered as an event handler; see setup()
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    if (Wire.available() == 3) {
      char type = Wire.read(); // receive byte as a character
      char id = Wire.read(); // receive byte as a character
      char setting = Wire.read(); // receive byte as a character
      processEvent(type, id, setting);
    } else {
      char c = Wire.read(); // receive byte as a character
    }
  }
}

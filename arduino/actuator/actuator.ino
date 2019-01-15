#include <Servo.h>
#include <Wire.h>

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif

// set I2C address
const int I2C_ADDR = 0x8;

// configure pin addresses
const int RELAY_PIN_0 = 0;
const int RELAY_PIN_1 = 1;
const int RELAY_PIN_2 = 2;
const int RELAY_PIN_3 = 4;
const int RELAY_PIN_4 = 7;
const int RELAY_PIN_5 = 8;
const int RELAY_PIN_6 = 12;
const int RELAY_PIN_7 = 13;

const int SERVO_PIN_0 = 3;
const int SERVO_PIN_1 = 5;
const int SERVO_PIN_2 = 6;
const int SERVO_PIN_3 = 9;
const int SERVO_PIN_4 = 10;
const int SERVO_PIN_5 = 11;

// initialize Servo
Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pins
  pinMode(RELAY_PIN_0, OUTPUT);
  pinMode(RELAY_PIN_1, OUTPUT);
  pinMode(RELAY_PIN_2, OUTPUT);
  pinMode(RELAY_PIN_3, OUTPUT);
  pinMode(RELAY_PIN_4, OUTPUT);
  pinMode(RELAY_PIN_5, OUTPUT);
  pinMode(RELAY_PIN_6, OUTPUT);
  pinMode(RELAY_PIN_7, OUTPUT);
  digitalWrite(RELAY_PIN_0, LOW);
  digitalWrite(RELAY_PIN_1, LOW);
  digitalWrite(RELAY_PIN_2, LOW);
  digitalWrite(RELAY_PIN_3, LOW);
  digitalWrite(RELAY_PIN_4, LOW);
  digitalWrite(RELAY_PIN_5, LOW);
  digitalWrite(RELAY_PIN_6, LOW);
  digitalWrite(RELAY_PIN_7, LOW);

  // initialize servos
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

// action received for relay
void actionRelay(char id, char setting) {
  char outVal = LOW;
  if (setting == 0) {
    outVal = LOW;
  } else {
    outVal = HIGH;
  }

  if (id == 0) {
    digitalWrite(RELAY_PIN_0, outVal);
  } else if (id == 1) {
    digitalWrite(RELAY_PIN_1, outVal);
  } else if (id == 2) {
    digitalWrite(RELAY_PIN_2, outVal);
  } else if (id == 3) {
    digitalWrite(RELAY_PIN_3, outVal);
  } else if (id == 4) {
    digitalWrite(RELAY_PIN_4, outVal);
  } else if (id == 5) {
    digitalWrite(RELAY_PIN_5, outVal);
  } else if (id == 6) {
    digitalWrite(RELAY_PIN_6, outVal);
  } else if (id == 7) {
    digitalWrite(RELAY_PIN_7, outVal);
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
  if (type == 'R') {
    actionRelay(id, setting);
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

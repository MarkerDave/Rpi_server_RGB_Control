/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
  modified 13 july 2016.
 */
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int LEDpin = 10;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(10, OUTPUT);
  Serial.begin(19200);
}

// the loop function runs over and over again forever
void loop() {
  serialEvent();
  if(stringComplete){
    Serial.println(inputString);
    if(inputString == "ON\n"){
      digitalWrite(LEDpin, HIGH);   // turn the LED on (HIGH is the voltage level)
      }
     if(inputString == "OFF\n"){
       digitalWrite(LEDpin, LOW);    // turn the LED off by making the voltage LOW
      }
    inputString = "";
    stringComplete = false;
    }
}
void serialEvent()
{
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


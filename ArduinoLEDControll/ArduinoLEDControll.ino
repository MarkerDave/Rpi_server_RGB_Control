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
  By Dave bemelmans
 */
 #include <NeoPixelBus.h>

const uint16_t PixelCount = 60;
const uint8_t PixelPin = 10;
 
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int red, green, blue = 0;

// three element pixels, in different order and speeds
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> strip(PixelCount, PixelPin);

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  Serial.begin(115200);
  strip.Begin();
  strip.Show();
}

// the loop function runs over and over again forever
void loop() {
  serialEvent();
  if(stringComplete){
    Serial.println(inputString);
    //all code here
    char charArray[30];
   
    int k = 0;
    int L = 0;
    for(int i = 0; i< inputString.length();i++){
      if(inputString[i] != ',' && inputString[i] !='\n')
      {
        charArray[k] = inputString[i];
        k++;
        Serial.print(charArray);
        Serial.print(" : ");
        Serial.println(L);
      }
      else{
        switch(L){
          case 0:
            red = atoi(charArray);
             L = 1;
            break;
          case 1:
            green = atoi(charArray);
             L = 2;
            break;
          case 2:
            blue = atoi(charArray);
            break;
        }     
        k =0;
       for(int i = 0; i<sizeof(charArray); i++){
        charArray[i] = (char)0;
       }
      }
    }
    RgbColor color(red, green, blue);
    for(int i = 0; i <= PixelCount; i++){
      strip.SetPixelColor(i,color);
      
    }
    strip.Show();
    Serial.println(red);
    Serial.println(green);
    Serial.println(blue);

    //******
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


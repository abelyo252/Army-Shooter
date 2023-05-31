
#include <Servo.h>
Servo servo1;  //Left right servo
Servo servo2;  //up down

int pos1 = 90;  //left right
int pos2 = 90;  //up down
int temp = 0; //For temp storage
int value = 5;

void setup() {
  Serial.begin(9600);
  servo1.attach(2);  //Left right
  servo2.attach(3);  //Up down
}

void left() {
  if (pos1 != 0) {
    pos1 -= value;
    servo1.write(pos1);
  }
}

void right() {
  if (pos1 != 180) {
    pos1 += value;
    servo1.write(pos1);
  }
}

void up() {
  if (pos2 != 180) {
    pos2 += value;
    servo2.write(pos2);
  }
}

void down() {
  if (pos2 != 0) {
    pos2 -= value;
    servo2.write(pos2);
  }
}

void rotate() {
  servo2.write(90); //Adjust camera!

  //For changing the temp value

  switch (pos1){
    case 0:
      temp = 0;
      break;
    case 180:
      temp = 1;
      break;
    default:
      // do nothing
      break;
      
  }

  switch (temp){
    case 1: // rotate to left
      pos1 -= value;
      servo1.write(pos1);
      break;
    case 0: //rotate to right
      pos1 += value;
      servo1.write(pos1);
      break;
    default:
      // do nothing
      break;
  }

}

void loop() {

  if (Serial.available() > 0) {  //When HC06 receive something

    String receive = Serial.readString();  //Read from Serial Communication

    switch (receive.toInt()) {
      case 1:
        right();
        break;
      case 2:
        left();
        break;
      case 3:
        up();
        break;
      case 4:
        down();
        break;
      case 23:  //left up
        left();
        up();
        Serial.println(receive);
        break;
      case 24:  //left down
        left();
        down();
        Serial.println(receive);
        break;
      case 13:  //Right up
        right();
        up();
        Serial.println(receive);
        break;
      case 14:  //Right down
        right();
        down();
        Serial.println(receive);
        break;
      case 5:  //Acquired
        //Stop at the point
        Serial.println(receive);
        break;
      case 6:  // Rotate
        rotate();
        Serial.println(receive);
        break;
      default:
        //do nothing
        break;
    }
  }
}

//Serial.println("Computer : " + String(receive[1]));

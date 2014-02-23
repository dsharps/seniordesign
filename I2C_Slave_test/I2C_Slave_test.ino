#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int x_rotation = 0;
int y_rotation = 0;
int thumbstick_X_pin = 0;
int thumbstick_Y_pin = 1;

int data_index = 0;

void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(9600);         // start serial for output
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    pinMode(thumbstick_X_pin, INPUT);
    pinMode(thumbstick_Y_pin, INPUT);

    Serial.println("Ready!");
}

void loop() {
    x_rotation = analogRead(thumbstick_X_pin);
    y_rotation = analogRead(thumbstick_Y_pin);
    Serial.print("X: ");
    Serial.print(x_rotation);
    Serial.print(", Y: ");
    Serial.print(y_rotation);
    Serial.print("\n");
    //delay(100);
}

// callback for received data
void receiveData(int byteCount){

    while(Wire.available()) {
        number = Wire.read();
        Serial.print("data received: ");
        Serial.println(number);

        if (number == 1){

            if (state == 0){
                digitalWrite(13, HIGH); // set the LED on
                state = 1;
            }
            else{
                digitalWrite(13, LOW); // set the LED off
                state = 0;
            }
         }
     }
}

// callback for sending data
void sendData(){
    switch (data_index){
      case 0: Wire.write(x_rotation & 0x00FF); break;
      case 1: Wire.write(x_rotation >> 8);   break;
      case 2: Wire.write(y_rotation & 0x00FF); break;
      case 3: Wire.write(y_rotation >> 8);   break;
      default: break;
    }
    data_index++;
    if (data_index == 4) {
      data_index = 0;
    }
}

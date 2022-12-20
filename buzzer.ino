const int buzzer = 12; //buzzer to arduino pin12
int incomingByte;      // a variable to read incoming serial data into

void setup(){
  pinMode(buzzer, OUTPUT); // Set buzzer
  Serial.begin(9600);
}

void loop(){
  // see if there's incoming serial data:
  if (Serial.available() > 0) 
  {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    if (incomingByte == 'u') {
      tone(buzzer, 25); // Send 25Hz signal for piezo feedback
      delay(500);        //buzz for 500 ms
    }
  }
  else
  {
    noTone(buzzer);
  }
}
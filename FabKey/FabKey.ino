/**
 * This code is made for the Sim900 module from epalsite.com
 * You can find the code on Github here : https://github.com/Nurrl/FabKey
 */

#include <SoftwareSerial.h>
SoftwareSerial Sim900Serial(2, 3);

// Define Pins
const byte pwrPin = 7;
const byte statusPin = 9;

const byte doorEnablePin = 8;
const byte doorLedPin = 13;
byte doorLedState = LOW;

// Define Timers
#include "Timer.h"
Timer doorStatusTimer(500, false);

// Latest SMS Storage
struct SMSs {
  String messageSender;
  String messageContent;

  bool isRead = true;
} latestSMS;

void setup() {
  /* Init pins */
  pinMode(pwrPin, OUTPUT);
  pinMode(statusPin, INPUT);
  
  pinMode(doorEnablePin, OUTPUT);
  pinMode(doorLedPin, OUTPUT);

  /* Init Serial and start Sim900 */
  Serial.begin(115200);
  Sim900Init();
}

void loop() {
  /* Computer serial loop */
  if (Serial.available() > 0) { // If we have an incomming byte, read it
    String incomingMessage = "";
    while (Serial.available() > 0)
      incomingMessage += Serial.readString();

    incomingMessage.trim();

    String inCmd = splitStr(incomingMessage, " ", 0);
    String inArgs = splitStr(incomingMessage, " ", 1);

    if (inCmd == "enableOpen") { // Enable door button
      doorStatusTimer.setStatus(true);

      digitalWrite(doorEnablePin, HIGH);
      digitalWrite(doorLedPin, HIGH);

      Serial.println("ok");
    } else if (inCmd == "disableOpen") { // Disable door button
      doorStatusTimer.setStatus(false);

      digitalWrite(doorEnablePin, LOW);
      digitalWrite(doorLedPin, LOW);
      
      Serial.println("ok");           
    } else if (inCmd == "sendSMS") { // Send new SMS to <number> with <message>
      String toNum = splitStr(inArgs, " ", 0);
      String messContent = splitStr(inArgs, " ", 1);

      if(toNum.length() == 12 && messContent.length() != 0) {
        sendSMS(toNum, messContent);
        Serial.println("ok"); 
      } else {
        Serial.println("err 2"); 
      }      
    } else if (inCmd == "getLatestSMS") { // Return the latest stored SMS
      if(!latestSMS.isRead) {
        Serial.println(latestSMS.messageSender + " -> " + latestSMS.messageContent);
        latestSMS.isRead = true;
      } else {
        Serial.println("none"); 
      }
    } else { // Output error
      Serial.println("err 1");      
    }
  }

  /* Sim900 Serial check loop */
  if(Sim900Serial.available()) {
    String incomingMessage = "";

    while(Sim900Serial.available() > 0)
      incomingMessage += Sim900Serial.readString();

    incomingMessage.trim();

    String inCmd = splitStr(incomingMessage, " ", 0);
    String inArgs = splitStr(incomingMessage, " ", 1);

    if (inCmd == "+CMT:") {
      String phoneNum = splitStr(inArgs, ",", 0);
      phoneNum.remove(0,1); phoneNum.remove(phoneNum.length() - 1, 1);
      
      String msgContent = splitStr(inArgs, "\r\n", 1);

      latestSMS.messageSender = phoneNum;
      latestSMS.messageContent = msgContent;

      latestSMS.isRead = false;
    }
  }

  /* Led Blink loop */
  if(doorStatusTimer.isElapsed()) { // If timer enabled, blink undefinitely with a 500ms delay
    if(doorLedState == LOW) 
      doorLedState = HIGH;
    else 
      doorLedState = LOW;

    digitalWrite(doorLedPin, doorLedState);
  }
}

void Sim900Init() {
  /* Start module if not started already */
  if(!digitalRead(statusPin)) {
    digitalWrite(pwrPin, HIGH);
    delay(2500);
    digitalWrite(pwrPin, LOW);
  }

  while(!digitalRead(statusPin)) {/* Wait for startup */}

  /* Begin SimReader serial */
  Sim900Serial.begin(9600);
  
  /* Setup basic params */
  sendAT("AT+CMGF=1"); // Set SMSs to text mode
  sendAT("AT+CPMS=ME"); // Set messages storage to module
  sendAT("AT+CMGD=1,4"); // Remove all messages from storage
  sendAT("AT+CNMI=2,2"); // Set SMS receive mode to notification
}

String sendAT(String command) {
  String commAnsw = "";
  
  Sim900Serial.print(command + '\r');

  delay(500); // Delay 500ms

  while(Sim900Serial.available() > 0)
    commAnsw += Sim900Serial.readString();
  
  return commAnsw;
}

void sendSMS(String phoneNumber, String textToSend) {
  sendAT("AT+CMGS=\"" + phoneNumber + "\""); // Set the phone number
  sendAT(textToSend); // Add message body
  sendAT((String)(char)26); // End the message
}

String splitStr(String checkString, String strDelim, bool strIndex) {
  String strOne, strTwo;
  int cutIndex = checkString.indexOf(strDelim);

  strOne = checkString.substring(0, cutIndex);
  strTwo = checkString.substring(cutIndex + strDelim.length()); 

  return (strIndex ? strTwo : strOne);
}


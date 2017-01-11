#include <SoftwareSerial.h>

#define pwrPin 7
#define rlayPin 8
 
SoftwareSerial Sim900Serial(2, 3);
 
void setup()
{
  Serial.begin(9600);
  // Sim900 init
  Sim900Init();
}
void loop()
{
  Sim900Serial.println("ATD0688210806;");
  while(1);
}

void Sim900Init() {
  /* Starting module with pwrPin hack */
  pinMode(pwrPin, OUTPUT);
  digitalWrite(pwrPin, HIGH);  
  delay(2500);
  digitalWrite(pwrPin, LOW);

  /* Setting baudrate to 19200 */
  Sim900Serial.begin(19200);
  Sim900Serial.flush();

  /* Wait for init */
  bool moduleReady = false;
  while (!moduleReady) {
    if (sendAT("AT+CREG?").indexOf("+CREG: 0,5") != -1)
      moduleReady = true;
    delay(500);
  }
}

String sendAT(String command) {
  Sim900Serial.flush();
  String commAnsw = "";
  
  Sim900Serial.println(command);
  delay(500);
  
  if (Sim900Serial.available() > 0)
    commAnsw = Sim900Serial.readString();
  
  return commAnsw;
}


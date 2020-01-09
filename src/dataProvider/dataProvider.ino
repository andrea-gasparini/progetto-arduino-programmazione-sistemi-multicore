#include <DHT.h>

#define DEBUG_LED 13
#define DHT_PIN 12
#define THERMISTOR_PIN A0
#define PRESISTOR_PIN A1
#define POTENTIOMETER_PIN A5
#define FANDIRECTION01_PIN 2
#define FANPWM_PIN 3
#define FANDIRECTION10_PIN 4

#define RESPONSE_OFF 0
#define RESPONSE_LOW 128
#define RESPONSE_MEDIUM 180
#define RESPONSE_HIGH 255

DHT dht(DHT_PIN, DHT11);

void setup()
{
  pinMode(FANDIRECTION10_PIN, OUTPUT);
  pinMode(FANDIRECTION01_PIN, OUTPUT);
  pinMode(FANPWM_PIN, OUTPUT);

  digitalWrite(FANDIRECTION10_PIN, HIGH);
  digitalWrite(FANDIRECTION01_PIN, LOW);
  analogWrite(FANPWM_PIN, 0);

  pinMode(DEBUG_LED, OUTPUT);
  digitalWrite(DEBUG_LED, LOW);

  Serial.begin(9600);
}

void loop()
{
  Serial.print(dht.readTemperature());
  Serial.print('|');

  Serial.print(analogRead(THERMISTOR_PIN));
  Serial.print('|');

  Serial.print(analogRead(PRESISTOR_PIN));
  Serial.print('|');

  Serial.println(analogRead(POTENTIOMETER_PIN));

  checkResponse();

  delay(1000);
}

void checkResponse()
{
  String response = "";
  while ( Serial.available() )
      response += (char)Serial.read();

  if ( response == "OFF" )
  {
    //digitalWrite(DEBUG_LED, LOW);
    analogWrite(FANPWM_PIN, RESPONSE_OFF);
  }
  else if ( response == "LOW" )
  {
    //digitalWrite(DEBUG_LED, HIGH);
    analogWrite(FANPWM_PIN, RESPONSE_LOW);
  }
  else if ( response == "MEDIUM" )
  {
    //digitalWrite(DEBUG_LED, HIGH);
    analogWrite(FANPWM_PIN, RESPONSE_MEDIUM);
  }
  else if ( response == "HIGH" )
  {
    //digitalWrite(DEBUG_LED, HIGH);
    analogWrite(FANPWM_PIN, RESPONSE_HIGH);
  }
}

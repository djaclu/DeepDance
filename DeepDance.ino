//Libraries
#include <Wire.h>
#include <WiFi.h>
#include <ArduinoJson.h>

//WIFI Parameters
const char* ssid = "TP-LINK_A08E";
const char* password = "35157830";

//Server Parameters
const uint16_t port = 60000;
const char * host = "192.168.0.100";
WiFiClient client;

//MPU-6050 Parameters & Variables
const int MPU_addr=0x68; //I2C Address of MPU-6050
int16_t AX,AY,AZ,T,GX,GY,GZ;
StaticJsonDocument<200> doc;
JsonObject root = doc.to<JsonObject>();

//PINS
int motor1Pin = 16;
int motor2Pin = 19;
int motor3Pin = 23;
int led1Pin = 25;
int led2Pin = 26;
int led3Pin = 27;
int led4Pin = 32;

void setup() {

  //PINS
  pinMode(motor1Pin, OUTPUT);
  pinMode(motor2Pin, OUTPUT);
  pinMode(motor3Pin, OUTPUT);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);
  pinMode(led4Pin, OUTPUT);

  //Serial
  Serial.begin(115200);
  delay(1000);

  //MPU-6050
  Wire.begin(21, 22);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // Wake-up MPU-6050
  Wire.endTransmission(true);
  Wire.beginTransmission(0b1101000);
  Wire.write(0x1B);
  Wire.write(0x00000000); //Set Gyroscope Sensitivity
  Wire.endTransmission();
  Wire.beginTransmission(0b1101000);
  Wire.write(0x1C); //Set Accelerometer Sensitivity
  Wire.write(0b00010000);
  Wire.endTransmission();
  Serial.println("Connected to IMU.");

  //WIFI
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1500);
    Serial.println("Connecting to WIFI..");
  }
  Serial.println("Connected to ");
  Serial.print(WiFi.SSID());
  Serial.print(" with IP: ");
  Serial.print(WiFi.localIP());
}

void loop() {

  //LED
  //digitalWrite(led1Pin, HIGH);
  //digitalWrite(led2Pin, HIGH);
  //digitalWrite(led3Pin, HIGH);
  //digitalWrite(led4Pin, HIGH);

  WiFiClient client;
 
  if (!client.connect(host, port)) {
    Serial.print("\nConnecting to server..");
    delay(1000);
    return;
  }

  mpu_read();

  String output;
  serializeJson(doc, output);
  client.print(output); 

  if (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

    client.stop();
    delay(100);
}

void mpu_read(){

  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true);  // request a total of 14 registers

  AX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  T=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  process_acc_data();
  return;

 }

 void process_acc_data(){
  root["AX"] = AX/4096.0;
  root["AY"] = AY/4096.0;
  root["AZ"] = AZ/4096.0;
  root["GX"] = GX/131.0;
  root["GY"] = GX/131.0;
  root["GZ"] = GX/131.0;
  }

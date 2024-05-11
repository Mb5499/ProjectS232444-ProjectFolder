#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 10

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

int counter;
int cycle;
bool isCharging;


void setup() {
    Serial.begin(9600);
    pinMode(8, OUTPUT); // IN1
    pinMode(7, OUTPUT); // IN2
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    counter = 1;
    cycle = 1;
    isCharging = false;
}

void loop() {
    float voltage = (analogRead(A0) / 41.2);
    float current = analogRead(A1) / 183.3;
    float voltageLoad = analogRead(A2) / 41.2;
    float currentLoad = analogRead(A3) / 183.3;
    float temp = (analogRead(A4) - 550.0) * 0.0005;



    if (voltage <= 2.5) {
        // Start charging
        digitalWrite(8, LOW);
        digitalWrite(7, HIGH);
        isCharging = true;
    } else{
        // Stop charging
        digitalWrite(8, HIGH);
        digitalWrite(7, LOW);
        isCharging = false;
    }

    if (isCharging == true) {
        // Charging logic
        cycle++;
        while(voltage<4.12)
        {
          float voltageDischarge = (analogRead(A0) /41.2) * 1.14 ;   // Read voltage from A0, with example calibration

          voltage = voltageDischarge;

        if(voltage < 4.12){
          Serial.println("Voltage_charge");
          Serial.print(" ");
          Serial.print(voltageDischarge);
          Serial.println("");


          delay(2000);
        }
        else{
         isCharging = false;
         delay(3000);
        }
        }

    } else if(isCharging == false ){
        // Discharging logic
        Serial.println("");
        Serial.print("__");
        Serial.print("\t");
        Serial.print("Cycle");
        Serial.print("\t");
        Serial.print("voltage_measured");
        Serial.print("\t");
        Serial.print("current_measured");  // TAB space to separate columns
        Serial.print("\t");
        Serial.print("temprature_measured");
        Serial.print("\t");
        Serial.print("Current_load");
        Serial.print("\t");
        Serial.print("Voltage_load");  // TAB space to separate columns
    while (voltage > 2.5) {
      float voltageDischarge = (analogRead(A0) /41.2) * 1.14 ;   // Read voltage from A0, with example calibration
      float currentDischarge = analogRead(A1) / 183.3;  // Read current from A1, with example calibration
      float voltageLoadDischarge = (analogRead(A2) /41.2) * 0.897 ;  // Read voltage from A0, with example calibration
      float currentLoadDischarge = analogRead(A3) / 183.3;  // Read current from A1, with example calibration
      sensors.requestTemperatures(); 
      float Temp = sensors.getTempCByIndex(0);
      voltage = voltageDischarge;

      if(voltage > 2.5)
      {
      Serial.println("");
      Serial.print(counter);
      Serial.print("\t");
      Serial.print(cycle);
      Serial.print("\t");
      Serial.print(voltageDischarge, 5);
      Serial.print("\t");
      Serial.print(currentDischarge, 5);
      Serial.print("\t");
      Serial.print(Temp);
      Serial.print("\t");
      Serial.print( currentLoadDischarge, 5);
      Serial.print("\t");
      Serial.print(voltageLoadDischarge, 5);
      counter++; // Increment counter for each discharge reading
      voltage = voltageDischarge;
        delay(2000);
      }
      else
      {
        voltage = (analogRead(A0) /41.2) * 1.14;
        isCharging = true;
        delay(500);
      }
       // Delay for 3 seconds or as required
    }
        // Assume battery needs recharging after discharging   
}
    delay(50); // Short delay before starting the loop again

  }



#include <Adafruit_VL53L0X.h>
#include <Stepper.h>

// Define constants
const int stepsPerRevolution = 200;  // Adjust based on your stepper motor specs
const int stepperSpeed = 120;        // Increased speed in RPM
const int scanningResolution = 10;  // Increased angle increment to reduce steps

// Initialize ToF sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Initialize stepper motor (adjust pins as needed)
Stepper stepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(1); // Wait for Serial connection
  }

  // Initialize ToF sensor
  if (!lox.begin()) {
    Serial.println("Failed to initialize VL53L0X sensor!");
    while (1);
  }

  // Initialize stepper motor
  stepper.setSpeed(stepperSpeed);
  Serial.println("Stepper and ToF Sensor initialized.");
}

void loop() {
  // Perform a full 360° scan
  for (int angle = 0; angle < 360; angle += scanningResolution) {
    // Measure distance
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false);

    int distance = (measure.RangeStatus != 4) ? measure.RangeMilliMeter : -1; // -1 for out of range

    // Send (angle, distance) via Serial
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);

    // Rotate stepper motor by the resolution
    int steps = (stepsPerRevolution * scanningResolution) / 360; // Steps per resolution
    stepper.step(steps);

    delay(20); // Reduce delay to increase speed
  }

  // Return to the starting position
  stepper.step(-stepsPerRevolution); // Full revolution in reverse
}
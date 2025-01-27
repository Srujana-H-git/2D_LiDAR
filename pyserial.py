import serial  
import time
import matplotlib.pyplot as plt
import numpy as np
from serial import SerialException  

# Configure the serial port
serial_port = "COM8"  
baud_rate = 115200
timeout = 2  # Timeout in seconds

try:
    # Initialize the serial connection
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)  # Correct class name
    time.sleep(2)  # Wait for the serial connection to establish
except SerialException as e:  # Correct exception handling
    print(f"Error: Unable to connect to serial port {serial_port}. {e}")
    exit(1)

# Initialize lists for angle and distance
angles = []
distances = []

def capture_data():
    """
    Captures data from the Arduino via the serial port.
    """
    global angles, distances
    angles.clear()  # Clear lists before capturing new data
    distances.clear()

    print("Capturing data...")

    while True:
        try:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()

            if line:  # Ensure we have valid data
                # Parse the angle and distance
                angle, distance = line.split(',')
                angle = int(angle)
                distance = int(distance)

                # Append data to the lists
                angles.append(angle)
                distances.append(distance)

                print(f"Angle: {angle}, Distance: {distance}")

                # Break the loop after a full 360° scan
                if angle >= 355:  # Assuming scanning starts from 0°
                    break
        except ValueError:
            print(f"Error: Malformed data received: {line}. Skipping...")
        except Exception as e:
            print(f"Error reading data: {e}")
            break

def plot_data(angles, distances):
    """
    Plots the polar data using matplotlib.
    """
    if not angles or not distances:
        print("No data to plot.")
        return

    # Convert polar to Cartesian coordinates
    angles_rad = np.radians(angles)  # Convert angles to radians
    x = np.array(distances) * np.cos(angles_rad)
    y = np.array(distances) * np.sin(angles_rad)

    # Create a polar plot
    plt.figure(figsize=(8, 8))
    plt.polar(angles_rad, distances, marker='o', linestyle='-', label='Distance Data')
    plt.title("2D Lidar Plot (Polar)")
    plt.legend()

    # Cartesian scatter plot overlay
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, label="Scan Data (Cartesian)", c='red')
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("2D Lidar Plot (Cartesian)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')

    # Show the plots
    plt.show()

# Correct the condition for the main script entry point
if __name__ == "__main__":
    try:
        print("Waiting for data...")
        capture_data()
        print("Data capture complete. Plotting...")
        plot_data(angles, distances)
    finally:
        if ser.is_open:
            ser.close()
            print("Serial connection closed.")
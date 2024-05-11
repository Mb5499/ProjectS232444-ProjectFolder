import os
import serial
import time

# Setup serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for connection to establish

current_mode = None  # Keep track of the current mode ('voltage_charge' or 'voltage_load')
header_written = {'voltage_charge': False, 'voltage_load': False}  # Track if header has been written for each mode

# Check if 'voltage_load.txt' exists and if it contains 'voltage_measured'
fileN = "/home/senior/Downloads/BAT.csv"
if os.path.exists(fileN):
    with open(fileN, "r") as file:
        for line in file:
            if "voltage_measured" in line:
                header_written['voltage_load'] = True
                break

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip('\r\n')  # Read a line from the serial port, decode, and strip CR+LF
            if not line:
                # Skip empty lines
                continue

            # Check for mode-switching lines
            if "Voltage_charge" in line:
                current_mode = "voltage_charge"
                continue  # Skip writing when in charge mode
            elif "Voltage_load" in line:
                current_mode = "voltage_load"

            # Write to the corresponding file based on the current mode
            if current_mode == "voltage_load":
                with open(fileN, "a") as file:
                    # Check if the line is a header and if it has already been written
                    if "voltage" in line.lower():
                        if header_written[current_mode]:
                            continue
                        else:
                            header_written[current_mode] = True
                    file.write(line + "\n")  # Write the data line with a newline character
                    file.flush()  # Force write to disk immediately
                    os.fsync(file.fileno())  # Ensure all internal file buffers are written to disk
                    time.sleep(5)

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    ser.close()  # Close the serial connection


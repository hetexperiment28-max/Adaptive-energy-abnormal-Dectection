#to ensure esp sending signals perfectly or not
import serial

ser = serial.Serial("COM11",115200)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        print(line)

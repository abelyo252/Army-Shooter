import time
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)
ser.reset_input_buffer()
while True:
    message = "LD"
    ser.write(message.encode('utf-8'))
    time.sleep(2)
    print("Send Finish!")
    #print(ser.readline().decode())
ser.close()


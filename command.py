import threading
import main



def boundaryChecker(img, shot , OFFSET):

    x, y = shot
    h, w, _ = img.shape

    if x > (w // 2 - OFFSET) and x < (w // 2 + OFFSET) \
            and y > (h // 2 - OFFSET) and y < (h // 2 + OFFSET):
        return "Acquired"

    else:
        return "Tracking"

def mkDecision(img, shot,OFFSET):


    cmd1, cmd2 = 0, 0

    x, y = shot
    h, w, _ = img.shape

    if x > (w // 2 - OFFSET) and x < (w // 2 + OFFSET) \
            and y > (h // 2 - OFFSET) and y < (h // 2 + OFFSET):
        return cmd1, cmd2

    else:

        # Quandrant 2
        if x < (w // 2) and y < (h // 2):
            cmd1, cmd2 = -1, 1
            return cmd1, cmd2

        # Quandrant 1
        elif x > (w // 2) and y < (h // 2):
            cmd1, cmd2 = 1, 1
            return cmd1, cmd2

        # Quadrant 3
        elif x < (w // 2) and y > (h // 2):
            cmd1, cmd2 = -1, -1
            return cmd1, cmd2

        # Quadrant 4
        elif x > (w // 2) and y > (h // 2):
            cmd1, cmd2 = 1, -1
            return cmd1, cmd2

def cmdInterpret(cmd1, cmd2):
    if cmd1 == -1 and cmd2 == 1:
        return "RIGHT , UP"
    elif cmd1 == 1 and cmd2 == 1:
        return "LEFT , UP"
    elif cmd1 == -1 and cmd2 == -1:
        return "RIGHT , DOWN"
    elif cmd1 == 1 and cmd2 == -1:
        return "LEFT , DOWN"
    elif cmd1 == 0 and cmd2 == 0:
        return "AC"

def sendMessage(recv_message, ser):

    # Acquired Signal
    if recv_message == "AC":
        message = "5"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    # Rotate Signal
    elif recv_message == "RR":
        message = "6"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    # Left UP Signal
    elif recv_message == "LEFT , UP":
        message = "23"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    # Left Down Signal
    elif recv_message == "LEFT , DOWN":
        message = "24"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    # Right Up Signal
    elif recv_message == "RIGHT , UP":
        message = "13"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    # Right Down Signal
    elif recv_message == "RIGHT , DOWN":
        message = "14"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)


def left_manual(ser):
    message = "2"
    try:
        ser.write(message.encode('utf-8'))
    except Exception as e:
        print("Unable to send data", e)

def right_manual(ser):
    message = "1"
    try:
        ser.write(message.encode('utf-8'))
    except Exception as e:
        print("Unable to send data", e)

def up_manual(ser):
    message = "3"
    try:
        ser.write(message.encode('utf-8'))
    except Exception as e:
        print("Unable to send data", e)

def down_manual(ser):
    message = "4"
    try:
        ser.write(message.encode('utf-8'))
    except Exception as e:
        print("Unable to send data", e)

def receive_data(ser):
    data = None
    while True:
        try:
            data = ser.readline().decode().strip()
            if data!= None:
                event.set()
        except:
            pass

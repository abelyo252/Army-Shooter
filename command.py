
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

        if x < (w // 2) and y < (h // 2):
            cmd1, cmd2 = -1, 1
            return cmd1, cmd2
        elif x > (w // 2) and y < (h // 2):
            cmd1, cmd2 = 1, 1
            return cmd1, cmd2
        elif x < (w // 2) and y > (h // 2):
            cmd1, cmd2 = -1, -1
            return cmd1, cmd2
        elif x > (w // 2) and y > (h // 2):
            cmd1, cmd2 = 1, -1
            return cmd1, cmd2

def cmdInterpret(cmd1, cmd2):
    if cmd1 == -1 and cmd2 == 1:
        return "RIGHT , DOWN"
    elif cmd1 == 1 and cmd2 == 1:
        return "LEFT , DOWN"
    elif cmd1 == -1 and cmd2 == -1:
        return "RIGHT , UP"
    elif cmd1 == 1 and cmd2 == -1:
        return "LEFT , UP"
    elif cmd1 == 0 and cmd2 == 0:
        return "AC"

def sendMessage(recv_message, ser):
    if recv_message != "AC" or recv_message != "RR":
        recv_message = recv_message.split()
        message = recv_message[0][0] + recv_message[1][1]
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)

    elif recv_message == "RR":
        message = "RR"
        try:
            ser.write(message.encode('utf-8'))
        except Exception as e:
            print("Unable to send data", e)
    else:
        message = "AC"
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

def receive_data(ser,q):
    while True:
        try:
            data = ser.readline().decode().strip()
            q.put(data)
            print("Data Received : ",data)

        except:
            pass
# PyGame template.

# Import standard modules.
import sys
import time

# Import non-standard modules.
import pygame
from pygame.locals import *
import cv2
import numpy as np
from utils import trucate

import utils
import command

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import serial
import threading
import queue


class ArmyShooter:
    """
    Helps in finding Frames Per Second and display on an OpenCV Image
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.init()

        pygame.font.init()
        self.font = pygame.font.Font("Fonts/Bahnschrift/BAHNSCHRIFT 6.TTF", 12)

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        # self.IP = "http://192.168.205.44:4747/video?640x480"
        self.IP = "http://192.168.192.128:4747/mjpegfeed?640x480"
        self.RES_VID = "res/talk.mp4"
        self.RED_COLOR = (255, 0, 0)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.OFFSET = 0

        self.slider = Slider(self.screen, 75, 450, 200, 15, min=0, max=100, step=1)
        self.output = TextBox(self.screen, 278, 443, 30, 30, fontSize=18)
        self.output.disable()

        self.PILOT = True
        self.switcher = True
        self.event = threading.Event()

        try:
            self.cap = cv2.VideoCapture(self.IP)
            self.ser = serial.Serial('/dev/rfcomm0', 9600)
            self.ser.reset_input_buffer()


            print("Bluetooth and Camera connected successfully")
        except Exception as e:
            print("Unable to Connect with Hardware! ", e)

    def receive_data(self):
        data = None
        while True:
            try:
                data = self.ser.readline().decode().strip()
                if data != None:
                    self.event.set()
            except:
                pass

    def start_thread(self):
        t = threading.Thread(target=self.receive_data)
        t.daemon = True
        t.start()
        print("Thread Started !")


    def update(self, dt):

        # Go through events that are passed to the script by the window.
        events = pygame.event.get()
        for event in events:

            if event.type == QUIT:
                # When everything done, release
                self.cap.release()
                pygame.quit()  # Opposite of pygame.init
                sys.exit()  # Not including this line crashes the script on Windows. Possibly

                # User pressed down on a key
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_m:
                    self.PILOT = False
                if event.key == pygame.K_a:
                    self.PILOT = True

                if self.PILOT == False:
                    if event.key == pygame.K_LEFT:
                        try:

                            print("Left Command About to Send")
                            command.left_manual(self.ser)
                            print("Left Command Executed")

                        except Exception as e:
                            print("Unable to send data", e)
                    elif event.key == pygame.K_RIGHT:
                        try:

                            print("Right Command About to Send")
                            command.right_manual(self.ser)
                            print("Right Command Executed")

                        except Exception as e:
                            print("Unable to send data", e)
                    elif event.key == pygame.K_UP:
                        try:

                            print("Up Command About to Send")
                            command.up_manual(self.ser)
                            print("Up Command Executed")


                        except Exception as e:
                            print("Unable to send data", e)
                    elif event.key == pygame.K_DOWN:
                        try:

                            print("Down Command About to Send")
                            command.down_manual(self.ser)
                            print("Down Command Executed")

                        except Exception as e:
                            print("Unable to send data", e)

        pygame_widgets.update(events)
        pygame.display.update()

    def setTolerance(self, img, offset, rt=2):
        self.OFFSET = offset
        h, w, _ = img.shape
        start = w // 2 - offset, h // 2 - offset
        end = w // 2 + offset, h // 2 + offset
        cv2.rectangle(img, start, end, (0, 255, 0), rt)

        cv2.line(img, (w // 2, h // 2 - offset), (w // 2, 0), (0, 255, 0), rt)
        cv2.line(img, (w // 2, h // 2 + offset), (w // 2, h), (0, 255, 0), rt)
        cv2.line(img, (w // 2 - offset, h // 2), (0, h // 2), (0, 255, 0), rt)
        cv2.line(img, (w // 2 + offset, h // 2), (w, h // 2), (0, 255, 0), rt)

    def toolbar(self, displayText_upper, displayText_lower, mode):

        # Upper
        fpsd = self.font.render("FPS: " + str(displayText_upper[0]), False, (255, 255, 255))
        camera = self.font.render("Camera: " + str(displayText_upper[1]), False, (255, 255, 255))
        inf_t = self.font.render("Inf Time: " + str(displayText_upper[2]), False, (255, 255, 255))
        status = self.font.render("Status : " + str(displayText_upper[3]), False, (255, 255, 255))

        self.screen.blit(fpsd, (15, 15))
        self.screen.blit(camera, (115, 15))
        self.screen.blit(inf_t, (298, 15))
        self.screen.blit(status, (self.SCREEN_WIDTH - 100, 15))

        # Lower

        X_distance = self.font.render("X: " + str(displayText_lower[0]), False, (255, 255, 255))
        Y_distance = self.font.render("Y: " + str(displayText_lower[1]), False, (255, 255, 255))
        R_Direction = self.font.render("RD: " + str(displayText_lower[2]), False, (255, 255, 255))
        Mode_Disp = self.font.render(mode, False, (255, 255, 255))
        self.screen.blit(X_distance, (330, self.SCREEN_HEIGHT - 27))
        self.screen.blit(Y_distance, (385, self.SCREEN_HEIGHT - 27))
        self.screen.blit(R_Direction, (self.SCREEN_WIDTH - 100, self.SCREEN_HEIGHT - 30))
        self.screen.blit(Mode_Disp, (15, self.SCREEN_HEIGHT - 30))

    def draw(self):

        self.output.setText(self.slider.getValue())
        pTime = time.time()

        # Check if camera opened successfully
        if (self.cap.isOpened() == True):
            ret, frame = self.cap.read()

            cmd1, cmd2 = 0, 0
            cmdInt = ''
            res = ''

            h, w, _ = frame.shape

            self.setTolerance(frame, self.slider.getValue() + 50)
            # cv2.rectangle(frame, start2, end2, (0, 0, 255), -1)

            if ret == True:

                if self.PILOT:
                    bbox, shot = utils.findPose(frame)
                    cTime = time.time()

                    try:

                        inf_time = cTime - pTime
                        fps = 1 / inf_time
                    except:
                        print("Unable to calculate FPS")

                    if bbox:
                        if isinstance(shot, tuple) and len(shot) == 2:
                            res = command.boundaryChecker(frame, shot, self.OFFSET)
                            mk_decision_result = command.mkDecision(frame, shot, self.OFFSET)
                            if mk_decision_result is not None:
                                cmd1, cmd2 = mk_decision_result
                                cmdInt = command.cmdInterpret(cmd1, cmd2)

                                try:
                                    if (self.event.is_set()):
                                        self.switcher = True
                                        self.event.clear()

                                    if self.switcher:
                                        command.sendMessage(cmdInt, self.ser)
                                        self.switcher = False



                                except Exception as e:
                                    print("Unable to send data", e)

                            X = w // 2 - shot[0]
                            Y = h // 2 - shot[1]

                            frame = utils.fancyDraw(frame, bbox, (0, 255, 0), shot=True)
                            displayText_upper = [int(fps), "0.0166ms", trucate(inf_time, 4), res]
                            displayText_lower = [int(X), int(Y), cmdInt]
                            pTime = cTime

                    else:
                        displayText_upper = [int(fps), "0.0166ms", trucate(inf_time, 4), "No Obj"]
                        displayText_lower = [int(0), int(0), "None"]
                        pTime = cTime

                        try:
                            if (self.event.is_set()):
                                self.switcher = True
                                self.event.clear()

                            if self.switcher:
                                command.sendMessage("RR", self.ser)
                                self.switcher = False



                        except Exception as e:
                            print("Unable to send data", e)

                    # frame = cv2.resize(frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), interpolation=cv2.INTER_LINEAR)
                    self.screen.blit(self.cvimage_to_pygame(frame), (0, 0))
                    if self.PILOT:
                        self.toolbar(displayText_upper, displayText_lower, "Auto")
                    else:
                        self.toolbar(displayText_upper, displayText_lower, "Man")


                else:

                    self.screen.blit(self.cvimage_to_pygame(frame), (0, 0))


        else:
            # print("Unable to find Camera")
            self.screen.fill((0, 0, 0))  # Fill the screen with black.
            Err_Disp = self.font.render("Unable to find Camera  :(", False, (255, 255, 255))
            self.screen.blit(Err_Disp, (260, 220))
            try:
                if (self.event.is_set()):
                    self.switcher = True
                    self.event.clear()

                if self.switcher:
                    command.sendMessage("RR", self.ser)
                    self.switcher = False



            except Exception as e:
                print("Unable to send data", e)

        # pygame.display.flip()

    def cvimage_to_pygame(self, image):
        """Convert cvimage into a pygame image"""
        image_bgr = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_rgb = np.rot90(image_rgb)
        image_rgb_p = pygame.surfarray.make_surface(image_rgb).convert()
        image_rgb_p = pygame.transform.flip(image_rgb_p, True, False)
        return image_rgb_p

    def runPyGame(self):

        # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
        fps = 60.0
        fpsClock = pygame.time.Clock()

        # Main game loop.
        dt = 1 / fps  # dt is the time since last frame.
        while True:  # Loop forever!
            self.update(dt)  # You can update/draw here, I've just moved the code for neatness.
            self.draw()

            dt = fpsClock.tick(fps)


if __name__ == '__main__':
    # aShooter = ArmyShooter(932,601)
    aShooter = ArmyShooter(640, 480)
    aShooter.start_thread()
    aShooter.runPyGame()

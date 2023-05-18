# PyGame template.

# Import standard modules.
import sys

# Import non-standard modules.
import pygame
from pygame.locals import *
import cv2
import numpy as np
from utils import trucate
import time
import utils

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class ArmyShooter:
    """
    Helps in finding Frames Per Second and display on an OpenCV Image
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.init()

        pygame.font.init()
        self.font = pygame.font.Font("Fonts/Bahnschrift/BAHNSCHRIFT 6.TTF",18)

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.IP = "http://192.168.17.110:8080/video"
        self.RES_VID = "res/talk2.mp4"
        self.cap = cv2.VideoCapture(self.IP)
        self.RED_COLOR = (255, 0, 0)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.OFFSET=0


        self.slider = Slider(self.screen, 75, 570, 200, 15, min=0, max=100, step=1)
        self.output = TextBox(self.screen, 278, 563, 30, 30, fontSize=18)
        self.output.disable()




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

                if event.key == pygame.K_LEFT:
                    print("Left")
                elif event.key == pygame.K_RIGHT:
                    print("Right")
                elif event.key == pygame.K_UP:
                    print("Up")
                elif event.key == pygame.K_DOWN:
                    print("Down")

        pygame_widgets.update(events)
        pygame.display.update()

    def setTolerance(self,img,offset,rt=2):
        self.OFFSET = offset
        h, w, _ = img.shape
        start = w//2 - offset, h//2 - offset
        end =  w//2 + offset, h//2 + offset
        cv2.rectangle(img, start, end, (0, 255, 0), rt)

        cv2.line(img, (w // 2, h//2- offset), (w // 2, 0), (0, 255, 0), rt)
        cv2.line(img, (w // 2, h//2 + offset), (w // 2, h), (0, 255, 0), rt)
        cv2.line(img, (w // 2 - offset, h//2), (0,h//2), (0, 255, 0), rt)
        cv2.line(img, (w // 2 + offset, h // 2), (w,h//2), (0, 255, 0), rt)





    def toolbar(self,displayText_upper,displayText_lower):

        # Upper
        fpsd = self.font.render("FPS: "+str(displayText_upper[0]),False,(255,255,255))
        camera = self.font.render("Camera: "+str(displayText_upper[1]), False, (255, 255, 255))
        inf_t = self.font.render("Inf Time: "+str(displayText_upper[2]), False, (255, 255, 255))
        status = self.font.render("Status : " + str(displayText_upper[3]), False, (255, 255, 255))

        self.screen.blit(fpsd, (15, 10))
        self.screen.blit(camera, (115, 10))
        self.screen.blit(inf_t, (298, 10))
        self.screen.blit(status, (self.SCREEN_WIDTH - 150, 10))

        # Lower

        X_distance = self.font.render("X: "+str(displayText_lower[0]), False, (255, 255, 255))
        Y_distance = self.font.render("Y: "+str(displayText_lower[1]), False, (255, 255, 255))
        R_Direction = self.font.render("RD: "+str(displayText_lower[2]), False, (255, 255, 255))
        self.screen.blit(X_distance, (330, self.SCREEN_HEIGHT-30))
        self.screen.blit(Y_distance, (385, self.SCREEN_HEIGHT-30))
        self.screen.blit(R_Direction, (self.SCREEN_WIDTH - 150, self.SCREEN_HEIGHT-30))

    def boundaryChecker(self, img, shot):

        x, y = shot
        h, w, _ = img.shape

        if x > (w // 2 - self.OFFSET) and x < (w // 2 + self.OFFSET) \
                and y > (h // 2 - self.OFFSET) and y < (h // 2 + self.OFFSET):
            return "Acquired"

        else:
            return "Tracking"

    def mkDecision(self, img, shot):


        cmd1, cmd2 = 0, 0

        x, y = shot
        h, w, _ = img.shape

        if x > (w // 2 - self.OFFSET) and x < (w // 2 + self.OFFSET) \
                and y > (h // 2 - self.OFFSET) and y < (h // 2 + self.OFFSET):
            return cmd1, cmd2

        else:

            if x < (w // 2) and y < (h // 2):
                cmd1, cmd2 = -1, 1
                return cmd1, cmd2

            elif x > (w // 2) and y < (h // 2):
                cmd1, cmd2 = 1, 1
                return cmd1, cmd2
            elif x > (w // 2) and y < (h // 2):
                cmd1, cmd2 = -1, -1
                return cmd1, cmd2
            elif x > (w // 2) and y < (h // 2):
                cmd1, cmd2 = 1, -1
                return cmd1, cmd2

    def cmdInterpret(self, cmd1, cmd2):
        if cmd1 == -1 and cmd2 == 1:
            return "LEFT , DOWN"
        elif cmd1 == 1 and cmd2 == 1:
            return "RIGHT , DOWN"
        elif cmd1 == -1 and cmd2 == -1:
            return "LEFT , UP"
        elif cmd1 == -1 and cmd2 == -1:
            return "RIGHT , UP"


    def draw(self):

        self.output.setText(self.slider.getValue())
        pTime = time.time()

        # Check if camera opened successfully
        if (self.cap.isOpened() == True):
            ret, frame = self.cap.read()
            h, w, _ = frame.shape
            self.setTolerance(frame, self.slider.getValue() + 50)
            # cv2.rectangle(frame, start2, end2, (0, 0, 255), -1)

            if ret == True:
                bbox, shot = utils.findPose(frame)

                if isinstance(shot, tuple) and len(shot) == 2:
                    if bbox:
                        frame = utils.fancyDraw(frame, bbox, (0, 255, 0), shot=True)
                        cmd1, cmd2 = 0, 0
                        cmdInt = ''
                        res = ''

                        res = self.boundaryChecker(frame, shot)
                        mk_decision_result = self.mkDecision(frame, shot)
                        if mk_decision_result is not None:
                            cmd1, cmd2 = mk_decision_result
                        cmdInt = self.cmdInterpret(cmd1, cmd2)
                        # cmdInt = str(cmdInt1) + str(cmdInt2)

                    else:
                        res = "No obj"
                        cmdInt = ""
                else:
                    res = "No obj"
                    cmdInt = ""


                cTime = time.time()

                try:
                    X = w // 2 - shot[0]
                    Y = h // 2 - shot[1]

                    inf_time = cTime - pTime

                    fps = 1 / inf_time
                    frame = cv2.resize(frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), interpolation=cv2.INTER_LINEAR)
                    self.screen.blit(self.cvimage_to_pygame(frame), (0, 0))


                    if res is not None:
                        displayText_upper = [int(fps), "0.0166ms", trucate(inf_time,4),res]
                    else:
                        res = "No Obj"
                        displayText_upper = [int(fps), "0.0166ms", trucate(inf_time,4), res]
                    displayText_lower = [int(X), int(Y), cmdInt]
                    pTime = cTime
                    self.toolbar(displayText_upper, displayText_lower)

                except:
                    return 0

        else:
            print("Unable to find Camera")
            self.screen.fill((0, 0, 0))  # Fill the screen with black.
            self.toolbar()

        #pygame.display.flip()

    def cvimage_to_pygame(self,image):
        """Convert cvimage into a pygame image"""

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb = np.rot90(image_rgb)
        image_rgb_p = pygame.surfarray.make_surface(image_rgb).convert()
        image_rgb_p = pygame.transform.flip(image_rgb_p,True,False)
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
     aShooter = ArmyShooter(932,601)
     aShooter.runPyGame()
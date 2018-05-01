import pygame
import time
import socket
import json


class PadController(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self):

        self.initialize_pad()

        self.sock = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM   # UDP
        )

    def initialize_pad(self):
        '''
        find gamepad using pygame and initialize the first one found
        '''

        # ask pygame for joystick-stuff
        pygame.init()
        pygame.joystick.init()

        # find pads / joysticks
        pad_count = pygame.joystick.get_count()
        if pad_count != 1:
            raise StandardError('More or less than one pad / joystick found. Dying...')
        pad_index = pad_count - 1 # this will be 0...always...

        # initialize pad
        self.pad = pygame.joystick.Joystick(pad_index)
        self.pad.init()
        print('pad initialized')

    def run_gamepad(self):
        '''
        run robot in gamepad-mode. controll robot using generic x-box gamepad
        if u wanna use another gamepad, buttons and axes have to be reconfigured
        depending on your device
        '''

        done = False

        # main-loop to acquire joystick-events and react to them
        while not done:

            # get pygame-events first
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print 'buttton pressed'
                if event.type == pygame.JOYBUTTONUP:
                    print 'buttton released'

            # main buttons
            button_a = self.pad.get_button(0)
            button_b = self.pad.get_button(1)
            button_x = self.pad.get_button(2)
            button_y = self.pad.get_button(3)

            # initialize axes for movement
            front = self.pad.get_axis(4)
            turn = self.pad.get_axis(0)  # 1,2,3
            turn = round(turn, 2)  # no need to be exact here...
            front = round(front, 2)

            message = json.dumps({
                'forward': front,
                'turn': turn,
            })

            UDP_IP = "192.168.43.173"
            UDP_PORT = 14242
            # MESSAGE = "Hello, World!"

            self.sock.sendto(message, (UDP_IP, UDP_PORT))

            time.sleep(.5)
            print(turn, front)


if __name__ == '__main__':
    controller = PadController()
    controller.run_gamepad()

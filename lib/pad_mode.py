#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class PadMode(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self, robo):

        self.robo = robo
        self.initialize_pad()

    def initialize_pad(self):

        # ask pygame for joystick-stuff
        pygame.init()
        pygame.joystick.init()

        # find pads / joysticks
        pad_count = pygame.joystick.get_count()
        if pad_count != 1:
            raise StandardError('More than one pad / joystick found. Dying...')
        pad_index = pad_count - 1 # this will be 0...always...

        # initialize pad
        self.pad = pygame.joystick.Joystick(pad_index)
        self.pad.init()


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


            pad_count = pygame.joystick.get_count()

            if pad_count != 1:
                # maybe later do something more polite here...
                print 'more than one gamepad found...'
                print 'dunno whata do, closing....'
                return

            pad_index = pad_count - 1 # this will be 0...always...

            # initialize pad
            pad = pygame.joystick.Joystick(pad_index)
            pad.init()

            # main buttons
            button_a = pad.get_button(0)
            button_b = pad.get_button(1)
            button_x = pad.get_button(2)
            button_y = pad.get_button(3)

            # check buttons
            if button_a:
                if not self.player.playing_song:
                    thread.start_new_thread(self.player.play_song,())
            if button_b:
                self.fire_cannon()
            if button_x:
                if not self.running:
                    self.running = True
                    thread.start_new_thread(self.run,())
            if button_y:
                if self.running:
                    self.running = False

            # initialize axes for movement
            front = pad.get_axis(4)
            turn = pad.get_axis(3)
            turn = round(turn, 2) # no need to be exact here...
            front = round(front, 2)
            
            # check if movement has to be performed
            if not self.running:
                if front < -0.1:
                    robo.go_pad(power = -65 + 62 * front)
                if front > 0.1:
                    robo.go_pad(power = 65 + 62 * front)
                if turn < -0.2:
                    robo.turn_pad(power = -65 + 62 * turn)
                if turn > 0.2:
                    robo.turn_pad(power = 65 + 62 * turn)

                # stop robot if nothing is found
                if abs(front) < 0.1:
                    self.stop()
                    continue
                if abs(turn) < 0.1:
                    self.stop()
                    continue

    def go_pad(self, power=80):
        for motor in self.motors:
            motor.run(-power)

    def turn_pad(self, power=80):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)

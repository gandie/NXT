#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import thread

class PadController(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self, robo):

        self.robo = robo
        self.initialize_pad()

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

            # check buttons
            if button_a:
                if not self.robo.player.playing_song:
                    thread.start_new_thread(self.robo.player.play_song,())
            if button_b:
                if not self.robo.player.playing_song:
                    thread.start_new_thread(self.robo.player.play_song, ('schland',))
            '''
            if button_b:
                self.robo.fire_cannon()
            if button_x:
                if not self.robo.running:
                    self.robo.running = True
                    thread.start_new_thread(self.robo.run,())
            if button_y:
                if self.robo.running:
                    self.robo.running = False
            '''

            # initialize axes for movement
            front = self.pad.get_axis(4)
            turn = self.pad.get_axis(3)
            turn = round(turn, 2) # no need to be exact here...
            front = round(front, 2)

            # check if movement has to be performed
            #if not self.running:
            if front < -0.1:
                self.go_pad(power = -65 + 62 * front)
            if front > 0.1:
                self.go_pad(power = 65 + 62 * front)
            if turn < -0.2:
                self.turn_pad(power = -65 + 62 * turn)
            if turn > 0.2:
                self.turn_pad(power = 65 + 62 * turn)

            # stop robot if nothing is found
            if abs(front) < 0.1:
                self.robo.stop()
            if abs(turn) < 0.1:
                self.robo.stop()

    def go_pad(self, power=80):
        for motor in self.robo.motors:
            motor.run(-power)

    def turn_pad(self, power=80):
        for motor in self.robo.motors:
            if motor == self.robo.motor_left:
                motor.run(power)
            elif motor == self.robo.motor_right:
                motor.run(-power)

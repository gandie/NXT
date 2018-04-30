#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import thread
import time

class PadController(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self, robo):

        self.robo = robo
        self.initialize_pad()
        self.curdir = 0

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

        self.calibrate()

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
            turn = self.pad.get_axis(0)  # 1,2,3
            turn = round(turn, 2) # no need to be exact here...
            front = round(front, 2)
            # print(turn, front)
            # check if movement has to be performed
            #if not self.running:
            if front < -0.1:
                self.go_pad(power=(-60 + 67 * front))
            if front > 0.1:
                self.go_pad(power=(60 + 67 * front))
            '''
            if turn < -0.2:
                self.turn_pad(1, 50)
            if turn > 0.2:
                self.turn_pad(-1, 50)
            '''
            # print(turn)
            # tacho = self.robo.steering_motor.get_tacho()
            # print(tacho)

            # stop robot if nothing is found
            if abs(front) < 0.1:
                self.robo.stop()
            if abs(turn) < 0.1:

                tacho = self.robo.steering_motor.get_tacho()
                tacho_cur = tacho.tacho_count
                tacho_diff = self.tacho_middle - tacho_cur
                if tacho_diff > 0:
                    self.robo.steering_motor.turn(power=90, tacho_units=tacho_diff)
                elif tacho_diff < 0:
                    self.robo.steering_motor.turn(power=-90, tacho_units=-tacho_diff)
            else:
                tacho = self.robo.steering_motor.get_tacho()
                tacho_cur = tacho.tacho_count
                tacho_desired = self.tacho_middle + turn * abs(self.steering_interval) * 0.5
                # print(tacho_desired)
                tacho_diff = tacho_cur - tacho_desired
                print(turn, tacho_diff)
                if tacho_diff < 0:
                    self.robo.steering_motor.turn(power=90, tacho_units=-tacho_diff)
                elif tacho_diff > 0:
                    self.robo.steering_motor.turn(power=-90, tacho_units=tacho_diff)
                '''
                '''
                '''
                if self.curdir != 0:
                    direction = -self.curdir
                    self.robo.steering_motor.turn(power=70*direction, tacho_units=75)
                    self.curdir = 0
                '''

                # pass
                # self.robo.steering_motor.turn(power=80, tacho_units=)
                # self.robo.stop()
            self.robo.steering_motor.brake()

    def calibrate(self):
        print('calibrating...')
        direction = 1
        self.robo.steering_motor.run(power=direction * 60)
        time.sleep(10)
        self.robo.steering_motor.brake()
        tacho = self.robo.steering_motor.get_tacho()
        tacho_one = tacho.tacho_count
        self.max_left = tacho_one
        print('left max', tacho_one)
        direction = -1
        self.robo.steering_motor.run(power=direction * 60)
        time.sleep(10)
        self.robo.steering_motor.brake()
        tacho = self.robo.steering_motor.get_tacho()
        tacho_two = tacho.tacho_count
        self.max_right = tacho_two
        print('max right', tacho_two)
        interval = tacho_one - tacho_two
        self.steering_interval = interval / 2
        middle = interval / 2
        self.tacho_middle = tacho_two + middle
        for i in range(5):
            tacho = self.robo.steering_motor.get_tacho()
            tacho_cur = tacho.tacho_count
            tacho_diff = self.tacho_middle - tacho_cur
            if tacho_diff > 0:
                self.robo.steering_motor.turn(power=50, tacho_units=tacho_diff)
                time.sleep(1)
            elif tacho_diff < 0:
                self.robo.steering_motor.turn(power=-50, tacho_units=-tacho_diff)
                time.sleep(1)

        tacho = self.robo.steering_motor.get_tacho()
        tacho_middle_now = tacho.tacho_count
        self.robo.steering_motor.idle()
        print('calibration done', tacho_one, tacho_two, self.tacho_middle, tacho_middle_now)

    def go_pad(self, power=80):
        print(power)
        for motor in self.robo.motors:
            motor.run(power)

    def turn_pad(self, direction, turn):
        self.robo.steering_motor.run(85*direction)
        # self.robo.steering_motor.turn(power=70*direction, tacho_units=50)
        self.curdir = direction
        '''
        for motor in self.robo.motors:
            if motor == self.robo.motor_left:
                motor.run(power)
            elif motor == self.robo.motor_right:
                motor.run(-power)
        '''

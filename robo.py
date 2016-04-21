#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nxt.locator
import thread
from nxt.motor import *
from nxt.sensor import *

import thread
import threading
import time

import random

import sys

import pygame

from lib.nxt_player import Nxt_Player

class ScoutRobo(object):

    '''
    ScoutRobo is a python class to control a lego-nxt robot by using bluetooth
    or usb connection.
    '''

    def __init__(self, bluetooth_only = True):

        '''
        initialize robot. by default robot is found using bluetooth,
        remember to install bluetooth lib before usage!
        '''

        # find brick
        if bluetooth_only:
            find_brick_method = nxt.locator.Method(usb = False, bluetooth = True)
        else:
            find_brick_method = nxt.locator.Method()

        self.brick = nxt.locator.find_one_brick(method = find_brick_method)

        # initialize motors
        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)
        self.motors = [self.motor_left, self.motor_right]
        self.cannon = Motor(self.brick, PORT_C)

        # initialize sensors
        self.sensor_ultrasonic = Ultrasonic(self.brick, PORT_3)
        self.sensor_touch_left = Touch(self.brick, PORT_2)
        self.sensor_touch_right = Touch(self.brick, PORT_1)
        #self.sensor_light_color = Light(self.brick, PORT_4)

        # initialize music
        self.player = Nxt_Player(self.brick)

        # initialize some vars used for auto-pilot
        self.touch_right = False
        self.touch_left = False
        self.transitions = []
        self.running = False
        self.curr_time = time.time()

        # limits used by check_transitions
        self.transition_count = 3
        self.transition_time = 10

    def test(self):
        '''
        use this to test new functions n' shit
        '''
        print 'testing...'
        self.player.play_song()

    def run_gamepad(self):
        '''
        run robot in gamepad-mode. controll robot using generic x-box gamepad
        if u wanna use another gamepad, buttons and axes have to be reconfigured
        depending on your device
        '''

        # ask pygame for joystick-stuff
        pygame.init()
        pygame.joystick.init()

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


    def run(self, init_state = 'normal'):
        '''
        auto-pilot mode, driving arround, scouting area
        TODO: implement navigation-voodoo
        '''

        self.state = init_state

        # main loop
        while self.running:

            # get sensor data
            self.touch_left = self.sensor_touch_left.get_sample()
            self.touch_right = self.sensor_touch_right.get_sample()
            self.distance = self.sensor_ultrasonic.get_sample()

            self.curr_time = time.time()
            self.check_transitions()

            # check if imperial march has to be played ;-)
            if not self.player.playing_song:
                number = random.randint(0, 400)
                if number == 88:
                    thread.start_new_thread(self.player.play_song,())

            # basic FSM from here...
            if self.state == 'normal':
                self.go_forward_forever()
                
                if self.touch_left:
                    self.state = 'touch_left'
                if self.touch_right:
                    self.state = 'touch_right'
                if self.distance < 8:
                    self.state = 'front'

            elif self.state == 'front':
                self.stop()
                self.transitions.append(('front', time.time()))
                self.go_backward(ftime = 1.5)
                # turn randomly if front sensor was triggered
                if random.randint(0, 1):
                    self.turn_right(ftime = 0.4)
                else:
                    self.turn_left(ftime = 0.4)
                self.state = 'normal'
                
            elif self.state == 'touch_left':
                self.stop()
                self.transitions.append(('touch_left', time.time()))
                self.go_backward(ftime = 1)
                self.turn_right(ftime = 0.4)
                self.state = 'normal'

            elif self.state == 'touch_right':
                self.stop()
                self.transitions.append(('touch_right', time.time()))
                self.go_backward(ftime = 1)
                self.turn_left(ftime = 0.4)
                self.state = 'normal'

        self.stop()


    def check_transitions(self):

        counter = 0

        '''
        # do not flush transitions, rather keep them for evaluation

        # check if latest transition if older than 10 seconds
        if self.transitions:
            last_trans = self.transitions[-1]
            diff = self.curr_time - last_trans[1] 
            if diff > self.transition_time:
                # flush transitions if last one is older
                self.transitions = []
                return
        '''

        # count transitions in last 10 seconds
        for trans in self.transitions:
            trans_time = trans[1]
            diff = self.curr_time - trans_time
            if diff < self.transition_time:
                counter += 1

        # lots of transitions found, cry for help...
        if counter > self.transition_count:
            print 'CRYING FOR HELP NOW!!!'
            self.transitions = []
            self.running = False

    def go_forward_forever(self, power = 80):
        for motor in self.motors:
            motor.run(power)

    def go_backward_forever(self, power = 80):
        for motor in self.motors:
            motor.run(-power)

    def stop(self):
        self.get_data = False
        for motor in self.motors:
            motor.idle()

    def go_pad(self, power=80):
        for motor in self.motors:
            motor.run(-power)

    def turn_pad(self, power=80):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)

    def go_forward(self, power=80, ftime=1):
        for motor in self.motors:
            motor.run(power)
        time.sleep(ftime)
        for motor in self.motors:
            motor.idle()

    def go_backward(self, power=80, ftime=1):
        for motor in self.motors:
            motor.run(-power)
        time.sleep(ftime)
        for motor in self.motors:
            motor.idle()

    def turn_left(self, power=80, ftime=1):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(-power)
            elif motor == self.motor_right:
                motor.run(power)
        time.sleep(ftime)
        for motor in self.motors:
            motor.idle()

    def turn_right(self, power=80, ftime=1):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)
        time.sleep(ftime)
        for motor in self.motors:
            motor.idle()

    def fire_cannon(self, balls=1):
        self.cannon.turn(127,360*balls)
        self.cannon.idle() # changed this to idle to make cannon movable

if __name__ == '__main__':
    robo = ScoutRobo()
    #robo.test()
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = None
    if mode == 'run':
        try:
            robo.run()
        except Exception as e:
            print e
            print 'run-mode died'
            robo.stop()
    elif mode == 'test':
        robo.test()
    elif mode == 'pad':
        try:
            robo.run_gamepad()
        except Exception as e:
            print e
            print 'pad-mode died...'
            robo.stop()

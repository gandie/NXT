#!/usr/bin/env python

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

class ScoutRobo(object):

    def __init__(self):
        self.brick = nxt.locator.find_one_brick()

        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)
        self.motors = [self.motor_left, self.motor_right]

        self.cannon = Motor(self.brick, PORT_C)

        self.sensor_ultrasonic = Ultrasonic(self.brick, PORT_3)
        self.sensor_touch_left = Touch(self.brick, PORT_2)
        self.sensor_touch_right = Touch(self.brick, PORT_1)
        #self.sensor_light_color = Light(self.brick, PORT_4)

        self.touch_right = False
        self.touch_left = False

        self.transitions = []

        self.running = False

        self.playing_march = False

        self.curr_time = time.time()

        self.freqs = {            
            'A0' : 220,
            'B0' : 233,
            'H0' : 247,
            'C0' : 262,
            'CIS0' : 277,
            'D0' : 294,
            'DIS0' : 311,
            'E0' : 330,
            'F0' : 349,
            'FIS0' : 370,
            'G0' : 392,
            'GIS0' : 415,
            'A1' : 440,
            'B1' : 466,
            'H1' : 494,
            'C1' : 523,
            'CIS1' : 554,
            'D1' : 587,
            'DIS1' : 622,
            'E1' : 659,
            'F1' : 698,
            'FIS1' : 740,
            'G1' : 784,
            'GIS1' : 831,
            'A2' : 880,
            'B2' : 932,
            'H2' : 988,
            'C2' : 1047,
            'CIS2' : 1109,
            'D2' : 1175,
            'DIS2' : 1245,
            'E2' : 1319,
            'F2' : 1397,
            'FIS2' : 1480,
            'G2' : 1568,
            'GIS2' : 1661,
            'A3' : 1760,
            'B3' : 1865,
            'H3' : 1976,
            'C3' : 2093,
            'CIS3' : 2217,
            'D3' : 2349,
            'DIS3' : 2489,
            'E3' : 2637,
            'F3' : 2794,
            'FIS3' : 2960,
            'G3' : 3136,
            'GIS3' : 3322
        }

    def test(self):
        #self.play_all_notes()
        self.play_march()
        self.play_schland()


    def run_gamepad(self):
        pygame.init()

        pygame.joystick.init()

        done = False
        while not done:
            print 'pad-mode...'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print 'buttton pressed'
                if event.type == pygame.JOYBUTTONUP:
                    print 'buttton released'
            pad_count = pygame.joystick.get_count()
            for i in range(pad_count):
                pad = pygame.joystick.Joystick(i)
                pad.init()

                button_a = pad.get_button(0)
                button_b = pad.get_button(1)
                button_x = pad.get_button(2)
                button_y = pad.get_button(3)
                print button_a

                if button_a:
                    if not self.playing_march:
                        thread.start_new_thread(self.play_march,())
                if button_b:
                    self.fire_cannon()
                if button_x:
                    print 'button_x'
                    if not self.running:
                        self.running = True
                        thread.start_new_thread(self.run,())
                if button_y:
                    if self.running:
                        self.running = False


                front = pad.get_axis(4)
                turn = pad.get_axis(3)
                turn = round(turn, 2)
                front = round(front, 2)

                print turn, front

                if not self.running:
                    if front < -0.1:
                        #robo.go_forward(ftime = 0.2)
                        robo.go_pad(power = -65 + 62 * front)
                    if front > 0.1:
                        #robo.go_backward(ftime = 0.2)
                        robo.go_pad(power = 65 + 62 * front)
                    if turn < -0.2:
                        #robo.turn_left(ftime = 0.2)
                        robo.turn_pad(power = -65 + 62 * turn)
                    if turn > 0.2:
                        robo.turn_pad(power = 65 + 62 * turn)
                        #robo.turn_right(ftime = 0.2)

                    if abs(front) < 0.1:
                        self.stop()
                        continue
                    if abs(turn) < 0.1:
                        self.stop()
                        continue


    def run(self):
        '''
        self.t_left_thread = threading.Thread(
            target = self.get_touch_left,
            args = (0.1,)
        )
        self.t_left_thread.start()
        '''
        #thread.start_new_thread(self.play_march,())
        self.state = 'normal'

        # main loop
        while self.running:

            # get sensor data
            self.touch_left = self.sensor_touch_left.get_sample()
            self.touch_right = self.sensor_touch_right.get_sample()

            self.distance = self.sensor_ultrasonic.get_sample()

            #print self.distance
            print self.motor_left.get_tacho()
            print self.motor_right.get_tacho()

            self.curr_time = time.time()

            self.check_transitions()

            if not self.playing_march:
                number = random.randint(0, 400)
                if number == 88:
                    print 'playing march now...'
                    #thread.start_new_thread(self.play_march,())

            if self.state == 'normal':
                self.go_forward_forever()
                
                if self.touch_left:
                    print 'left'
                    self.state = 'touch_left'
                if self.touch_right:
                    print 'right'
                    self.state = 'touch_right'
                if self.distance < 8:
                    print 'front'
                    self.state = 'front'

            elif self.state == 'front':
                self.stop()
                self.transitions.append(('front', time.time()))
                self.go_backward(ftime = 1.5)
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



            #print 'Running in {} state...'.format(self.state)
        self.stop()


    def check_transitions(self):

        counter = 0

        # check if latest transition if older than 10 seconds
        if self.transitions:
            last_trans = self.transitions[-1]
            diff = self.curr_time - last_trans[1] 
            if diff > 10:
                self.transitions = []
                return

        # count transitions in last 10 seconds
        for trans in self.transitions:
            trans_time = trans[1]
            diff = self.curr_time - trans_time
            if diff < 10:
                counter += 1

        # lots of transitions found, cry for help...
        if counter > 3:
            print 'CRYING FOR HELP NOW!!!'
            self.play_schland()
            self.transitions = []
            self.running = False

    def go_forward_forever(self, power = 80):
        for motor in self.motors:
            motor.run(power)

    def go_backward_forever(self, power = 80):
        for motor in self.motors:
            motor.run(-power)

    def turn_left_forever(self, power=80, ftime=1):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(-power)
            elif motor == self.motor_right:
                motor.run(power)

    def turn_right_forever(self, power=80, ftime=1):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)

    def stop(self):
        self.get_data = False
        for motor in self.motors:
            motor.idle()

    def play_all_notes(self, v = 50, times = 1):
        #alle toene
        for i in range(times):
            self.brick.play_tone_and_wait(self.freqs['A0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['CIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['E0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['F0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['CIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['CIS2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['E2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['F2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['CIS3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['E3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['F3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G3'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS3'], 4*v)

    def play_march(self, v = 150, times = 1):
        self.playing_march = True
        for i in range(times):
            self.brick.play_tone_and_wait(self.freqs['G0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['G0'] , 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            self.brick.play_tone_and_wait(self.freqs['G0'] , 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['D1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['D1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS1'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['H1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['FIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['H1'], v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS1'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['E1'], v)
            self.brick.play_tone_and_wait(self.freqs['DIS1'], v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS0'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['CIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['H1'], v)
        
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            self.brick.play_tone_and_wait(self.freqs['A1'], v)
            self.brick.play_tone_and_wait(self.freqs['B1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['FIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['FIS0'], v)
            
            self.brick.play_tone_and_wait(self.freqs['B1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            self.brick.play_tone_and_wait(self.freqs['D1'], 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['G0'], v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['FIS1'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['E1'], v)
            self.brick.play_tone_and_wait(self.freqs['DIS1'], v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['GIS0'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['CIS1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['H1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            self.brick.play_tone_and_wait(self.freqs['A1'], v)
            self.brick.play_tone_and_wait(self.freqs['B1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['FIS0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            
            self.brick.play_tone_and_wait(self.freqs['G0'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['DIS0'], 3*v)
            self.brick.play_tone_and_wait(self.freqs['B1'], v)
            self.brick.play_tone_and_wait(self.freqs['G0'], 8*v)

        self.playing_march = False

    def play_schland(self, v = 150, times = 1):
        #schland
        for i in range(times):
            self.brick.play_tone_and_wait(self.freqs['F1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['D2'], 4*v)      
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['F1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['F1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['D2'], 4*v)      
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['F1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)      
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)      
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)      
            self.brick.play_tone_and_wait(self.freqs['A2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)
            
            self.brick.play_tone_and_wait(self.freqs['H2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)
            
            self.brick.play_tone_and_wait(self.freqs['G2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['E2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['E2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['D2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['D2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            
            self.brick.play_tone_and_wait(self.freqs['G1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], v)      
            self.brick.play_tone_and_wait(self.freqs['B2'], v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['D2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)

            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)      
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 8*v)

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
        self.cannon.brake()

    def get_distance(self, ftime):
        while True:
            sensor = self.sensor_ultrasonic
            self.distance = sensor.get_sample()
            print 'distance = {}'.format(self.distance)
            time.sleep(ftime)

    def get_touch_right(self, ftime):
        while self.get_data:
            sensor = self.sensor_touch_right
            self.touch_right = sensor.get_sample()
            time.sleep(ftime)

    def get_touch_left(self, ftime):
        while self.get_data:
            sensor = self.sensor_touch_left
            self.touch_left = sensor.get_sample()
            time.sleep(ftime)

    def get_light(self, ftime):
        while True:
            sensor = self.sensor_light_color
            self.light = sensor.get_sample()
            time.sleep(ftime)


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
        except:
            print 'i died'
            robo.stop()
    elif mode == 'test':
        robo.test()
    elif mode == 'pad':
        try:
            robo.run_gamepad()
        except:
            print 'pad-mode died...'
            robo.stop()

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

class ScoutRobo(object):

    def __init__(self):
        self.brick = nxt.locator.find_one_brick()

        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)
        self.motors = [self.motor_left, self.motor_right]

        self.cannon = Motor(self.brick, PORT_C)

        #self.sensor_ultrasonic = Ultrasonic(self.brick, PORT_3)
        self.sensor_touch_left = Touch(self.brick, PORT_2)
        self.sensor_touch_right = Touch(self.brick, PORT_1)
        #self.sensor_light_color = Light(self.brick, PORT_4)

        self.touch_right = False
        self.touch_left = False

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

    def run(self):
        '''
        self.t_left_thread = threading.Thread(
            target = self.get_touch_left,
            args = (0.1,)
        )
        self.t_left_thread.start()

        self.t_right_thread = threading.Thread(
            target = self.get_touch_right,
            args = (0.1,)
        )
        self.t_right_thread.start()
        '''
        #thread.start_new_thread(self.get_touch_left,(0.1,))
        #thread.start_new_thread(self.get_touch_right,(0.1,))
        thread.start_new_thread(self.play_march,())
        #thread.start_new_thread(self.get_light,(0.1,))
        self.state = 'normal'
        self.curr_takt = 1
        seconds = 10
        ctime = 0
        while True:
            self.touch_left = self.sensor_touch_left.get_sample()
            self.touch_right = self.sensor_touch_right.get_sample()
            #ctime += 0.5
            if ctime > seconds:
                break
            if self.state == 'normal':
                self.go_forward_forever()
                
                if self.touch_left:
                    print 'left'
                    self.state = 'touch_left'
                if self.touch_right:
                    print 'right'
                    self.state = 'touch_right'
                
            elif self.state == 'touch_left':
                self.stop()
                self.go_backward(ftime = 1)
                self.turn_right(ftime = 0.4)
                self.state = 'normal'
            elif self.state == 'touch_right':
                self.stop()
                self.go_backward(ftime = 1)
                self.turn_left(ftime = 0.4)
                self.state = 'normal'
            #print self.state
            #time.sleep(0.5)
            print 'Running in {} state...'.format(self.state)
        self.stop()


    def go_forward_forever(self, power = 80):
        for motor in self.motors:
            motor.run(power)

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
    if mode == 'run':
        try:
            robo.run()
        except:
            print 'i died'
            robo.stop()
    elif mode == 'test':
        robo.test()

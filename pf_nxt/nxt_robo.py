#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nxt.motor import *
from nxt.sensor import *
from nxt.bluesock import BlueSock

import time

from pf_nxt.nxt_player import Nxt_Player
from pf_nxt.nxt_pad import PadController
from pf_nxt.nxt_autopilot import AutoPilot
from pf_nxt.nxt_pair import Pair


class ScoutRobo(object):
    '''
    ScoutRobo is a python class to control a lego-nxt robot by using bluetooth
    or usb connection.
    '''

    def __init__(self, baddr, pin, cannon=False):
        '''
        initialize robot. by default robot is found using bluetooth,
        remember to install bluetooth lib before usage!
        :param baddr: The bluetooth mac address
        :param pin: The pin to ensure the connection
        '''

        # get config from keyword-arguments, default-value after comma
        self.cannon = cannon

        # Pair with nxt via bluetooth
        self.stable_connection = Pair(baddr, pin)

        # Connect to nxt via bluetooth
        self.brick = BlueSock(baddr).connect()

        # initialize basic functions
        self.init_motors()
        self.init_sensors()

        # initialize some useful vars
        self.touch_right = False
        self.touch_left = False

        # locked is used to stop robo from moving when it has collided
        # getting orders from http-server
        self.locked = False

        # player for beeps and stuff
        self.player = Nxt_Player(self.brick)

        # Initialize pad and autopilto modules
        self.pad_controller = PadController(self)
        self.autopilot = AutoPilot(self)

    def init_motors(self):
        '''
        find and initialize motors from ports of brick
        '''

        self.motors = [
            Motor(self.brick, PORT_A),
            # Motor(self.brick, PORT_B)
        ]

        self.steering_motor = Motor(self.brick, PORT_C)
        self.steering_motor.brake()
        '''
        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)

        # put main motors into list for driving
        self.motors = [self.motor_left, self.motor_right]

        # cannon is not in use for normal setup right now
        if self.cannon:
            # crashes if no motor is connected to port_c!
            self.cannon_motor = Motor(self.brick, PORT_C)
        '''

    def init_sensors(self):
        '''
        find and initialize sensors from ports of brick
        useful sensors: 'touch_left', 'touch_right', 'light_color', 'ultrasonic'
        '''

        # map sensor names against driver class and port plugged in robot for
        # safe initialization
        SENSOR_MAP = {
            "touch_left": (Touch, PORT_2),
            "touch_right": (Touch, PORT_1),
            "light_color": (Color20, PORT_3),  # unable to false-detect this one
            "ultrasonic": (Ultrasonic, PORT_4),
        }

        self.sensors = {}
        for sensor_name, sensor in SENSOR_MAP.items():
            sensor_class, port = sensor
            try:
                sensor_instance = sensor_class(self.brick, port)
                sensor_instance.get_sample()
            except Exception:
                print('Init sensor %s on port %s failed.' % (sensor_name, port))
                print('Are you sure its plugged in?')  # Have u tried turning it off and on again?
                continue
            self.sensors[sensor_name] = sensor_instance

    def keep_alive(self):
        '''
        Keeps robot connection alive so it won't turn off automatically after
        time. It will come to weird errors if the robot turns off while the
        server is running. Only option is to terminate the process then.
        Don't even know if this is working, just a theory
        '''
        self.brick.sock.send("DD!")

    def get_telemetry(self):
        '''
        method to acquire sensor data, called e.g. by external modules
        '''

        # Fancy oneliner to create a new dictionary with old keys but new values
        telemetry = {k: v.get_sample() for k, v in self.sensors.items()}

        return telemetry

    def check_color(self):
        '''
        check if underground has white color (= 6)
        '''
        # TODO: check docs and write / use dictionary mapping color codes
        if self.sensors.get("light_color"):
            val = self.sensors["light_color"].get_sample()
            if val == 5:
                return True
            else:
                return False
        else:
            return False

    def check_collision(self):
        '''
        check touch and ultrasonic sensors to detect collisions
        '''
        if self.sensors.get("touch_left") and self.sensors.get("touch_right"):
            self.touch_left = self.sensors["touch_left"].get_sample()
            self.touch_right = self.sensors["touch_right"].get_sample()

            if self.touch_left or self.touch_right:
                return True

        # also check ultrasonic here, its useful if robo drives straight
        # forward towards a wall, so touch sensors cant detect collision
        if self.sensors.get("ultrasonic"):
            self.distance = self.sensors["ultrasonic"].get_sample()
            # TODO: magic number --> config file!
            if self.distance < 6:
                return True

        return False

    def timed_checks(self, ftime):
        '''
        timed collision and color checks done while robo is moving
        '''

        # count times color sensor detects goal color
        color_times = 0

        # color sensor can be a little fuzzy, so one detection does not
        # necessarily mean "goal reached"
        color_times_limit = 3

        # TODO: reset counter after certain amount of time!

        start = time.time()
        while True:
            now = time.time()
            if (now - start) > ftime:
                break
            if self.check_collision():
                self.stop()
                if not self.player.playing_song:
                    self.player.play_song('fail')
                # self.locked = True
                break
            if self.check_color():
                color_times += 1
                if color_times > color_times_limit:
                    self.stop()
                    if not self.player.playing_song:
                        self.player.play_song('success')
                    # self.locked = True
                    break
        return

    def unlock(self):
        '''
        robo is locked when it collides. unlock is called by nxt-control app
        '''
        self.locked = False

    def go_forward_forever(self, power=80):
        for motor in self.motors:
            motor.run(power)

    def go_backward_forever(self, power=80):
        for motor in self.motors:
            motor.run(-power)

    def stop(self):
        for motor in self.motors:
            motor.idle()
        # self.steering_motor.reset_position(True)
        '''
        tacho = self.steering_motor.get_tacho()
        count = tacho.tacho_count
        print(tacho)
        if abs(count) > 0:
            self.steering_motor.turn(power=80* -(count/-count), tacho_units=1)
        '''
        # self.steering_motor.brake()

    def go_forward(self, power=80, ftime=1):
        if self.locked:
            return
        for motor in self.motors:
            motor.run(power)

        self.timed_checks(ftime)

        for motor in self.motors:
            motor.idle()

    def go_backward(self, power=80, ftime=1):
        if self.locked:
            return
        for motor in self.motors:
            motor.run(-power)

        self.timed_checks(ftime)

        for motor in self.motors:
            motor.idle()

    def turn_left(self, power=80, ftime=1):
        if self.locked:
            return
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(-power)
            elif motor == self.motor_right:
                motor.run(power)

        self.timed_checks(ftime)

        for motor in self.motors:
            motor.idle()

    def turn_right(self, power=80, ftime=1):
        if self.locked:
            return
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)

        self.timed_checks(ftime)

        for motor in self.motors:
            motor.idle()

    def turn_right_forever(self, power=80):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(power)
            elif motor == self.motor_right:
                motor.run(-power)

    def turn_left_forever(self, power=80):
        for motor in self.motors:
            if motor == self.motor_left:
                motor.run(-power)
            elif motor == self.motor_right:
                motor.run(power)

    def fire_cannon(self, balls=1):
        self.cannon_motor.turn(127, 360 * balls)
        self.cannon_motor.idle()
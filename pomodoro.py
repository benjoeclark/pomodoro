#!/usr/bin/env python

import time
import threading
import sys

class DisplayThread(threading.Thread):
    def __init__(self, pomodoro):
        self.pomodoro = pomodoro
        threading.Thread.__init__(self)

    def run(self):
        while len(self.pomodoro.states[-1]) > 0:
            print '\n' + self.pomodoro.states[-1].displayString[:self.pomodoro.states[-1].blit],
            sys.stdout.flush()
            self.pomodoro.nextState(self.pomodoro.states[-1].update())
            time.sleep(1)

class InputThread(threading.Thread):
    def __init__(self, pomodoro):
        self.pomodoro = pomodoro
        threading.Thread.__init__(self)

    def run(self):
        while len(self.pomodoro.states[-1]) > 0:
            command = raw_input()
            self.pomodoro.handleCommand(command)
        

class State(object):
    def initialize(self, timeInterval=25, timeStep=10, displayString='.'*50):
        self.timeInterval = timeInterval
        self.timeStep = timeStep
        self.displayString = displayString
        self.runningTime = 0
        self.blit = 0

    def update(self):
        self.blit = (self.blit + 1) % len(self.displayString)
        self.runningTime += 1
        self.blit = (self.runningTime / self.timeStep) % len(self.displayString)
        if self.runningTime < self.timeInterval:
            return self
        else:
            return self.nextState

class Timing(State):
    def __init__(self, timeInterval=25):
        self.nextState = Alarm()
        self.initialize(timeInterval)

class Alarm(State):
    def __init__(self):
        self.nextState = None
        self.initialize(5, 1, '*'*10)

class Pomodoro(object):
    def __init__(self, timeInterval=25, filename='log'):
        self.log = open(filename, 'a')
        self.states = [Timing(timeInterval)]
        DisplayThread(self).start()
        InputThread(self).start()

    def handleCommand(self, command):
        self.log.write(command + '\n')
        if command == 'exit':
            self.nextState(None)

    def nextState(self, state):
        if state is None:
            self.states.pop()
        if state is not self.states[-1]:
            self.log.write(str(self.states[-1].__class__))
            self.log.write(str(state.__class__))
            self.states = [state]


def main():
    pomodoro = Pomodoro()

if __name__ == '__main__':
    main()

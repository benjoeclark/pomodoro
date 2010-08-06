#!/usr/bin/env python

import time
import sys

class State(object):
    def initialize(self, timeInterval=25, timeStep=1., blitLength=70):
        self.timeInterval = timeInterval
        self.timeStep = timeStep
        self.blitLength = blitLength
        self.blit = 0

    def update(self):
        self.blit += 1
        print
        print '*' * (self.blit % self.blitLength),
        sys.stdout.flush()
        time.sleep(self.timeStep * 60.)
        if self.blit < self.timeInterval/self.timeStep:
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
        self.initialize(5, 1./120., 10)

class Pomodoro(object):
    def __init__(self, timeInterval=25.):
        self.state = Timing(timeInterval)
        self.run()

    def run(self):
        while self.state is not None:
            self.state = self.state.update()


def main():
    pomodoro = Pomodoro()

if __name__ == '__main__':
    main()

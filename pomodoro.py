#!/usr/bin/env python

import time
import threading
import sys

class DisplayThread(threading.Thread):
    def __init__(self, pomodoro):
        self.pomodoro = pomodoro
        threading.Thread.__init__(self)

    def run(self):
        while self.pomodoro.running:
            print '\n' + self.pomodoro.getString(),
            sys.stdout.flush()
            time.sleep(1)

class InputThread(threading.Thread):
    def __init__(self, pomodoro):
        self.pomodoro = pomodoro
        threading.Thread.__init__(self)

    def run(self):
        while self.pomodoro.running:
            command = raw_input()
            self.pomodoro.handleCommand(command)

class Pomodoro(object):
    def __init__(self, timeInterval=25*60, filename='timer.log'):
        self.log = open(filename, 'a')
        self.running = True
        self.timeInterval = timeInterval
        self.paused = False
        self.alarm = False
        self.displayString = '.'*50
        self.blit = 0
        self.blitStep = 60
        self.time = 0
        DisplayThread(self).start()
        InputThread(self).start()

    def getString(self):
        if self.alarm:
            self.blit = (self.blit + 1) % 10
            return '*' * self.blit
        if self.paused:
            self.blit = (self.blit + 1) % len('paused')
            return 'paused'[:self.blit+1]
        self.time += 1
        self.blit = (self.time / self.blitStep) % len(self.displayString)
        if self.time >= self.timeInterval:
            self.alarm = True
            if not self.log.closed:
                self.log.write(time.asctime() + '>' + str(self.timeInterval) + '\n')
        return self.displayString[:self.blit+1]

    def handleCommand(self, command):
        if self.alarm:
            self.alarm = False
            self.time = 0
        elif command == 'a':
            self.alarm = True
        elif command == 'p' or command == 'pause':
            if not self.paused:
                self.blit = 0
            self.paused = not self.paused
        elif command == 'exit':
            self.running = False
            self.log.close()

def main():
    pomodoro = Pomodoro()

if __name__ == '__main__':
    main()

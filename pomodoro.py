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
    def __init__(self, description='', timeInterval=25*60, filename='timer.log'):
        self.description = description
        self.log = filename
        self.running = True
        self.timeInterval = timeInterval
        self.paused = False
        self.alarm = False
        self.displayString = ('.'*50).replace('.....', '....,')
        self.blit = 0
        self.blitStep = 60
        self.time = 0
        self.alarmTime = 0
        DisplayThread(self).start()
        InputThread(self).start()

    def getString(self):
        if self.alarm:
            self.alarmTime += 1
            self.blit = (self.blit + 1) % 10
            return str(self.alarmTime // 60) + '*' * self.blit
        if self.paused:
            self.blit = (self.blit + 1) % len('paused')
            return 'paused'[:self.blit+1]
        self.time += 1
        self.blit = (self.time / self.blitStep) % len(self.displayString)
        if self.time >= self.timeInterval:
            self.alarm = True
            log = open(self.log, 'a')
            if not log.closed:
                log.write(time.asctime() + '>' + str(self.timeInterval))
                log.write(' ' + self.description + '\n')
            log.close()
        return self.description + self.displayString[:self.blit+1]

    def handleCommand(self, command):
        if self.alarm:
            self.alarm = False
            self.time = 0
            self.running = False
        elif command == 'a':
            self.alarm = True
        elif command == 'p' or command == 'pause':
            if not self.paused:
                self.blit = 0
            self.paused = not self.paused
        elif command == 'exit':
            self.running = False

def main():
    pomodoro = Pomodoro(sys.argv[-1])

if __name__ == '__main__':
    main()

import pyperclip as ppc
import sys, select
from time import sleep
import time

#pyperclip.copy('The text to be copied to the clipboard.')
#print(pyperclip.paste())

import sys
import selectors
import termios


DEFAULT_TIMEOUT = 5.0
INTERVAL = 0.05

SP = ' '
CR = '\r'
LF = '\n'
CRLF = CR + LF

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TimeoutOccurred(Exception):
    pass


def echo(string):
    sys.stdout.write(string)
    sys.stdout.flush()


def posix_inputimeout(prompt='', timeout=DEFAULT_TIMEOUT):
    echo(prompt)
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    events = sel.select(timeout)

    if events:
        key, _ = events[0]
        return key.fileobj.readline().rstrip(LF)
    else:
        #echo(LF)
        #termios.tcflush(sys.stdin, termios.TCIFLUSH)
        #raise TimeoutOccurred
        pass

def cprint(text, colorcode):
    print(colorcode + text + bcolors.ENDC)

inputimeout = posix_inputimeout

history = []
i = 0
t_old = None
t = None
current = ppc.paste()
history.append(current)
cprint(f"{i} --> {current}", bcolors.OKBLUE)
while True:
    if current != ppc.paste():
        current = ppc.paste()
        history.append(current)
        i += 1

        mlen = len(current) if len(current) < 25 else 25
        cprint(f"{i} --> {current[:mlen]}", bcolors.OKBLUE)


    t = inputimeout(prompt='', timeout=1)
    
    if t:
        if t == "ls":
            for k, c in enumerate(history):
                mlen = len(c) if len(c) < 25 else 25
                cprint(f"{k} --> {c[:mlen]}", bcolors.OKBLUE)
        elif len(t) < 4: 
            t = int(t)
            ppc.copy(history[t])
            print(f"coppied {t} --> {history[t]}")
            current = ppc.paste()
            t = None
    else:
        pass

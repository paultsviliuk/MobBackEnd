import random
from random import choice
from string import ascii_letters

def makeTokken():
    tokken=[]
    for i in range(1,10):
        tokken.append(random.randint(1,200))
    tokken=bytearray(tokken)
    tokken=str(tokken)[9:].replace('\\','>')
    tokken=tokken.replace('"','<')
    return tokken

def makeRestoreCode():
    return ''.join(choice(ascii_letters) for i in range(10))
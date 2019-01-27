#!/usr/bin/env python3

# Light each LED in sequence, and repeat.

from patterns import patt
from patterns import allCols
from patterns import german
import random
import pdb
import sys
import opc,time
numLEDs = 54
client = opc.Client('localhost:7890')
client.set_interpolation(False)

cols = [(231, 76, 60),(230, 126, 34),(241, 196, 15),(39, 174, 96),(52, 152, 219),(142, 68, 173)]
def fill(inString,inColor):
   pass 

def nextColor(r,g,b):
    if r > 0 and b == 0:
        return r-1,g+1,b
    if g > 0 and r == 0:
        return r,g-1,b+1
    if b > 0 and g == 0:
        return r+1,g,b-1

def rainbowStripes():
    for i in range(18):
        direction = i//6 + 1
        stripe = i%6 + 1
        pixels = [ (90,90,90) ] * numLEDs
        for j in patt['stripe'][direction][stripe]:
            pixels[j] = cols[stripe-1]
        client.put_pixels(pixels)
        time.sleep(0.1)

def rainbowRings():
    for i in range(6):
        pixels = [ (0,0,0) ] * numLEDs
        for j in patt['ring'][1]:
            pixels[j] =cols[i]
        for j in patt['ring'][2]:
            pixels[j] =cols[(i+5)%6]
        for j in patt['ring'][3]:
            pixels[j] =cols[(i+4)%6]
        client.put_pixels(pixels)
        time.sleep(0.3)

def rainbowTriangles():
    pixels = [ (0,0,0) ] * numLEDs
    for i in range(6):
        for j in patt['triangle'][i+1]:
            pixels[j] =cols[i]
    client.put_pixels(pixels)
    time.sleep(5)
def rainbowTriangleWipe():
    pixels = [ (0,0,0) ] * numLEDs
    triMap = [1,2,3,6,5,4]
    # finds each larger triangle
    for i in range(6):
        # fills in the triangle
        for j in patt['triangle'][triMap[i]]:
            pixels[j] =cols[i]
    client.put_pixels(pixels)
    time.sleep(1)
    for loop in range(30):
        # finds each larger triangle
        for i in range(6):
            # fills in the triangle
            for j in patt['triangle'][triMap[i]]:
                pixels[j] =cols[i]
        dominantColor = loop//5
        overtaken = (6-loop%6)%6
        for j in patt['triangle'][triMap[overtaken]]:
            pixels[j] =cols[dominantColor]
        for j in patt['triangle'][triMap[(overtaken+1)%6]]:
            pixels[j] =cols[dominantColor]
        client.put_pixels(pixels)
        time.sleep(0.3)

def rando():
    hexSet = list(range(54))
    pixels = [ (0,0,0) ] * numLEDs
    for ledNum in hexSet:
        colNum = random.randint(0,len(german)-1)
        pixels[ledNum] = german[colNum]
    client.put_pixels(pixels)
    return pixels

def randomloop(delay=0.5):
    while True:
        rando()
        time.sleep(delay)

def sprinkle(delay=0.05):
    pixels = rando()
    led_list = list(range(54))
    random.shuffle(led_list)
    while True:
        for ledNum in led_list:
            colNum = random.randint(0,len(german)-1)
            while german[colNum] == pixels[ledNum]:
                colNum = random.randint(0,len(german)-1)
            pixels[ledNum] = german[colNum]
            client.put_pixels(pixels)
            time.sleep(delay)
             

def pumpkin():
    pixels = [german[1]] * numLEDs
    for j in patt['pumpkin']['mouth']:
        pixels[j] = (0,0,0)
    for j in patt['pumpkin']['eyes']:
        pixels[j] = (0,0,0)
    for j in patt['pumpkin']['top']:
        pixels[j] = (0,255,0)
    client.put_pixels(pixels)

def tree():
    pixels = [(1, 50, 67)] * numLEDs
    for j in patt['tree']['leaves']:
        pixels[j] = (0,255,0)
    for j in patt['tree']['trunk']:
        pixels[j] = (86, 47, 14)
    for j in patt['tree']['star']:
        pixels[j] = (245, 230, 83)

def david():
    r,g,b = (255,0,0)
    while True:
        pixels = [(100,100,100)] * numLEDs
        for j in patt['david']:
            pixels[j] = (r,g,b)
        r,g,b = nextColor(r,g,b)
        client.put_pixels(pixels)
        time.sleep(.01)



def fun(routine):
    try:
        globals()[routine]()
    except (ImportError):
        print("Trouble in paradise")

if __name__ == "__main__":
    if sys.argv[1]:
        fun(sys.argv[1])

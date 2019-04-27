#!/usr/bin/env python3

# Light each LED in sequence, and repeat.

from pudb.remote import set_trace
from patterns import patt
from patterns import allCols
from patterns import german
import random
import pdb
import sys
import opc,time
import queue
numLEDs = 54
cols = [(231, 76, 60),(230, 126, 34),(241, 196, 15),(39, 174, 96),(52, 152, 219),(142, 68, 173)]
class Fun:
    def __init__(self):
        self.client = opc.Client('localhost:7890')
        self.client.set_interpolation(False)
        self._instances = {}

    def _run(self, q):
        delay = 1
        need_next = False
        current_pattern = None
        q.put('off')
        while True:
            empty_queue = q.empty()
            if empty_queue and not need_next:
                time.sleep(delay)
            else:
                if not empty_queue:
                    try:
                        # set_trace(term_size=(150,75))
                        current_pattern = q.get(block=False, timeout=1)
                    except queue.Empty:
                        pass
                result = self._fetch_frame(current_pattern)
                if result is not None:
                    pixels, delay, need_next = result
                self.client.put_pixels(pixels)
                time.sleep(delay)

    def _fetch_frame(self, current_pattern):
        try:
            if current_pattern.startswith('custom'):
                func = getattr(self, '_custom')
                return func(current_pattern)
            else:
                func = getattr(self, current_pattern)
                if current_pattern not in self._instances:
                    self._instances[current_pattern] = func()
                return next(self._instances[current_pattern])
        except AttributeError:
            return None


    def _custom(self, new_data):
        """takes a string of exactly numLeds long of the form
           custom XXXXXX XXXXXX ..."""
        pixels = []
        try:
            for i in range(numLEDs):
                hex_code = new_data[7*(i+1):7*(i+2)]
                if hex_code[6] != "_":
                    raise ValueError
                red = int(hex_code[0:2], 16)
                green = int(hex_code[2:4], 16)
                blue = int(hex_code[4:6], 16)
                pixel = (red, green, blue)
                pixels.append(pixel)
            return (pixels , 1, False)
        except:
            return None


    def rainbow_stripes(self):
        while True:
            for i in range(18):
                direction = i//6 + 1
                stripe = i%6 + 1
                pixels = [ (90,90,90) ] * numLEDs
                for j in patt['stripe'][direction][stripe]:
                    pixels[j] = cols[stripe-1]
                yield (pixels, 0.1, True)

    def rainbow_rings(self):
        while True:
            for i in range(6):
                pixels = [ (0,0,0) ] * numLEDs
                for j in patt['ring'][1]:
                    pixels[j] =cols[i]
                for j in patt['ring'][2]:
                    pixels[j] =cols[(i+5)%6]
                for j in patt['ring'][3]:
                    pixels[j] =cols[(i+4)%6]
                yield (pixels, 0.3, True)

    def rainbow_triangles(self):
        while True:
            pixels = [ (0,0,0) ] * numLEDs
            for i in range(6):
                for j in patt['triangle'][i+1]:
                    pixels[j] =cols[i]
            yield(pixels, 0.1, False)

    def rainbow_triangle_wipe(self):
        while True:
            pixels = [ (0,0,0) ] * numLEDs
            triMap = [1,2,3,6,5,4]
            # finds each larger triangle
            for i in range(6):
                # fills in the triangle
                for j in patt['triangle'][triMap[i]]:
                    pixels[j] =cols[i]
            yield (pixels, 1, True)
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
                yield (pixels, 0.3, True)

    def sprinkle(self):
        hexSet = list(range(54))
        pixels = [ (0,0,0) ] * numLEDs
        for ledNum in hexSet:
            colNum = random.randint(0,len(german)-1)
            pixels[ledNum] = german[colNum]
        while True:
            led_list = list(range(54))
            random.shuffle(led_list)
            for ledNum in led_list:
                colNum = random.randint(0,len(german)-1)
                while german[colNum] == pixels[ledNum]:
                    colNum = random.randint(0,len(german)-1)
                pixels[ledNum] = german[colNum]
                yield (pixels,0.05, True)
    
    def snake(self):
        default_color = (0,0,0)
        random = random.randint(0,255)
        fade = n*5
        while True:
            for cell in range(numLEDs):
                pixels = [default_color] * numLEDs
                #first cell of snake
                pixels[cell] = (0,0,255)
                #other cells of snake
                for n in range(1,numLEDs):
                    pixels[cell-n] = (random-fade,random-fade,random-fade)
                yield (pixels, .09, True)

    def pumpkin(self):
        while True:
            pixels = [german[1]] * numLEDs
            for j in patt['pumpkin']['mouth']:
                pixels[j] = (0,0,0)
            for j in patt['pumpkin']['eyes']:
                pixels[j] = (0,0,0)
            for j in patt['pumpkin']['top']:
                pixels[j] = (0,255,0)
            yield (pixels,0.1,False)

    def tree(self):
        while True:
            pixels = [(1, 50, 67)] * numLEDs
            for j in patt['tree']['leaves']:
                pixels[j] = (0,255,0)
            for j in patt['tree']['trunk']:
                pixels[j] = (86, 47, 14)
            for j in patt['tree']['star']:
                pixels[j] = (245, 230, 83)
            yield (pixels, 0.1, False)

    def off(self):
        while True:
            pixels = [(0, 0, 0)] * numLEDs
            yield (pixels, 0.1, False)

    def flower(self):
        while True:
            #variable for yellow  petals
            petal_color = (255,233,0)
            #set background to purple
            pixels = [(149,44,201)] * numLEDs
            for j in patt['flower']['pistil']:
                #set pistil to brown
                pixels[j] = (66,28,19)
            for j in patt['flower']['left']:
                pixels[j] = petal_color
            for j in patt['flower']['top']:
                pixels[j] = petal_color
            for j in patt['flower']['right']:
                pixels[j] = petal_color
            for j in patt['flower']['bottom']:
                pixels[j] = petal_color
            yield (pixels, 0.1, False)

    def david(self):
        while True:
            r,g,b = (0,0,255)
            pixels = [(100,100,100)] * numLEDs
            for j in patt['david']:
                pixels[j] = (r,g,b)
            yield (pixels, 0.1, False)

    def valentine(self):
        while True:
            pixels = [(255,255,255)] * numLEDs
            for j in patt['valentine']:
                pixels[j] = (255,0,0)
            yield (pixels, 0.1, False)

    def pizza(self):
        while True:
            pixels = [(233,223,192)] * numLEDs
            for p in patt['ring'][3]:
                pixels[p] = (244,191,73)
            yield (pixels, 0.1, False)

    def fade(self):
        while True:
            bright = random.randint(0,255)
            pixels = [(bright,bright,bright)] * numLEDs
            while bright > 0:
                bright -= 1
                pixels = [(bright,bright,bright)] * numLEDs
                yield (pixels, .027, True)
            yield (pixels, 0.5, False)

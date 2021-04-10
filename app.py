from flask import Flask
from PixelBoard import PixelBoard
import time
import json
import board
import threading


class myBoard(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1
        self.pixel_board = PixelBoard(board.D18, 16, 16, 0.6)
        self.images = self.initImages()
        self.bvalue = 0
        self.loop = False
        self.current_index = 0

    def initImages(self):
        print('loading images')
        with open('/home/pi/Pixel Board/image.json') as f:
            data = json.load(f)
        print('images loaded')
        return data

    def display(self):
        length = len(self.images)
        while(True):
            # check if on or off
            if(self.bvalue):
                start = int(time.time())
                temp_index = self.current_index
                # loop till time to move on to next image
                while((int(time.time()) - start < (10)) or self.loop):
                    if(self.current_index != temp_index or not self.bvalue):
                        break
                    for i in range(len(self.images[self.current_index % length])):
                        if(self.current_index != temp_index or not self.bvalue):
                            break
                        self.pixel_board.displayImage(
                            self.images[self.current_index % length][f'frame {i}'])
                        time.sleep(0.1)
                else:
                    self.current_index = (self.current_index + 1) % length
            else:
                self.pixel_board.clear()
                time.sleep(0.1)

    def run(self):
        print('running')
        while True:
            self.display()


app = Flask(__name__)
my_board = myBoard()

@app.route('/')
def hello():
    return "Hello World!"

    
@app.route('/switch')
def switch():
    my_board.bvalue = not my_board.bvalue
    print('on/off pressed')
    return my_board.bvalue and "ON" or "OFF"


@app.route('/prev')
def prev():
    my_board.current_index -= 1
    print('skip button pressed')
    return f'Skipped. Current index: {my_board.current_index}'

@app.route('/next')
def next():
    my_board.current_index += 1
    print('skip button pressed')
    return f'Skipped. Current index: {my_board.current_index}'


@app.route('/loop')
def loop_switch():
    my_board.loop = not my_board.loop
    print('loop button pressed')
    return my_board.loop and "LOOP ON" or "LOOP OFF"


if __name__ == '__main__':
    my_board.start()
    app.run(port=80, host='0.0.0.0', debug=False, use_reloader=False)

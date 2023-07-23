from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from PixelBoard import PixelBoard
import image_to_json
import time
import json
import board
import threading
import imghdr
import os


class myBoard(threading.Thread):
    def __init__(self, pBoard):
        threading.Thread.__init__(self)
        self.pixel_board = pBoard
        self.images = self.initImages()
        self.bvalue = 0
        self.loop = False
        self.current_index = 0
        self.length = len(self.images)

    def initImages(self):
        print('loading images')
        with open('/home/pi/Pixel Board/image.json') as f:
            data = json.load(f)
        print('images loaded')
        return data

    def display(self):
        while(True):
            # check if on or off
            if(self.bvalue):
                start = int(time.time())
                temp_index = self.current_index
                # loop till time to move on to next image
                while((int(time.time()) - start < (10)) or self.loop):
                    if(self.current_index != temp_index or not self.bvalue):
                        break
                    for i in range(len(self.images[self.current_index % self.length])):
                        if(self.current_index != temp_index or not self.bvalue):
                            break
                        self.pixel_board.displayImage(
                            self.images[self.current_index % self.length][f'frame {i}'])
                        time.sleep(0.1)
                else:
                    self.current_index = (self.current_index + 1) % self.length
            else:
                self.pixel_board.clear()
                time.sleep(0.1)

    def switch(self):
        self.bvalue = not self.bvalue

    def skip(self):
        self.current_index += 1

    def prev(self):
        self.current_index -=1

    def loopSwitch(self):
        self.loop = not self.loop

    def run(self):
        print('Pixel Board Running')
        while True:
            self.display()


app = Flask(__name__)
my_board = myBoard(PixelBoard(board.D18, 16, 16, 0.6))
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = '/home/pi/Pixel Board/images'


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.route('/')
def hello():
    return "Hello World!"

    
@app.route('/switch')
def switch():
    my_board.switch()
    print('on/off pressed')
    return my_board.bvalue and "ON" or "OFF"


@app.route('/prev')
def prev():
    my_board.prev()
    print('skip button pressed')
    return f'Skipped. Current index: {my_board.current_index}'

@app.route('/next')
def next():
    my_board.skip()
    print('skip button pressed')
    return f'Skipped. Current index: {my_board.current_index}'


@app.route('/loop')
def loop_switch():
    my_board.loopSwitch()
    print('loop button pressed')
    return my_board.loop and "LOOP ON" or "LOOP OFF"


@app.route('/upload')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    print(filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(path)
        print(f'File uploaded at {path}')
        print('Processing image')
        image_to_json.imgToJson(path, my_board.images)
        print('image processed')
        my_board.length = len(my_board.images)
        os.system('rm image.json && touch image.json')
        with open('image.json', 'w') as fout:
             json.dump(my_board.images, fout)
        print('image file updated')
    return '', 204


if __name__ == '__main__':
    my_board.start()
    app.run(port=80, host='0.0.0.0', debug=False, use_reloader=False)

import time, json, board
from PixelBoard import PixelBoard
import BlynkLib
import threading
global bvalue, images, loop, current_index


def initImages():
    print('loading images')
    with open('/home/pi/Pixel Board/image.json') as f:
        data = json.load(f)
    print('images loaded')
    return data



images = initImages()
print('Initializing blynk connection')
blynk = BlynkLib.Blynk('gWccqWX-FZoCWHrJ5IOr-q97prFF8L6W',
                       server='blynk.iot-cm.com', port=8080)


bvalue = 0
loop = False
current_index = 0

# ON/OFF
@blynk.VIRTUAL_WRITE(1)
def on_off_handler(value):
    global bvalue
    if(int(value[0]) == 1):
        bvalue = not bvalue
        print('on/off pressed')
    

# SKIP ANIMATION
@blynk.VIRTUAL_WRITE(2)
def skip_handler(value):
    global current_index
    if(int(value[0]) == 1):
        current_index += 1
        print('skip button pressed')

# LOOP
@blynk.VIRTUAL_WRITE(3)
def loop_handler(value):
    global loop
    loop = bool(int(value[0]))
    print('loop button pressed')


def display():
    global current_index
    length = len(images)
    while(True):
        # check if on or off
        if(bvalue):
            start =int(time.time())
            temp_index = current_index
            # loop till time to move on to next image
            while((int(time.time()) - start < (10)) or loop):
                if(current_index != temp_index or not bvalue):
                    break
                for i in range(len(images[current_index%length])):
                    if(current_index != temp_index or not bvalue):
                        break
                    pixel_board.displayImage(images[current_index%length][f'frame {i}'])
                    time.sleep(0.1)
            else:
                current_index = (current_index + 1) % length
        else:
            pixel_board.clear()
            time.sleep(0.1)


pixel_board = PixelBoard(board.D18,16,16,0.6)


def getInput():
    while True:
        blynk.run()


try:
    t1 = threading.Thread(target=display)
    t2 = threading.Thread(target=getInput)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


except KeyboardInterrupt:
    pixel_board.clear()
    time.sleep(0.5)
    exit()

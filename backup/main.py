import time, json, board
from PixelBoard import PixelBoard
import BlynkLib
import threading
global bvalue, images, loop, current_index

time.sleep(5)

# Initialize Blynk
blynk = BlynkLib.Blynk('gWccqWX-FZoCWHrJ5IOr-q97prFF8L6W',
                       server='blynk.iot-cm.com', port=8080)
def initImages():
    with open('/home/pi/Pixel Board/image.json') as f:
        data = json.load(f)
    return data

images = initImages()
bvalue = 1
loop = False
current_index = 0

# ON/OFF
@blynk.VIRTUAL_WRITE(1)
def on_off_handler(value):
    global bvalue
    bvalue = bool(int(value[0]))

# SKIP ANIMATION
@blynk.VIRTUAL_WRITE(2)
def skip_handler(value):
    global current_index
    if(int(value[0]) == 1):
        print(value[0])
        current_index += 1

# LOOP
@blynk.VIRTUAL_WRITE(3)
def loop_handler(value):
    global loop
    loop = bool(int(value[0]))


def display():
    global current_index
    length = len(images)
    while(True):
        # check if on or off
        if(bvalue):
            start = time.time()
            temp_index = current_index
            # loop till time to move on to next image
            while((time.time() - start < (10)) or loop):
                blynk.run()
                if(not bvalue):
                    pixel_board.clear()
                    break
                if(current_index != temp_index):
                    break
                for i in range(len(images[current_index%length])):
                    blynk.run()
                    if(not bvalue):
                        pixel_board.clear()
                        break
                    if(current_index != temp_index):
                        break
                    pixel_board.displayImage(images[current_index%length][f'frame {i}'])
                    time.sleep(0.1)
            current_index = (current_index + 1) % length
        else:
            pixel_board.clear()
            while(not bvalue):
                blynk.run()
                time.sleep(1)

pixel_board = PixelBoard(board.D18,16,16,0.6)


try:
    """t1 = threading.Thread(target=display)
    t2 = threading.Thread(target=getInput)

    t1.start()
    t2.start()

    t1.join()
    t2.join()"""
    while True:
        display()

except KeyboardInterrupt:
    pixel_board.clear()
    time.sleep(0.5)
    exit()

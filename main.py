from PixelBoard import PixelBoard
import BlynkLib
import time, json, board

# Initialize Blynk
blynk = BlynkLib.Blynk('gWccqWX-FZoCWHrJ5IOr-q97prFF8L6W', server='blynk.iot-cm.com', port = 8080)


def initImages():
    with open('/home/pi/Pixel Board/image.json') as f:
        data = json.load(f)
    return data


global bvalue, images


images = initImages()
bvalue = 1

def getValue():
    global bvalue
    return bvalue

def setValue(n):
    global bvalue
    bvalue = n


@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    setValue(int(value[0]))
    time.sleep(0.5)
    counter = 0
    length = len(images)
    if(bool(getValue())):
        start = time.time()
        counter = (counter + 1)%length
        while(time.time() - start < (10)):
            if(not bool(getValue())):
                pixel_board.clear()
                break
            for i in range(len(images[counter%length])):
                if(not bool(getValue())):
                    pixel_board.clear()
                    break
                pixel_board.displayImage(images[counter%length][f'frame {i}'])
                time.sleep(0.1)
    else:
        pixel_board.clear()
        while(not bool(getValue())):
            time.sleep(1)

pixel_board = PixelBoard(board.D18,16,16,0.6)

try:
    while(True):
        blynk.run()

except KeyboardInterrupt:
    pixel_board.clear()
    time.sleep(0.5)
    exit()

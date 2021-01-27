from PIL import Image, ImageSequence
import time, json, imageio, os
#import BlynkLib

# Initialize Blynk
#blynk = BlynkLib.Blynk('gWccqWX-FZoCWHrJ5IOr-q97prFF8L6W', server='blynk.iot-cm.com', port = 8080)


global img_array, bvalue

bvalue = 1


def initImages():
    with open('image.json') as f:
        data = json.load(f)
    return data


images = initImages()

"""
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    bvalue = int(value[0])"""


def imgToJson(path):
    print(path)
    temp = path.split('.')
    width, height = Image.open(path).size
    if(width > 16 and height > 16):
        resize_img(path)
        time.sleep(1)

    counter = 0
    frame = {}
    if temp[1] == 'gif':
        img = imageio.get_reader(path)
        for iframe in img:
            dict = {}
            for row in range(16):
                for col in range(16):
                    dict[f'{col}, {row}'] = iframe[col][row][:3].tolist()
            frame['frame '+str(counter)] = dict
            counter += 1
        images.append(frame)

    else:
        img = imageio.imread(path)
        dict = {}
        for row in range(16):
            for col in range(16):
                dict[f'{col}, {row}'] = img[col][row][:3].tolist()
        frame['frame 0'] = dict
        images.append(frame)


def resize_img(path):
    size = 16,16

    # Open source
    im = Image.open(path)

    # Get sequence iterator
    frames = ImageSequence.Iterator(im)

    # Wrap on-the-fly thumbnail generator
    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.ANTIALIAS)
            yield thumbnail

    frames = thumbnails(frames)

    # Save output
    om = next(frames) # Handle first frame separately
    om.info = im.info # Copy sequence info
    om.save(path, save_all=True, append_images=list(frames))



def resize_files():
    for file in os.listdir('./images'):
        imgToJson(f'images/{file}')


#pixel_board = PixelBoard(board.D18,16,16,0.6)
"""
pixel_board = PixelBoard(board.D18,16,16,0.6)

resize_files()
with open('image.json', 'w') as fout:
    json.dump(images , fout)

"""


resize_files()
with open('image.json', 'w') as fout:
    json.dump(images , fout)

"""
try:
    counter = 0
    length = len(images)
    while(True):
        blynk.run()
        if(bool(bvalue)):
            start = time.time()
            counter += 1
            while(time.time() - start < (10)):
                for i in range(len(images[counter%length])):
                    pixel_board.displayImage(images[counter%length][f'frame {i}'])
                    time.sleep(0.1)
        else:
            pixel_board.clear()


except KeyboardInterrupt:
    pixel_board.clear()
    time.sleep(0.5)
    exit()
"""

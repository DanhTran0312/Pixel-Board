from PIL import Image, ImageSequence
import time
import json
import imageio
import os


def imgToJson(path, image_list):
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
        image_list.append(frame)

    else:
        img = imageio.imread(path)
        dict = {}
        for row in range(16):
            for col in range(16):
                dict[f'{col}, {row}'] = img[col][row][:3].tolist()
        frame['frame 0'] = dict
        image_list.append(frame)


def resize_img(path):
    size = 16, 16

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
    om = next(frames)  # Handle first frame separately
    om.info = im.info  # Copy sequence info
    om.save(path, save_all=True, append_images=list(frames))

    

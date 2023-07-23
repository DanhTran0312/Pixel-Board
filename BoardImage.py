from PIL import Image, ImageSequence
import imageio
import json


class BoardImage():
    def __init__(self, path):
        temp = path.split('.')
        self.path = path
        self.name = temp[0]
        self.format = temp[1]


    def saveImage(self, img):
        img_file = loadImage()
        if img_file != "":
            images = [img_file]
            images.append(img)
        else:
            images = [img]
        a_file = open("image.json", "w")
        json.dump(images, a_file)
        a_file.close()



    def init(self):
        if(self.name in img_dict):
            return loadImage()[self.name]
        else:
            img_dict = {}
            if self.format == 'gif':
                 im = imageio.get_reader()
                 img_dict[self.name] = []
                 for frame in im:
                     img_dict[self.name].append(frame)
            else:
                img = imageio.imread(self.path)
                img_dict[self.name] = img
                saveImage([img_dict])
            return self.getImage()



    def loadImage(self):
        a_file = open("image.json", "r")
        content = a_file.read()
        a_file.close()
        return content



    def resize_gif(self, path):
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



    def getImage(self):
        if(self.name in img_dict):
            return loadImage()[self.name]
        else:
            img_dict = {}
            if self.format == 'gif':
                 im = imageio.get_reader()
                 img_dict[self.name] = []
                 for frame in im:
                     img_dict[self.name].append(frame)
            else:
                img = imageio.imread(self.path)
                img_dict[self.name] = img
                saveImage([img_dict])
            return self.getImage()

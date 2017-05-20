import Tkinter as tk # Python 2
import time
import os
import random
import utils
from PIL import Image, ImageTk, ImageSequence

class Gif:
    def __init__(self, organism, root):
        """ adds an image widget to root level window """
        file_names = organism.gif_names
        num_gif_frames = organism.num_frames
        self.frames = [[] for name in organism.gif_names]

        for k in range(len(file_names)):
            pil_gif = Image.open(file_names[k])
            i = 0
            for frame in ImageSequence.Iterator(pil_gif):
                frame = frame.resize((organism.width, organism.height), Image.ANTIALIAS)
                self.frames[k].append(ImageTk.PhotoImage(frame, format='gif -index %i' % (i)))
                i += 1

        # The image must be stored to Tk or it will be garbage collected.
        image = Image.open(file_names[0])
        image = image.resize((organism.width, organism.height), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        root.image = ImageTk.PhotoImage(image)

        self.label = tk.Label(root, image=root.image, bg='white')

        if organism.click_handler != None:
            self.label.bind("<Button-1>", lambda event, arg=organism: organism.click_handler(event, arg))
        if organism.move_handler != None:
            self.label.bind("<B1-Motion>", lambda event, arg=organism: organism.move_handler(event, arg))
        if organism.release_handler != None:
            self.label.bind("<ButtonRelease-1>", lambda event, arg=organism: organism.release_handler(event, arg))

        self.label.pack()

    def set_frame(self, gif_num, frame_num):
        """ sets image to frames[frame_num] """
        self.label.configure(image= self.frames[gif_num][frame_num])

    def set_pos(self, x, y):
        self.label.place(x=x, y=y)


def get_frame_num(elapsed_time, interval, num_frames):
    """ specifies which frame in the gif to use, assuming that the gif should be looping forever """
    section_num = int(elapsed_time / float(interval))
    return section_num % num_frames


# http://stackoverflow.com/questions/7503567/python-how-i-can-get-gif-frames
class GIFError(Exception): pass
def get_gif_num_frames(filename):
    frames = 0
    with open(filename, 'rb') as f:
        if f.read(6) not in ('GIF87a', 'GIF89a'):
            raise GIFError('not a valid GIF file')
        f.seek(4, 1)
        def skip_color_table(flags):
            if flags & 0x80: f.seek(3 << ((flags & 7) + 1), 1)
        flags = ord(f.read(1))
        f.seek(2, 1)
        skip_color_table(flags)
        while True:
            block = f.read(1)
            if block == ';': break
            if block == '!': f.seek(1, 1)
            elif block == ',':
                frames += 1
                f.seek(8, 1)
                skip_color_table(ord(f.read(1)))
                f.seek(1, 1)
            else: raise GIFError('unknown block type')
            while True:
                l = ord(f.read(1))
                if not l: break
                f.seek(l, 1)
    return frames
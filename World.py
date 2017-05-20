import Tkinter as tk # Python 2
import time
import os
import random
import utils
import Gif
import Organism


class World:

    def __init__(self):
        """ initializes to full screen, but completely transparent / click-through """
        root = tk.Tk()
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        root.overrideredirect(True)
        root.geometry(str(self.width)+"x"+str(self.height)+"+0+0")
        root.lift()
        root.wm_attributes("-topmost", True)
        #root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "white")
        root.configure(bg='white')

        # set important parameters
        self.root = root
        self.delay = 20  # in milliseconds
        self.organisms = dict()
        self.gravity = 9.8  # no negative gravity please

    def add_organism(self, organism):
        """ adds an organism object that can react / interact to the mainloop """
        gif = Gif.Gif(organism, self.root)
        self.organisms[organism.name] = [organism, gif]

    def mainloop(self):

        for name, organism_pair in self.organisms.iteritems():
            organism = organism_pair[0]
            organism.update(self, organism)
            gif = organism_pair[1]
            gif.set_frame(organism.gif_num, organism.frame_num)

            if not organism.being_held:
                organism.x += organism.v_x
                organism.y += -organism.v_y

            # check if valid first, we will use + y-dir as going up
            self.validity_thresh(organism)
            self.apply_gravity(organism)
            gif.set_pos(organism.x, organism.y)

        # update and react
        self.root.after(self.delay, self.mainloop)

    def validity_thresh(self, organism):
        """ check if any parts are out of bounds """
        left = organism.x
        right = left + organism.width
        top = organism.y
        bottom = top + organism.height

        if left < 0:
            organism.x = 0
        elif right >= self.width:
            organism.x = self.width - organism.width

        if top < 0:
            organism.y = 0
        elif bottom >= self.height:
            organism.y = self.height - organism.height

    def apply_gravity(self, organism):
        if not utils.touching_borders(self, organism) and not organism.defy_gravity:
            organism.v_y += -self.gravity * self.delay / 1000.0

    def start(self):
        self.root.after(0, self.mainloop)
        self.root.mainloop()
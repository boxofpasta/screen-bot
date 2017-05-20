import Tkinter as tk # Python 2
import time
import os
import random
import utils
import Gif
import datetime

start_time = datetime.datetime.now()

class Organism:

    def __init__(self, update_func, width, height, gif_names,
                 click_handler=None,
                 move_handler=None,
                 release_handler=None):
        """ 
            update_func defines how the organism will react to world info.
            The function call must look like: update_func(World, Organism)
        """
        self.update = update_func

        self.being_held = False

        # positions (World will modify these values based on current velocities!)
        # do not modify these unless you would like to teleport
        self.x = 0
        self.y = 0

        # velocities, note that v_y will be ignored when gravity is on and the sprite is not touching
        # any of the screen borders
        self.v_x = 0
        self.v_y = 0

        self.defy_gravity = False
        self.frame_interval = 100

        # World will resize the gif to be these dimensions
        self.width = width
        self.height = height

        # array of gifs, to support multiple sprites
        self.gif_names = gif_names
        self.num_frames = [Gif.get_gif_num_frames(gif_name) for gif_name in gif_names]
        self.frame_num = 0
        self.gif_num = 0
        self.name = "default sprite"

        # these callback options are optional
        self.click_handler = click_handler
        self.move_handler = move_handler
        self.release_handler = release_handler

    def loop_gif_update(self):
        """ loops the current gif (just sets the frame_num), default behaviour """
        elapsed = utils.get_elapsed_time(start_time, datetime.datetime.now())
        num_frames = self.num_frames[self.gif_num]
        self.frame_num = Gif.get_frame_num(elapsed, self.frame_interval, num_frames)

import Tkinter as tk # Python 2
import time
import os
import random
import utils
import Gif
import Organism
import World
import datetime

start_time = datetime.datetime.now()

def update_func(world, organism):
    # choose gif based on direction
    organism.gif_num = 0
    if organism.v_x < 0:
        organism.gif_num = 1

    # update frame in gif
    organism.loop_gif_update()

    # update the velocity, this accelerates the sprite in the current direction
    accel = 0.5
    if organism.v_x > 0:
        organism.v_x += accel
    else:
        organism.v_x -= accel

    if organism.defy_gravity or utils.touching_borders(world, organism):
        if organism.v_y > 0:
            organism.v_y += accel
        else:
            organism.v_y -= accel

    # react upon hitting the screen edges
    if utils.hit_left(world, organism):
        print "OW!"
        organism.v_x = accel
    elif utils.hit_right(world, organism):
        print "DAMMIT!"
        organism.v_x = -accel

    if utils.hit_top(world, organism):
        print "P**********!"
        organism.v_y = -accel
    elif utils.hit_bottom(world, organism):
        print "..."

        # make a jump
        organism.v_y = 10

def click_handler(event, organism):
    print "i have been saved!"
    organism.being_held = True

def move_handler(event, organism):
    organism.x = event.x_root
    organism.y = event.y_root

def release_handler(event, organism):
    organism.being_held = False
    print "oh no, out of control again!!"

if __name__ == '__main__':

    # setup the sprite
    gif_names = ["gifs/bird_right.gif", "gifs/bird_left.gif"]
    organism = Organism.Organism(update_func, 60, 60, gif_names,click_handler, move_handler, release_handler)
    organism.frame_interval = 50

    # setup and run the world
    w = World.World()
    w.add_organism(organism)
    w.start()
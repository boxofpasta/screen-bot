import Tkinter as tk # Python 2
import time
import os
import random
import datetime


# This file contains helpful functions that don't belong anywhere else

def hit_left(world, organism):
    return (organism.x <= 0)

def hit_right(world, organism):
    return ((organism.x + organism.width) >= world.width)

def hit_top(world, organism):
    return (organism.y <= 0)

def hit_bottom(world, organism):
    return ((organism.y + organism.height) >= world.height)

def touching_borders(world, org):
    return (hit_left(world, org) or hit_right(world, org) or hit_bottom(world, org) or hit_top(world, org))

def get_elapsed_time(start, now):
    """ takes 2 datetime arguments """
    delta = now - start
    return int(delta.total_seconds() * 1000)
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:34:24 2021

@author: Thomas Dye
"""

import subprocess
import matplotlib.pyplot as plt

def gerbv(basename):
    command = "gerbv -f #FFFFFF {0}.GTO -f #a0a000 {0}.TXT -f #FF0000 {0}.GTL -f #00FF00 {0}.GBL -f #202020 {0}.GML".format(basename)
    gerbvsub = subprocess.Popen(command,start_new_session=True)
    return gerbvsub

def gerbvplt(basename):
    command = "gerbv -a -D1000 -xpng -o {0}.png -f #FFFFFF {0}.GTO -f #a0a000 {0}.TXT -f #FF0000 {0}.GTL -f #00FF00 {0}.GBL -f #202020 {0}.GML".format(basename)
    gerbvsub = subprocess.run(command)
    im = plt.imread(basename + '.png')
    plt.imshow(im)
    return gerbvsub

class plotter:
    
    base_render_command = "gerbv -a -D1000 -xpng -o {0}_{2}.png -f {1} {0}.{2}"
    
    def __init__(self,basename):
        self.basename = basename
    
    def render(self,layer_ext="GTL",color="#FF0000"):
        command = self.base_render_command.format(self.basename,color,layer_ext)
        self.render_result = subprocess.run(command)
    
    def plot(self,layer_ext):
            im = plt.imread(self.basename + '_' + layer_ext + '.png')
            return plt.imshow(im)
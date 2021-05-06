# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:00:44 2021

@author: Thomas Dye
"""

from pcbtools import gerber as gtools
from pcbtools.gerber.render.cairo_backend import GerberCairoContext

class Renderer:
    
    def __init__(self,basename):
        self.__basename__ = basename
        self.ctx = GerberCairoContext()
    
    def dump_image(self, name):
        self.ctx.dump(name)
    
    def clear_image(self):
            self.ctx.clear()
    
    def render_layer(self,extension):
        name = self.__basename__ + '.' + extension
        layer = gtools.load_layer(name)
        self.ctx.render_layer(layer)
    
    def render_layers(self,extensions):
        for ext in extensions:
            self.render_layer(ext)
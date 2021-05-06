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
        self.ctx = []
    
    def new_window(self):
        self.ctx.append(GerberCairoContext())
    
    def clear_window(self, i):
        if i in range(len(self.ctx)):
            self.ctx[i].clear()
    
    def render_layer(self,extension):
        layer = gtools.load_layer(self.__basename__ + '.' + extension)
        if len(self.ctx) == 0:
            self.new_window()
        n = len(self.ctx)-1
        self.ctx[n].render_layer(layer)
    
    def render_layers(self,extensions):
        for ext in extensions:
            self.render_layer(ext)
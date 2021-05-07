# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:00:44 2021

@author: Thomas Dye
"""

from pcbtools import gerber as gtools
from pcbtools.gerber.render import GerberCairoContext

class Renderer:
    
    def __init__(self,basename):
        self.__basename__ = basename
        self.ctx = GerberCairoContext()
        
    
    
    def render_layer(self,extension):
        name = self.__basename__ + '.' + extension
        layerfile = gtools.read(name)
        layerfile.render(self.ctx)
    
    def render_layers(self,extensions):
        for ext in extensions:
            self.render_layer(ext)
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:07:57 2021

@author: Thomas Dye
"""

from cuflow import cuflow



if __name__ == "__main__":
    brd = cuflow.Board((285,95), trace=0.127, space=0.127, via_hole=0.2, via=0.4, via_space=0.254, silk=0.153)
    

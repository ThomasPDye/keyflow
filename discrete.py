# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:28:37 2021

@author: Thomas Dye
"""

import os
import cuplot
from cuflow import cuflow

class C0402(cuflow.Discrete2):
    family = "C"
    footprint = "0402"
    dims = dict(C=1.05,X=0.62,Y=0.56,L=1.05,W=0.6)
    def place(self,dc):
        # pads on either side
        for d in (-90,90):
            dc.push()
            dc.right(d)
            dc.forward(self.dims['C']/2)
            dc.rect(self.dims['X'],self.dims['Y'])
            self.pad(dc)
            dc.pop()
        # Silk outline
        dc.rect(self.dims['L'],self.dims['W'])
        dc.silko()
        # label
        dc.push()
        dc.right(90)
        dc.forward(self.dims['C'] + self.dims['Y'])
        self.label(dc)


class Y2520(cuflow.Part):
    family = "Y"
    footprint = "2520"
    dims = dict(L=2.0,W=2.5,X=1.0,Y=0.95,B=1.25,C=1.425)
    def place(self,dc):
        # four pads
        x = -self.dims['C']/2
        y = -self.dims['B']/2
        for i in range(4):
            dc.push()
            dc.goxy(x,y)
            dc.rect(self.dims['X'],self.dims['Y'])
            self.pad(dc)
            dc.pop()
            if i%2 == 0:
                x = -x
            elif i%2 == 1:
                y = -y
        # name pads
        nm = ['CRYSTAL','GND','CRYSTAL','GND']
        for i in range(len(self.pads)):
            self.pads[i].setname(nm[i])
        # silk outline with pin1 in bottom left
        dc.push()
        dc.left(90)
        l = max(self.dims['L'],self.dims['B']+self.dims['Y'])+self.board.silk*3
        w = max(self.dims['W'],self.dims['C']+self.dims['X'])+self.board.silk*3
        self.chamfered(dc,l,w)
        dc.pop()

class Crystal2520(Y2520):
    def escape(self,lgnd='GL2',capclass=C0402):
        brd = self.board
        capdims = capclass.dims
        for i,p in enumerate(self.pads):
            if p.name == 'GND' and self.pads[i-1] == 'CRYSTAL':
                dcp = self.pads[i-1].forward(self.dims['Y']/2)
                dcn = self.pads[i].forward(self.dims['X']/2)
                dcc = dcn.copy()
                cap = capclass(dcc.goxy(capdims['C']/2,capdims['X']/2),val='20pF')
        return

if __name__ == "__main__":
    if "output" not in os.listdir():
        os.mkdir("output")
    
    brd = cuflow.Board((20,20), trace=0.127, space=0.127,
                       via_hole=0.2, via=0.4, via_space=0.127,
                       silk=0.153)
    dc = brd.DC((10,10))
    crystal1 = Crystal2520(dc)
    crystal1.escape()
    brd.outline()
    brd.fill()
    brd.check()
    basename = "output/discrete_test"
    brd.save(basename)
    cuplot.gerbvplt(basename)
    #cuplot.gerbv(basename)
    
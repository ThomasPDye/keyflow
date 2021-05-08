# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:24:20 2021

@author: Thomas Dye
"""

import os
import cuplot
import discrete
from cuflow import cuflow

class QFN44(cuflow.Part):
    family = "U"
    footprint = "QFN44"
    dims = dict(DE=7.1,D2E2=5.4,L=0.65,b=0.3,e=0.5)
    def place(self, dc):
        # Ground pad
        dc.push()
        dc.rect(self.dims['D2E2'],self.dims['D2E2'])
        self.pad(dc)
        dc.pop()
        # silkscreen outline
        silk = self.board.silk
        self.chamfered(dc,self.dims['DE']+silk*1.5,self.dims['DE']+silk*1.5)
        # numbered pads
        for i in range(4):
            dc.left(90)
            dc.push()
            dc.forward(self.dims['DE']/2 - self.dims['L']/2)
            dc.right(90)
            dc.forward((11-1)*self.dims['e']/2)
            dc.left(180)
            self.train(dc, 11, lambda: self.rpad(dc, self.dims['b'], self.dims['L']), self.dims['e'])
            dc.pop()
        
class TQFP44(cuflow.Part):
    family = "U"
    footprint = "TQFP44"
    dims = dict(DE=12.25,D1E1=10.10,L=0.75,b=0.45,e=0.8)
    def place(self, dc):
        # silkscreen outline
        silk = self.board.silk
        self.chamfered(dc, self.dims['D1E1']+silk, self.dims['D1E1']+silk)
        # numbered pads
        for i in range(4):
            dc.left(90)
            dc.push()
            dc.forward(self.dims['DE']/2 - self.dims['L']/2)
            dc.right(90)
            dc.forward((11-1)*self.dims['e']/2)
            dc.left(180)
            self.train(dc, 11, lambda: self.rpad(dc, self.dims['b'], self.dims['L']), self.dims['e'])
            dc.pop()

ATMEGA32U4_MU_pins = [
    'GND',
    'PE6',
    'UVcc',
    'D-',
    'D+',
    'UGnd',
    'UCap',
    'VBus',
    'PB0',
    'PB1',
    'PB2',
    'PB3',
    'PB7',
    'nRESET',
    'VCC',
    'GND',
    'XTAL2',
    'XTAL1',
    'PD0',
    'PD1',
    'PD2',
    'PD3',
    'PD5',
    'GND',
    'AVCC',
    'PD4',
    'PD6',
    'PD7',
    'PB4',
    'PB5',
    'PB6',
    'PC6',
    'PC7',
    'PE2',
    'VCC',
    'GND',
    'PF7',
    'PF6',
    'PF5',
    'PF4',
    'PF1',
    'PF0',
    'AREF',
    'GND',
    'AVCC'
]

ATMEGA32U4_AU_pins = [
    'PE6',
    'UVcc',
    'D-',
    'D+',
    'UGnd',
    'UCap',
    'VBus',
    'PB0',
    'PB1',
    'PB2',
    'PB3',
    'PB7',
    'nRESET',
    'VCC',
    'GND',
    'XTAL2',
    'XTAL1',
    'PD0',
    'PD1',
    'PD2',
    'PD3',
    'PD5',
    'GND',
    'AVCC',
    'PD4',
    'PD6',
    'PD7',
    'PB4',
    'PB5',
    'PB6',
    'PC6',
    'PC7',
    'PE2',
    'VCC',
    'GND',
    'PF7',
    'PF6',
    'PF5',
    'PF4',
    'PF1',
    'PF0',
    'AREF',
    'GND',
    'AVCC'
]
        
class ATMEGA32U4_MU(QFN44):
    source = {'Microchip/Atmel' : 'ATMEGA32U4_MU'}
    mfr = 'ATMEGA32U4_MU'
    
    def escape(self,lvcc='GL3',lgnd='GL2',capclass=discrete.C0402,crystalclass=discrete.Y2520):
        brd = self.board
        assert len(ATMEGA32U4_MU_pins) == len(self.pads)
        for p,n in zip(self.pads, ATMEGA32U4_MU_pins):
            p.setname(n)
        for i,p in enumerate(self.pads):
            if p.name == 'GND' and  i != 0:
                dc = self.pads[i].copy()
                dc.right(180)
                dc.forward(self.dims['DE']/2 - self.dims['D2E2']/2 - self.dims['L']/2)
                dc.wire()
                if self.pads[i-1].name == 'VCC':
                    np = 5 - ((i-1-1)%11)
                    nn = 5 - ((i-1)%11)
                    dp = np/5
                    dn = nn/5
                    dcp = self.pads[i-1].forward(self.dims['L']/2)
                    dcn = self.pads[i].forward(self.dims['L']/2)
                    capdims = capclass.dims
                    dcc = dcn.copy()
                    pitchdelta = capdims['C'] - self.dims['e']
                    y = pitchdelta/(dp-dn)
                    x = y*dn
                    dcc.goxy(x,y)
                    cap = capclass(dcc.goxy(capdims['C']/2,capdims['X']/2),val='100nF')
                    dcn.meet(cap.pads[0])
                    dcn.wire()
                    dcp.meet(cap.pads[1])
                    dcp.wire()
                    dcncap = cap.pads[0]
                    dcpcap = cap.pads[1]
                    dcncap.goxy((capdims['X']/2 + brd.via_space + brd.via/2),0)
                    dcpcap.goxy(-(capdims['X']/2 + brd.via_space + brd.via/2),0)
                    dcncap.wire()
                    dcncap.via(lgnd)
                    dcpcap.wire()
                    dcpcap.via(lvcc)
                elif self.pads[i+1].name == 'AVCC':
                    np = 5 - ((i+1-1)%11)
                    nn = 5 - ((i-1)%11)
                    dp = np/5
                    dn = nn/5
                    dcp = self.pads[i+1].forward(self.dims['L']/2)
                    dcn = self.pads[i].forward(self.dims['L']/2)
                    capdims = capclass.dims
                    dcc = dcp.copy()
                    pitchdelta = capdims['C'] - self.dims['e']
                    y = pitchdelta/(dn-dp)
                    x = y*dp
                    dcc.goxy(x,y)
                    cap = capclass(dcc.goxy(capdims['C']/2,capdims['X']/2),val='100nF')
                    dcn.meet(cap.pads[1])
                    dcn.wire()
                    dcp.meet(cap.pads[0])
                    dcp.wire()
                    dcncap = cap.pads[1]
                    dcpcap = cap.pads[0]
                    dcncap.goxy(-(capdims['X']/2 + brd.via_space + brd.via/2),0)
                    dcpcap.goxy((capdims['X']/2 + brd.via_space + brd.via/2),0)
                    dcncap.wire()
                    dcncap.via(lgnd)
                    dcpcap.wire()
                    dcpcap.via(lvcc)
            if p.name == 'XTAL1' and self.pads[i-1].name == 'XTAL2':
                n2 = 5 - ((i-1-1)%11)
                n1 = 5 - ((i-1)%11)
                d2 = n2/5
                d1 = n1/5
                dc2 = self.pads[i-1].forward(self.dims['L']/2)
                dc1 = self.pads[i].forward(self.dims['L']/2)
                crystaldims = crystalclass.dims
                
                
class ATMEGA32U4_AU(TQFP44):
    source = {'Microchip/Atmel' : 'ATMEGA32U4_AU'}
    mfr = 'ATMEGA32U4_AU'
    def escape(self):
        brd = self.board
        assert len(ATMEGA32U4_AU_pins) == len(self.pads)
        for p,n in zip(self.pads, ATMEGA32U4_MU_pins):
            p.setname(n)
        

if __name__ == "__main__":
    if "output" not in os.listdir():
        os.mkdir("output")
    brd = cuflow.Board((20,20), trace=0.127, space=0.127,
                       via_hole=0.2, via=0.4, via_space=0.127,
                       silk=0.153)
    dc = brd.DC((10,10))
    um = ATMEGA32U4_MU(dc)
    um.escape()
    brd.outline()
    brd.fill()
    brd.check()
    basename = "output/atmega32u4_MU_Test"
    brd.save(basename)
    cuplot.gerbvplt(basename)
    #cuplot.gerbv(basename)
    
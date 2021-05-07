# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:24:20 2021

@author: Thomas Dye
"""

import os
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
    def escape(self):
        brd = self.board
        assert len(ATMEGA32U4_MU_pins) == len(self.pads)
        for p,n in zip(self.pads, ATMEGA32U4_MU_pins):
            p.setname(n)
        

        
        
class ATMEGA32U4_AU(TQFP44):
    source = {'Microchip/Atmel' : 'ATMEGA32U4_AU'}
    mfr = 'ATMEGA32U4_AU'

if __name__ == "__main__":
    if "output" not in os.listdir():
        os.mkdir("output")
    brd = cuflow.Board((50,50), trace=0.127, space=0.127,
                       via_hole=0.2, via=0.4, via_space=0.127,
                       silk=0.153)
    dc = brd.DC((25,25))
    u1 = ATMEGA32U4_MU(dc)
    u1.escape()
    brd.outline()
    brd.fill()
    brd.check()
    brd.save("output/atmega32u4_MU_Test")
    os.chdir('output')
    command = "gerbv -f #FFFFFF {0}.GTO -f #FF0000 {0}.TXT -f #a0a000 {0}.GTL -f #008000 {0}.GBL -f #202020 {0}.GML"
    os.system(command.format("atmega32u4_MU_Test"))
    os.chdir('..')
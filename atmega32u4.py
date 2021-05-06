# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:24:20 2021

@author: Thomas Dye
"""

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
        self.chamfered(dc,self.dims['DE']+0.1,self.dims['DE']+0.1)
        # numbered pads
        for i in range(4):
            dc.left(90)
            dc.push()
            dc.forward(self.dims['DE']/2 - self.dims['L']/2)
            dc.right(90)
            dc.forward(11*self.dims['e']/2)
            dc.left(180)
            self.train(dc, 11, self.rpad(dc, self.dims['b'], self.dims['L']), self.dims['e'])
            dc.pop()
        
class TQFP44(cuflow.Part):
    family = "U"
    footprint = "TQFP44"
    dims = dict(DE=12.25,D1E1=10.10,L=0.75,b=0.45,e=0.8)
    def place(self, dc):
        # silkscreen outline
        self.chamfered(dc, self.dims['D1E1']+0.1, self.dims['D1E1']+0.1)
        # numbered pads
        for i in range(4):
            dc.left(90)
            dc.push()
            dc.forward(self.dims['DE']/2 - self.dims['L']/2)
            dc.right(90)
            dc.forward(11*self.dims['e']/2)
            dc.left(180)
            self.train(dc, 11, self.rpad(dc, self.dims['b'], self.dims['L']), self.dims['e'])
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
    
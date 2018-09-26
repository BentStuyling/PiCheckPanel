# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 17:01:19 2018

@author: TQN
"""

import tkinter as tk
import time, random, Adafruit_ADS1x15
from threading import Thread

#Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1
#FANCY
class Mainframe(tk.Frame):
    # Mainframe contains the widgets
    # More advanced programs may have multiple frames
    # or possibly a grid of subframes
    
    def __init__(self,master,*args,**kwargs):
        # *args packs positional arguments into tuple args
        # **kwargs packs keyword arguments into dict kwargs
        
        # initialise base class
        tk.Frame.__init__(self,master,*args,**kwargs)
        # in this case the * an ** operators unpack the parameters
 
        # put your widgets here
        # Oil Temperature:
        tk.Label(self, text = 'Oil   [°C]:').grid(sticky = 'W', row=0, column = 0)
        self.OilTemp = tk.IntVar()
        tk.Label(self,textvariable = self.OilTemp).grid(sticky = 'W', row=0, column = 1)
        
        #pressure
        tk.Label(self, text = 'Oil [Bar]:').grid(sticky = 'W',row=0, column = 3)
        self.OilPress = tk.IntVar()
        tk.Label(self,textvariable = self.OilPress).grid(sticky = 'W',row=0, column =4)
        
        #Coolant Temperature:
        tk.Label(self, text = 'Clnt [°C]:').grid(sticky = 'W', row=1, column = 0)
        self.ClntTemp = tk.IntVar()
        tk.Label(self,textvariable = self.ClntTemp).grid(sticky = 'W', row=1, column = 1)
        
        #Battery Voltage:
        tk.Label(self, text = 'Bat [  V]:').grid(sticky = 'W', row=1, column = 3)
        self.BatVolt = tk.IntVar()
        tk.Label(self,textvariable = self.BatVolt).grid(sticky = 'W', row=1, column = 4)
         
        # call Get Temp which will call itself after a delay
        
        self.GetOilTemp()
        self.GetOilPress()
        self.GetClntTemp()
        self.GetBatVolt()
        
    def GetOilTemp(self):
        ## replace this with code to read sensor
        self.value = adc.read_adc(0, gain=GAIN)
        self.OilTemp.set(self.value)
                      
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetOilTemp)
        
    def GetOilPress(self):
        ## replace this with code to read sensor
        self.value = adc.read_adc(1, gain=GAIN)
        self.OilPress.set(self.value)
               
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetOilPress)

    def GetClntTemp(self):
        ## replace this with code to read sensor
        self.value = adc.read_adc(2, gain=GAIN)
        self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        ## replace this with code to read sensor
        self.value = adc.read_adc(3, gain=GAIN)
        self.BatVolt.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetBatVolt)
   
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
               
        # set the title bar text
        self.title('Bentron E30')
        # Make sure app window is big enough to show title 
        self.geometry("320x100")
      
        # create and pack a Mainframe window
        Mainframe(self).grid()
        
        # now start
        self.mainloop()
        
    
def func1():
    start = time.clock()
    while True:
        
        func1.rand = random.randint(1, 100)
        time.sleep(0.1)
        elapsed = time.clock()
        elapsed = elapsed - start
        if elapsed >5:
            break
        
                       
# create an App object
# it will run itself
if __name__ == '__main__':
    #Thread(target = func1).start()
    App()
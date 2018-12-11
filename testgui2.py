# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 17:01:19 2018

@author: TQN
"""

import tkinter as tk
from tkinter.font import Font
import time, random
#import Adafruit_ADS1x15
from threading import Thread

#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()
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
        LabelFont = Font(family="Times New Roman", size=23)
        
        # put your widgets here
        # Oil Temperature:
        
        tk.Label(self,   font=LabelFont, text = 'OIL  [°C]:').grid(sticky = 'W', row=0, column = 0)
        self.OilTemp = tk.IntVar()
        tk.Label(self,textvariable = self.OilTemp).grid(sticky = 'W', row=0, column = 1)
        
        #pressure
        tk.Label(self, font=LabelFont, text = 'OIL [Bar]:').grid(sticky = 'W',row=0, column = 3)
        self.OilPress = tk.IntVar()
        tk.Label(self,textvariable = self.OilPress).grid(sticky = 'W',row=0, column =4)
        
        #Coolant Temperature:
        tk.Label(self, font=LabelFont, text = 'CLNT [°C]:').grid(sticky = 'W', row=1, column = 0)
        self.ClntTemp = tk.IntVar()
        tk.Label(self,textvariable = self.ClntTemp).grid(sticky = 'W', row=1, column = 1)
        
        #Battery Voltage:
        tk.Label(self, font=LabelFont, text = 'BAT [  V]:').grid(sticky = 'W', row=1, column = 3)
        self.BatVolt = tk.IntVar()
        tk.Label(self,textvariable = self.BatVolt).grid(sticky = 'W', row=1, column = 4)
         
        # call Get Temp which will call itself after a delay
        
        self.GetOilTemp()
        self.GetOilPress()
        self.GetClntTemp()
        self.GetBatVolt()

        
    def GetOilTemp(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(0, gain=GAIN)
        self.value = random.randint(-20,120)
        self.OilTemp.set(self.value)
                      
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetOilTemp)
        
    def GetOilPress(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(1, gain=GAIN)
        self.value = random.randint(0,100)/10
        self.OilPress.set(self.value)
               
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetOilPress)

    def GetClntTemp(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(2, gain=GAIN)
        self.value = random.randint(-20,120)
        self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(3, gain=GAIN)
        self.value = random.randint(0,150)/10
        self.BatVolt.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 100
        self.after(self.TimerInterval,self.GetBatVolt)
 
        
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #Fonts
        #text = tk.Text(self)
        #Labelfont = Font(family="Times New Roman",size= 60)
        #text.configure(font=Labelfont)
        # set the title bar text
        self.title('Bentron E30')
        # Make sure app window is big enough to show title 
        self.geometry("240x320")
        #self.attributes('-fullscreen', True)
        # create Mainframe window
        self.bind('<Escape>',self.smallwindow)
        self.bind('<F11>',self.fullscreen)
            
        self.bind('<F10>',self.toggle_window)
        Mainframe(self).pack()
        # now start
        self.mainloop()    
    def toggle_window(self,event):
        Mainframe(self).destroy()

         
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry("240x320")


                      
# create an Window object
# it will run itself
if __name__ == '__main__':
    #Thread(target = func1).start()
    Window()
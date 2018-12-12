# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:00:16 2018

@author: TQN
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 17:01:19 2018

@author: TQN
"""

import tkinter as tk
from tkinter.font import Font
import  random
#import Adafruit_ADS1x15

#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()


def get_data():
    '''replace this function with whatever you want to provide the data
    for now, we just return soem random data'''
    rand_x = list(range(100))
    rand_y = [random.randrange(100) for _ in range(100)]
    return rand_x, rand_y

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
        LabelFont = Font(family="arial black", size=10, )
        Labelcolor = 'white'
        ValueFont = Font(family="Arial", size=15, weight = 'bold')
        Valuecolor = 'orange'
        UnitFont = Font(family="Arial", size=10, weight = 'bold')
        Unitcolor = 'orange'
        # Crate frames for labels and values to display
        # Title frame
        frame_lable_Title = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_Title.grid(row=0)
        frame_lable_Title.grid_propagate(0)
        # Line canvas
        linecanvas_1 = tk.Canvas(self, width = 240, height =2, bg = 'black', highlightthickness=0)
        linecanvas_1.grid(row = 1)
        linecanvas_1.grid_propagate(0)
        # First row frames for lables and values
        frame_lable_row_1 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon row frames for lables and values
        frame_lable_row_2 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width = 240, height =5, bg = 'black', highlightthickness=0)
        linecanvas_2.grid(row = 6)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Canvas(self,width = 240, height =140, bg = 'white', highlightthickness=0)
        Plotframe.grid(row=7)
        Plotframe.grid_propagate(0)
        
        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'MOTOR').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1, 240, 1, fill = 'white')
        # Oil Temperature:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'OELTEMP').place(x = 5, y =10)
        self.OilTemp = tk.IntVar()
        tk.Label(frame_value_row_1,font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilTemp).place(x = 45, y =10, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = '[°C]').place(x = 45, y =10, anchor ='w')

        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'OELDRUCK').place(x = 120, y= 10)
        self.OilPress = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilPress).place(x = 165, y =10, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = '[BAR]').place(x = 165, y =10, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'KUHLW').place(x = 5, y =10)
        self.ClntTemp = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,bg = 'black', textvariable = self.ClntTemp).place(x = 45, y =10, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = '[°C]').place(x = 45, y =10, anchor ='w')        

        #Battery Voltage:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'UBATT').place(x = 120, y= 10)
        self.BatVolt = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.BatVolt).place(x = 165, y =10, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = '[V]').place(x = 165, y =10, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 240, 4, fill = 'white')

        #Call Get [value] which will call itself after a delay
        self.GetOilTemp()
        self.GetOilPress()
        self.GetClntTemp()
        self.GetBatVolt()

        
    def GetOilTemp(self):
        ## replace this with code to read sensor
        GAIN = 1
        #self.value = adc.read_adc(0, gain=GAIN)
        self.value = random.randint(-20,120)
        self.OilTemp.set(self.value)
                      
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetOilTemp)
        
    def GetOilPress(self):
        ## replace this with code to read sensor
        GAIN = 1
        #self.value = adc.read_adc(1, gain=GAIN)
        self.value = random.randint(0,80)/10
        self.OilPress.set(self.value)
               
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetOilPress)

    def GetClntTemp(self):
        ## replace this with code to read sensor
        GAIN = 1
        #self.value = adc.read_adc(2, gain=GAIN)
        self.value = random.randint(-20,120)
        self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        ## replace this with code to read sensor
        GAIN = 1
        #self.value = adc.read_adc(3, gain=GAIN)
        self.value = random.randint(0,150)/10
        self.BatVolt.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 125
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

        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(240, 320))
        self.configure(background='black')
        #self.attributes('-fullscreen', True)
        
        # create Mainframe window
        self.bind('<Escape>',self.smallwindow)
        self.bind('<F11>',self.fullscreen)
            
        self.bind('<F10>',self.toggle_window)
        Mainframe(self).grid()
        # now start
        self.mainloop()    
    def toggle_window(self,event):
        Mainframe(self).destroy()

         
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))


                      
# create an Window object
# it will run itself
if __name__ == '__main__':
    #Thread(target = func1).start()
    Window()
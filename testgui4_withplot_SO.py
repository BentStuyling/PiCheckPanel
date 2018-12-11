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
import time, random
#import Adafruit_ADS1x15
import datetime as dt
from threading import Thread
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1
#FANCY
# Parameters


# Declare global variables
update_interval = 500 # Time (ms) between polling/animation updates
max_elements = 100     # Maximum number of elements to store in plot lists
frame = None
canvas = None
ax1 = None
temp_plot_visible = None
# Global variable to remember various states
#fullscreen = False
temp_plot_visible = True
light_plot_visible = True

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
        Plotframe = tk.Frame(self,width = 240, height =153, bg = 'black')
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
        # Lay out the main container (expand to fit window)
        #Plotframe.pack(fill=tk.BOTH, expand=1)

        # Create figure for plotting
        self.fig = figure.Figure(facecolor= 'black', figsize=(3.3, 2))
        self.fig.subplots_adjust(left=0.2, right=0.8, bottom = 0.2, top = 1)
        self.ax1 = self.fig.add_subplot(1, 1, 1, axisbg = 'black')
        
        # Instantiate a new set of axes that shares the same x-axis
        self.ax2 = self.ax1.twinx()
        
        # Empty x and y lists for storing data to plot later
        self.xs = []
        self.temps = []
        self.lights = []
        
        # Variables for holding temperature and light data
        self.temp_c = tk.DoubleVar()
        self.lux = tk.DoubleVar()
        
        # Create dynamic font for text
        #dfont = tkFont.Font(size=-24)
        
        # Create a Tk Canvas widget out of our figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        #canvas_plot = self.canvas.get_tk_widget()
        
        
        
        # Add a standard 5 pixel padding to all widgets
        for w in Plotframe.winfo_children():
            w.grid(padx=5, pady=5)
        
        # Make it so that the grid cells expand out to fill window
        for i in range(0, 5):
            Plotframe.rowconfigure(i, weight=1)
        for i in range(0, 5):
            Plotframe.columnconfigure(i, weight=1)

        # Call animate() function periodically
        self.fargs = (self.ax1, self.ax2, self.xs, self.temps, self.lights, self.temp_c, self.lux)
        self.ani = animation.FuncAnimation(  self.fig, 
                                        self.animate, 
                                        fargs=self.fargs, 
                                        interval=update_interval) 
        
    def GetOilTemp(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(0, gain=GAIN)
        self.value = random.randint(-20,120)
        self.OilTemp.set(self.value)
                      
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetOilTemp)
        
    def GetOilPress(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(1, gain=GAIN)
        self.value = random.randint(0,80)/10
        self.OilPress.set(self.value)
               
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetOilPress)

    def GetClntTemp(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(2, gain=GAIN)
        self.value = random.randint(-20,120)
        self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        ## replace this with code to read sensor
        #self.value = adc.read_adc(3, gain=GAIN)
        self.value = random.randint(0,150)/10
        self.BatVolt.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetBatVolt)
    # This function is called periodically from FuncAnimation
    def animate(self,i, ax1, ax2, xs, temps, lights, temp_c, lux):
    
        # Update data to display temperature and light values
        try:
            new_temp = random.randint(0,120)
            new_lux = random.randint(0,120)
        except:
            pass
    
        # Update our labels
        temp_c.set(new_temp)
        lux.set(new_lux)
    
        # Append timestamp to x-axis list
        timestamp = mdates.date2num(dt.datetime.now())
        xs.append(timestamp)
    
        # Append sensor data to lists for plotting
        temps.append(new_temp)
        lights.append(new_lux)
    
        # Limit lists to a set number of elements
        xs = xs[-max_elements:]
        temps = temps[-max_elements:]
        lights = lights[-max_elements:]
    
        # Clear, format, and plot light values first (behind)
        color = 'tab:orange'
        ax1.clear()
        ax1.set_ylabel('KUHLWASSERTEMP [°C]', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', labelcolor=color)
        ax1.fill_between(xs, temps, 0, linewidth=2, color=color, alpha=0.3)
    
        # Clear, format, and plot temperature values (in front)
        color = 'tab:blue'
        ax2.clear()
        ax2.set_ylabel('OELTEMP [°C]', color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.plot(xs, lights, linewidth=2, color=color)

        
        # Format timestamps to be more readable
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
        self.fig.autofmt_xdate()
    
        # Make sure plots stay visible or invisible as desired
        ax1.collections[0].set_visible(temp_plot_visible)
        ax2.get_lines()[0].set_visible(light_plot_visible)
    
    # Dummy function prevents segfault
    def _destroy(self, event):
        pass
 
        
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
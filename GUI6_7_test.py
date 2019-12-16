## Digital HUD check panel for BMW E30 based on Raspberry Pi
version = 6.7
Update_date = '(02-12-2019)'

import tkinter as tk
from tkinter.font import Font
import random, time, csv
import Adafruit_ADS1x15
import matplotlib.figure as figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import smbus2
import bme280
import socket

import pigpio, read_PWM
## reading PWM signals
RPM_GPIO = 26
pi = pigpio.pi()
rpm_signl =  read_PWM.reader(pi, RPM_GPIO)

## barometric pressure/humid/temp
calibration_params = bme280.load_calibration_params(smbus2.SMBus(1), 0x76)

##Digital pin connections and initialisation
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#Pin for buttonpush detection
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Pin for backlight brightness setting
# GPIO.setup(12, GPIO.OUT)
# pwm = GPIO.PWM(12, 1000)
# pwm.start(100)
# pwm.ChangeDutyCycle(100)

Warning = 'none'


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        #Initialize fullscreen (window resolution)
        self.attributes('-fullscreen', True)
        # Fonts
        global TitleFont
        TitleFont = Font(family='Arial', size=18, weight = 'bold')
        global LabelFont
        LabelFont = Font(family='Arial', size=16, weight = 'bold')
        global Labelcolor
        Labelcolor = 'white'
        global ValueFont
        ValueFont = Font(family="DS-Digital", size=29, weight = 'bold')
        global Valuecolor
        Valuecolor = 'orange'
        global UnitFont
        UnitFont = Font(family="DS-Digital", size=18, weight = 'bold')
        global Unitcolor
        Unitcolor = 'orange'
        
        global StatusFont
        StatusFont = Font(family='Arial', size=12, weight = 'bold')
        global StatusLabelcolor
        StatusLabelcolor = 'white'
        global StatusValuecolor
        StatusValuecolor = 'orange'
        
        # Creat key binds
        self.bind('<F9>', self.toggle_frame)
        self.bind('<F11>',self.fullscreen)
        self.bind('<F10>',self.smallwindow)
        
        # Configre window            
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(240, 320))
        self.config(cursor='none')
        #self.overrideredirect(1) # Uncomment to remove title bar
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (Status, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.config(bg="black")
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Put al frames in same loation
        # Start with this page:
        self.show_frame("PageOne")
        self.GetButton()
        self.Logging()
        #self.GetBrightness()

    def GetButton(self):
        self.pushbutton(self)
        self.TimerInterval = 100 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetButton)
        
    # def GetBrightness(self):
    #     self.value = '{:.2f}'.format(round(adc_2.read_adc(0, gain=1)*(4.069/32768)*((3.3+1)/1)*1.022, 2))
    #     self.TimerInterval = 200 # Update interval of this sensor value
    #     self.after(self.TimerInterval,self.GetBrightness)   

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
        
    def toggle_frame(self,frame_class):
        try:
            if self.pagenr ==0:
                self.show_frame("Status")
            if self.pagenr ==1:
                self.show_frame("PageOne")
            if self.pagenr ==2:
                self.show_frame("PageTwo")
            if self.pagenr ==3:
                self.show_frame("PageThree")
            
            self.pagenr = self.pagenr +1
            
            if self.pagenr == 4:
                self.pagenr = 0
        except:
            self.show_frame("PageTwo")
            self.pagenr =3
 
    def pushbutton(self,frame_class):
        if GPIO.input(11) ==1:
            try:
                print(self.switchtime) 

            except:
                self.switchtime = time.time()
                self.show_frame("PageTwo")
                self.pagenr =3
            #check if frame was not toggled to recently (time in seconds)
            if time.time()-self.switchtime > 0.5:
                if self.pagenr ==0:
                    self.show_frame("Status")
                    self.switchtime = time.time()
                if self.pagenr ==1:
                    self.show_frame("PageOne")
                    self.switchtime = time.time()
                if self.pagenr ==2:
                    self.show_frame("PageTwo")
                    self.switchtime = time.time()
                if self.pagenr ==3:
                    self.show_frame("PageThree")
                    self.switchtime = time.time()
                self.pagenr = self.pagenr +1
                if self.pagenr == 4:
                    self.pagenr = 0
    
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))
    
    def Logging(self):
        self.date = time.localtime()
        self.filename = "/home/pi/Logfiles/{}_{}_{}.csv".format(self.date.tm_year, self.date.tm_mon, self.date.tm_mday)
        with open(self.filename, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',')
            logwriter.writerow(["{}:{}:{}".format(self.date.tm_hour, self.date.tm_min, self.date.tm_sec),get_signal.ClntTemp(self), get_signal.OilTemp(self), get_signal.DiffTemp(self), get_signal.BatVolt(self), str(get_signal.OilPress(self))] )
            
        self.TimerInterval = 5000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Logging)
        
   

class Status(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Crate frames for labels and values to display
        # Title frame
        frame_lable_Title = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_Title.grid(row=0)
        frame_lable_Title.grid_propagate(0)
        # Line canvas
        linecanvas_1 = tk.Canvas(self, width = 240, height =2, bg = 'black', highlightthickness=0)
        linecanvas_1.grid(row = 1)
        linecanvas_1.grid_propagate(0)
        
        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=TitleFont, fg=Labelcolor, 
                 bg = 'black', text = 'STATUS').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,240, 1, fill = 'white', width = 2)
        # First row frames for lables and values
        frame_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_1.grid(row=2)
        frame_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
        frame_row_2 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_2.grid(row=3)
        frame_row_2.grid_propagate(0)

        # third rowd frames for lables and values
        frame_row_3 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_3.grid(row=4)
        frame_row_3.grid_propagate(0)
        
        # fourth rowd frames for lables and values
        frame_row_4 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_4.grid(row=5)
        frame_row_4.grid_propagate(0)
        
        # Fifth rowd frames for lables and values
        frame_row_5 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_5.grid(row=6)
        frame_row_5.grid_propagate(0)
        # Sixth rowd frames for lables and values
        frame_row_6 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_6.grid(row=7)
        frame_row_6.grid_propagate(0)
        # Sefeth rowd frames for lables and values
        frame_row_7 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_row_7.grid(row=8)
        frame_row_7.grid_propagate(0)

        
        # Time:
        tk.Label(frame_row_1, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Time:').place(x = 5, y =4)
        self.TimeVal= tk.IntVar()
        tk.Label(frame_row_1, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black' , textvariable = self.TimeVal).place(x =55, y =15, anchor ='w')

        #Date:
        tk.Label(frame_row_2, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Date:').place(x = 5, y= 4)
        self.DateVal = tk.IntVar()
        tk.Label(frame_row_2, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', textvariable = self.DateVal).place(x = 55, y =15, anchor ='w')
        
        #Wifi:
        tk.Label(frame_row_3, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Wifi:').place(x = 5, y= 4)
        self.Wifi= tk.IntVar()
        tk.Label(frame_row_3, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', textvariable = self.Wifi).place(x = 55, y =15, anchor ='w')
        #IP:
        tk.Label(frame_row_4, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'IP:').place(x = 5, y= 4)
        self.IP= tk.IntVar()
        tk.Label(frame_row_4, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', textvariable = self.IP).place(x = 55, y =15, anchor ='w')
         
        #Version:
        tk.Label(frame_row_5, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Ver.:').place(x = 5, y= 4)
        tk.Label(frame_row_5, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', text = version).place(x = 55, y =15, anchor ='w')         
        tk.Label(frame_row_5, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', text = Update_date).place(x = 90, y =15, anchor ='w')     
        
        #Module Temp:
        tk.Label(frame_row_6, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Module temp:').place(x = 5, y= 4)
        self.Temp = tk.IntVar()
        tk.Label(frame_row_6, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', textvariable = self.Temp).place(x = 130, y =15, anchor ='w')         
        tk.Label(frame_row_6, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', text = 'c').place(x = 173, y =15, anchor ='w')    
        
        #Module Humidity:
        tk.Label(frame_row_7, font=StatusFont, fg=StatusLabelcolor, 
                 bg = 'black', text = 'Module humid:').place(x = 5, y= 4)
        self.Humid = tk.IntVar()
        tk.Label(frame_row_7, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', textvariable = self.Humid).place(x = 135, y =15, anchor ='w')         
        tk.Label(frame_row_7, font = StatusFont, fg =StatusValuecolor,
                 bg = 'black', text = '%').place(x = 178, y =15, anchor ='w')    
        
        self.Get_time()
        self.Get_date()
        self.Get_wifi()
        self.Get_Temp()
        self.Get_Humid()
        
    def Get_time(self):
        self.date = time.localtime()
        self.value = "{}:{}:{}".format(self.date.tm_hour, self.date.tm_min, self.date.tm_sec)
        self.TimeVal.set(self.value)
        self.TimerInterval = 1000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Get_time)
    def Get_date(self):
        self.date = time.localtime()
        self.value = "{}-{}-{}".format(self.date.tm_mday, self.date.tm_mon, self.date.tm_year)
        self.DateVal.set(self.value)
        self.TimerInterval = 60000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Get_date)
        
    def Get_wifi(self):
        self.ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            #get wifi name
            output = subprocess.check_output(('grep', 'ESSID'), stdin=self.ps.stdout)
            output = str(output)
            ESSID_index = output.find('ESSID')+7
            end_index = output.find("\\")-3
            self.value= output[ESSID_index:end_index]
            if self.value == 'ff/an':
                self.Wifi.set('Not connected')
            else:
                self.Wifi.set(self.value)
        except subprocess.CalledProcessError:
            # grep did not match any lines
            self.Wifi.set(self.value)   
        try:    
            #get ip adress
            testIP = "8.8.8.8"
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((testIP, 0))
            self.ipaddr = s.getsockname()[0]
            self.IP.set(self.ipaddr)
        except:
            self.IP.set('Not connected')
        
        self.TimerInterval = 5000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Get_wifi)  
    
    def Get_Temp(self):
        self.value = get_signal.ModuleTemp(self)
        self.Temp.set(self.value)
        self.TimerInterval = 60000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Get_Temp)
    
    def Get_Humid(self):
        self.value = get_signal.ModuleHumid(self)
        self.Humid.set(self.value)
        self.TimerInterval = 60000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.Get_Humid)    
        
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        frame_lable_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
        frame_lable_row_2 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width = 240, height =10, bg = 'black', highlightthickness=0)
        linecanvas_2.grid(row = 6)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Frame(self,width = 240, height =148, bg = 'black')
        Plotframe.grid(row=7)
        Plotframe.grid_propagate(0)
        
        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=TitleFont, fg=Labelcolor, 
                 bg = 'black', text = 'MOTOR').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,240, 1, fill = 'white', width = 2)
        
        # Oil Temperature:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'ÖLTEMP').place(x = 5, y =4)
        self.ValPos_1 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black' , textvariable = self.ValPos_1).place(x = 60, y =15, anchor ='e')
        tk.Label(frame_value_row_1, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'C').place(x = 60, y =19, anchor ='w')
        
        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'ÖLDRUCK').place(x = 120, y= 4)
        self.ValPos_2 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_2).place(x = 200, y =15, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'BAR').place(x = 200, y =19, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'KUHLW.').place(x = 5, y =4)
        self.ValPos_3 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_3).place(x = 60, y =15, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'C').place(x = 60, y =19, anchor ='w')   

        #Engine RPM:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'UMW.').place(x = 120, y= 4)
        self.ValPos_4 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_4).place(x = 200, y =15, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'dc').place(x = 200, y =19, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 240, 4, fill = 'white', width = 2)

        #Call Get [value] which will call itself after a delay
        
        self.GetValPos_1()
        self.GetValPos_2()
        self.GetValPos_3()
        self.GetValPos_4()

        ##GRAPHS
        # Variables for graph plotting
        self.update_interval = 2000 # Time (ms) between polling/animation updates
        self.graph_duration = 600 # Time (s) of grap length

        # Parameters
        self.x_len = int(round(((self.graph_duration*1000)/self.update_interval),0)) # Number of points to display
        self.y1_range = [78, 107]  # Range of possible Y values to display left axis
        self.y2_range = [78, 107]  # Range of possible Y values to display right axis
        # Create graph fiugre
        self.fig = figure.Figure(facecolor= 'black', figsize=(3.25, 2),dpi=75)
        self.ax1 = self.fig.add_subplot(1, 1, 1,facecolor = 'black')
        self.fig.subplots_adjust(left=0.12, right=0.95, bottom = 0.25, top = 0.95)
        # Create a Tk Canvas widget out of figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        # Instantiate a new set of axes that shares the same x-axis
        #self.ax2 = self.ax1.twinx()
                
        # Layout of  axes
        # Axis one (left)
        # self.ax1.set_ylabel('TEMP. [C]', color=color, weight = 'bold', fontsize= 13)
        self.ax1.tick_params(axis='y', labelcolor='orange', pad = 1, length = 0,  labelsize=14,)
        self.ax1.set_yticks([80,85,90,95,100, 105])
        self.ax1.grid(linewidth=2, axis = 'y')
        self.ax1.tick_params(axis='x', labelcolor='orange', pad = 1, labelsize = 14)
        self.ax1.set_xlabel('ZEIT [s]', color='white',labelpad= 0, weight = 'bold',fontsize= 14)
        self.ax1.set_ylim(self.y1_range)
        self.ys1 = [0] * self.x_len
        self.xs = list(range(0, self.x_len))
        self.ax1.set_xticks([0 ,self.x_len/4, self.x_len/2, self.x_len/1.333, self.x_len])
        self.ax1.set_xticklabels([int(self.graph_duration),round(int(self.graph_duration)/1.3333),round(int(self.graph_duration)/2),round(int(self.graph_duration)/4),0])    
        self.fig.text(0.03, 0.03, 'KUHLW', color='tab:blue', fontsize=13, weight = 'bold')
        self.fig.text(0.87, 0.03, 'ÖL', color='tab:orange', fontsize=13, weight = 'bold')
        # Axis 2 (right)
        # color = 'tab:orange'
        # self.ax2.set_ylabel('ÖLTEMP. [C]', color=color, weight = 'bold',fontsize= 13)
        # self.ax2.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, labelsize=10)
        # self.ax2.tick_params(axis='x', labelcolor=color, pad = 0,labelsize=10)
        # self.ax2.set_ylim(self.y2_range)
        self.ys2 = [0] * self.x_len
        # PLot lines
        color = 'tab:blue'
        self.line1, = self.ax1.plot(self.xs, self.ys1,linewidth=3, color=color)
        color = 'tab:orange'
        self.line2, = self.ax1.plot(self.xs, self.ys2,linewidth=3, color=color)
        
       

        
        #Add all elements to frame
        for w in Plotframe.winfo_children():
            w.grid(padx =0, pady =0)

        # Call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig,
            self.animate,
            fargs=(self.ys1,self.ys2,self.x_len, self.line1, self.line2),
            interval=self.update_interval,
            blit=True)

            
    def GetValPos_1(self):
        self.value = get_signal.OilTemp(self)
        # if self.value > 110:
        #     self.bg_Pos_1.set('red')
        # else:
        #     self.bg_Pos_1.set('black')
        if self.value == "--":
            self.ValPos_1.set(self.value)
        else:
            self.ValPos_1.set(round(self.value))
        

        self.TimerInterval = 3000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_1)
    
    def GetValPos_2(self):
        self.value = get_signal.OilPress(self)
        if self.value == "--":
            self.ValPos_2.set(self.value)
        else:
            self.ValPos_2.set(self.value)
        self.TimerInterval = 175 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_2)   
        
    def GetValPos_3(self):
        self.value = get_signal.ClntTemp(self)
        if self.value == "--":
            self.ValPos_3.set(self.value)
        else:
            self.ValPos_3.set(round(self.value))
        self.TimerInterval = 3000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_3)
    
    # def GetValPos_4(self):
    #     self.ValPos_4.set(get_signal.BatVolt(self))
    #     self.TimerInterval = 175 # Update interval of this sensor value
    #     self.after(self.TimerInterval,self.GetValPos_4)
    def GetValPos_4(self):
        self.value = get_signal.EngineRPM(self)
        if self.value == "--":
            self.ValPos_4.set(self.value)
        else:
            self.ValPos_4.set(round(self.value,1)) 
        self.TimerInterval = 175 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_4)        
    
    # This function is called periodically from FuncAnimation  
    def animate(self, i, ys1, ys2, x_len, line1, line2):
        # Append new sensor value to line plot list.
        Temp1 = get_signal.ClntTemp(self)
        Temp2 = get_signal.OilTemp(self)
        
        if Temp1 == "--":
            ys1.append(199)
        else:
            ys1.append(Temp1)
        
        if Temp2 == "--":
            ys2.append(199)
        else:
            ys2.append(Temp2)

        # Limit y list to set number of items
        ys1 = ys1[-self.x_len:]
        ys2 = ys2[-self.x_len:]
        # Update line with new Y values
        line1.set_ydata(ys1)
        line2.set_ydata(ys2)
        return line1, line2,

    
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        frame_lable_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
        frame_lable_row_2 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width = 240, height =10, bg = 'black', highlightthickness=0)
        linecanvas_2.grid(row = 6)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Frame(self,width = 240, height =148, bg = 'black')
        Plotframe.grid(row=7)
        Plotframe.grid_propagate(0)
        
        # put your widgets here
        # screen title
        self.Title = tk.IntVar()
        tk.Label(frame_lable_Title, font=TitleFont, fg=Labelcolor, 
                 bg = 'black', textvariable = self.Title).place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,240, 1, fill = 'white', width = 2)
        # Oil Temperature:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'ACHSE').place(x = 5, y =4)
        self.ValPos_1 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_1).place(x = 60, y =15, anchor ='e')
        tk.Label(frame_value_row_1, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'C').place(x = 60, y =19, anchor ='w')
        
        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'GETRIEBE').place(x = 120, y= 4)
        self.ValPos_2 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_2).place(x = 180, y =15, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'C').place(x = 180, y =19, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'KUHLW.').place(x = 5, y =4)
        self.ValPos_3 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_3).place(x = 60, y =15, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'C').place(x = 60, y =19, anchor ='w')   

        #Battery Voltage:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'UBATT').place(x = 120, y= 4)
        self.ValPos_4 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_4).place(x = 180, y =15, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'V').place(x = 180, y =19, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 240, 4, fill = 'white', width = 2)

        #Call Get [value] which will call itself after a delay
        self.GetTitle()
        self.GetValPos_1()
        self.GetValPos_2()
        self.GetValPos_3()
        self.GetValPos_4()

        ##GRAPHS
        # Variables for graph plotting
        self.update_interval = 2000 # Time (ms) between polling/animation updates
        self.graph_duration = 600 # Time (s) of grap length

        # Parameters
        self.x_len = int(round(((self.graph_duration*1000)/self.update_interval),0)) # Number of points to display
        self.y1_range = [38, 102]  # Range of possible Y values to display left axis
        self.y2_range = [38, 102]  # Range of possible Y values to display right axis
        # Create graph fiugre
        self.fig = figure.Figure(facecolor= 'black', figsize=(3.25, 2),dpi=75)
        self.ax1 = self.fig.add_subplot(1, 1, 1,facecolor = 'black')
        self.fig.subplots_adjust(left=0.12, right=0.95, bottom = 0.25, top = 0.95)
        # Create a Tk Canvas widget out of figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        # Instantiate a new set of axes that shares the same x-axis
        #self.ax2 = self.ax1.twinx()
                
        # Layout of  axes
        # Axis one (left)
        # self.ax1.set_ylabel('TEMP. [C]', color=color, weight = 'bold', fontsize= 13)
        self.ax1.tick_params(axis='y', labelcolor='orange', pad = 1, length = 0,  labelsize=14,)
        self.ax1.set_yticks([40,50,60,70,80,90,100])
        self.ax1.grid(linewidth=2, axis = 'y')
        self.ax1.tick_params(axis='x', labelcolor='orange', pad = 1, labelsize = 14)
        self.ax1.set_xlabel('ZEIT [s]', color='white',labelpad= 0, weight = 'bold',fontsize= 14)
        self.ax1.set_ylim(self.y1_range)
        self.ys1 = [0] * self.x_len
        self.xs = list(range(0, self.x_len))
        self.ax1.set_xticks([0 ,self.x_len/4, self.x_len/2, self.x_len/1.333, self.x_len])
        self.ax1.set_xticklabels([int(self.graph_duration),round(int(self.graph_duration)/1.3333),round(int(self.graph_duration)/2),round(int(self.graph_duration)/4),0])    
        self.fig.text(0.03, 0.03, 'ACHSE', color='tab:blue', fontsize=13, weight = 'bold')
        self.fig.text(0.68, 0.03, 'GETRIEBE', color='tab:orange', fontsize=13, weight = 'bold')
        # Axis 2 (right)
        # color = 'tab:orange'
        # self.ax2.set_ylabel('ÖLTEMP. [C]', color=color, weight = 'bold',fontsize= 13)
        # self.ax2.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, labelsize=10)
        # self.ax2.tick_params(axis='x', labelcolor=color, pad = 0,labelsize=10)
        # self.ax2.set_ylim(self.y2_range)
        self.ys2 = [0] * self.x_len
        # PLot lines
        color = 'tab:blue'
        self.line1, = self.ax1.plot(self.xs, self.ys1,linewidth=3, color=color)
        color = 'tab:orange'
        self.line2, = self.ax1.plot(self.xs, self.ys2,linewidth=3, color=color)
        
       

        
        #Add all elements to frame
        for w in Plotframe.winfo_children():
            w.grid(padx =0, pady =0)

        # Call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig,
            self.animate,
            fargs=(self.ys1,self.ys2,self.x_len, self.line1, self.line2),
            interval=self.update_interval,
            blit=True)

    def GetTitle(self):
        if Warning == 'none':
            self.Title.set('ANTRIEB')
        else:
            self.Title.set(Warning)
        self.TimerInterval = 1000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetTitle)
                
    def GetValPos_1(self):
        self.value = get_signal.DiffTemp(self)
        if self.value == "--":
            self.ValPos_1.set(self.value)
        else:
            self.ValPos_1.set(round(self.value))
        self.TimerInterval = 3000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_1)
    
    def GetValPos_2(self):
        self.value = get_signal.GetriebeTemp(self)
        if self.value == "--":
            self.ValPos_2.set(self.value)
        else:
            self.ValPos_2.set(round(self.value))
        self.TimerInterval = 3000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_2)   
        
    def GetValPos_3(self):
        self.value = get_signal.ClntTemp(self)
        if self.value == "--":
            self.ValPos_3.set(self.value)
        else:
            self.ValPos_3.set(round(self.value))
        self.TimerInterval = 3000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_3)
    
    def GetValPos_4(self):
        self.ValPos_4.set(get_signal.BatVolt(self))
        self.TimerInterval = 175 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_4)      
    
    # This function is called periodically from FuncAnimation  
    def animate(self, i, ys1, ys2, x_len, line1, line2):
        # Append new sensor value to line plot list.
        Temp2 = get_signal.GetriebeTemp(self)
        Temp1 = get_signal.DiffTemp(self)
        
        if Temp1 == "--":
            ys1.append(199)
        else:
            ys1.append(Temp1)
        
        if Temp2 == "--":
            ys2.append(199)
        else:
            ys2.append(Temp2)

        # Limit y list to set number of items
        ys1 = ys1[-self.x_len:]
        ys2 = ys2[-self.x_len:]
        # Update line with new Y values
        line1.set_ydata(ys1)
        line2.set_ydata(ys2)
        return line1, line2,
    
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        frame_lable_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
        frame_lable_row_2 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Third rowd frames for lables and values
        frame_lable_row_3 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_lable_row_3.grid(row=6)
        frame_lable_row_3.grid_propagate(0)
        frame_value_row_3 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_value_row_3.grid(row=7)
        frame_value_row_3.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width = 240, height =10, bg = 'black', highlightthickness=0)
        linecanvas_2.grid(row = 8)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Frame(self,width = 240, height =148, bg = 'black')
        Plotframe.grid(row=9)
        Plotframe.grid_propagate(0)
        
        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=TitleFont, fg=Labelcolor, 
                 bg = 'black', text = 'UMGEBUNG').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,240, 1, fill = 'white', width = 2)
        
        # Pressure:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'LUFTDRUCK').place(x = 5, y =4)
        self.ValPos_1 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black' , textvariable = self.ValPos_1).place(x = 5, y =15, anchor ='w')
        tk.Label(frame_value_row_1, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'hPa').place(x = 105, y =19, anchor ='w')
        # Altitude
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'HÖHE').place(x = 5, y =4)
        self.ValPos_2 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,
                 bg = 'black' , textvariable = self.ValPos_2).place(x = 5, y =15, anchor ='w')
        tk.Label(frame_value_row_2, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'm').place(x = 112, y =19, anchor ='w')    
        # Outsidetemperature
        tk.Label(frame_lable_row_3, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'AUSSENTEMP').place(x = 5, y =4)
        self.ValPos_3 = tk.IntVar()
        tk.Label(frame_value_row_3, font = ValueFont, fg =Valuecolor,
                 bg = 'black' , textvariable = self.ValPos_3).place(x = 5, y =15, anchor ='w')
        tk.Label(frame_value_row_3, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'C').place(x = 112, y =19, anchor ='w') 
        
        self.GetValPos_1() #In this caseValpos_1 (Pressure), ValPos_2 (altutude) and ValPos_3 (outside temp) as well
    
    def GetValPos_1(self):
        #pressure
        self.press= get_signal.AirPressure(self)
        self.ValPos_1.set(self.press) # set value to display
        #Altitude:
        self.QNH = 1013.25 #Standard pressure at sealevel
        self.temp=get_signal.OutsiteTemp(self)  #get outsite air temperature
        self.ValPos_3.set(self.temp)# set value to display
        self.altitude = round(((self.temp+273.15)/0.0065)*(pow(self.QNH/self.press,0.190234)-1),1) # 10 should be the actual outside temperature
        self.ValPos_2.set(self.altitude)  # set value to display
        self.TimerInterval = 5000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_1)

## sensors    
#Create an ADS1015 ADC (12-bit) instance.
adc_1 = Adafruit_ADS1x15.ADS1115(address=0x48) 
adc_2 = Adafruit_ADS1x15.ADS1115(address=0x49)
adc_3 = Adafruit_ADS1x15.ADS1115(address=0x4a)
adc_4 = Adafruit_ADS1x15.ADS1115(address=0x4b)
## Create instances of sensors:    
Vin = 5.25
class get_signal:

    def OilTemp(self):
        # self.U = random.uniform(3,5)
        self.U= (4.096/32768)*adc_1.read_adc(1, gain=1)
        self.R= 330*((Vin/self.U)-1)
        if 1 < self.R <24000:
            self.temp = (480608.65298)/(1 + (self.R/(2.876073*10**-17))**0.1812132) -96.85298
            self.value= round(self.temp,2)
            if self.value >80:
                global Warning 
                Warning = 'High Oiltemp'
                print(Warning)
            return self.value
        else:
            self.value = "--"
            return self.value

    def OilPress(self):
        self.newvalue = round(random.uniform(0,80)/10,1)
        #self.newvalue = abs(round((((4.096/32768)*adc_1.read_adc(0, gain=1)-0.475)/4)*9,1))
        try:
            self.value = round(self.oldvalue*0.3 + self.newvalue*0.7,1)
        except:
            self.value = round(self.newvalue,1)
        self.oldvalue = self.value
        return self.value
        
    def FuelPress(self):
        # self.value = round(random.uniform(0,80)/10,1)
        self.value = abs(round((((4.096/32768)*adc_2.read_adc(3, gain=1)-0.475)/4)*9,1))
        return self.value   

    def ClntTemp(self):
        # self.U = random.uniform(3,4)
        self.U= (4.096/32768)*adc_1.read_adc(2, gain=1)
        self.R= 330*((Vin/self.U)-1)
        if 1 < self.R <24000:
            self.temp =  (211749.2077)/(1 + (self.R/(1.274787*10**-14))**0.185661) -113.7
            self.value= round(self.temp,2)
            return self.value
        else:
            self.value = "--"
            return self.value
    
    def BatVolt(self):
        # self.value = '{:.2f}'.format(round(random.uniform(0,14),2))
        self.value = '{:.1f}'.format(round(adc_1.read_adc(3, gain=1)*(4.069/32768)*((3.3+1)/1)*1.022, 1))
        return self.value  

    def DiffTemp(self):
        # self.U = random.uniform(0,4)
        self.U= (4.096/32768)*adc_2.read_adc(1, gain=1)
        self.R= 330*((Vin/self.U)-1)
        if 1 < self.R <24000:
            self.temp =  (480608.65298)/(1 + (self.R/(2.876073*10**-17))**0.1812132) -96.85298
            self.value= round(self.temp,2)
            return self.value
        else:
            self.value = "--"
            return self.value        

    def GetriebeTemp(self):
        # self.U = random.uniform(0,4)
        self.U= (4.096/32768)*adc_2.read_adc(2, gain=1)
        self.R= 330*((Vin/self.U)-1)
        if 1 < self.R <24000:
            self.temp =  (480608.65298)/(1 + (self.R/(2.876073*10**-17))**0.1812132) -96.85298
            self.value= round(self.temp,2)
            return self.value
        else:
            self.value = "--"
            return self.value    
    
    def AirPressure(self):
        self.data = bme280.sample(smbus2.SMBus(1), 0x76, calibration_params)
        #Pressure:
        self.value = round(self.data.pressure,1)
        return self.value
    
    def ModuleTemp(self):
        self.data = bme280.sample(smbus2.SMBus(1), 0x76, calibration_params)
        #Temperature
        self.value = round(self.data.temperature,1)
        return self.value
    
    def ModuleHumid(self):
        self.data = bme280.sample(smbus2.SMBus(1), 0x76, calibration_params)
        #Humidity
        self.value = round(self.data.humidity,1)
        return self.value
    
    def OutsiteTemp(self):
        try:
            self.device_file = '/sys/bus/w1/devices/28-0114382f22aa/w1_slave'
            self.f = open(self.device_file, 'r')
            self.lines = self.f.readlines()
            self.f.close()
            
            while self.lines[0].strip()[-3:] != 'YES':
                #time.sleep(0.2)
                self.lines = read_temp_raw()
            self.equals_pos = self.lines[1].find('t=')
            if self.equals_pos != -1:
                self.temp_string = self.lines[1][self.equals_pos+2:]
                self.value = round(float(self.temp_string) / 1000.0,1)
        except:
            self.value = 20
        
        return self.value
    
    def EngineRPM(self):
        try:
            self.p = rpm_signl
            self.f = self.p.frequency()
            self.pw = self.p.pulse_width()
            self.dc = self.p.duty_cycle()
            # self.value = self.f*60,0
            self.value = self.dc
        except:
            self.value = '--'
        return self.value
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

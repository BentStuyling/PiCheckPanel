import tkinter as tk
from tkinter.font import Font
import random, time
#import Adafruit_ADS1x15
import matplotlib.figure as figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        # Fonts
        global LabelFont
        LabelFont = Font(family='Arial', size=13, weight = 'bold')
        global Labelcolor
        Labelcolor = 'white'
        global ValueFont
        ValueFont = Font(family="DS-Digital", size=22, weight = 'bold')
        global Valuecolor
        Valuecolor = 'orange'
        global UnitFont
        UnitFont = Font(family="DS-Digital", size=15, weight = 'bold')
        global Unitcolor
        Unitcolor = 'orange'
        
        # Creat key binds
        self.bind('<Escape>',self.Destroy)
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
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Put al frames in same loation
        # Start with this page:
        self.show_frame("PageOne")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def toggle_frame(self,frame_class):
        
        try:
            if self.pagenr ==0:
                self.show_frame("StartPage")
            if self.pagenr ==1:
                self.show_frame("PageOne")
            if self.pagenr ==2:
                self.show_frame("PageTwo")
            
            self.pagenr = self.pagenr +1
            
            if self.pagenr == 3:
                self.pagenr = 0
        except:
            self.show_frame("PageTwo")
            self.pagenr =0
 
    def Destroy(self):
        self.destroy()
                
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page").pack()
        
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
        frame_lable_row_1 = tk.Frame(self,width = 240, height =35, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 240, height =30, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
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
        tk.Label(frame_lable_Title, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'MOTOR').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,240, 1, fill = 'white', width = 2)
        # Oil Temperature:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'ÖLTEMP').place(x = 15, y =10)
        self.ValPos_1 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_1).place(x = 55, y =10, anchor ='e')
        tk.Label(frame_value_row_1, font = UnitFont, fg =Unitcolor,
                 bg = 'black',text = 'C').place(x = 55, y =14, anchor ='w')
        
        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'ÖLDRUCK').place(x = 130, y= 10)
        self.ValPos_2 = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_2).place(x = 175, y =10, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'BAR').place(x = 175, y =14, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'KUHLW.').place(x = 15, y =10)
        self.ValPos_3 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_3).place(x = 55, y =10, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'C').place(x = 55, y =14, anchor ='w')        

        #Battery Voltage:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'UBATT').place(x = 130, y= 10)
        self.ValPos_4 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_4).place(x = 175, y =10, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'V').place(x = 175, y =14, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 2, 240, 2, fill = 'black')
                
       
        
        
        #Call Get [value] which will call itself after a delay
        self.GetValPos_1()
        self.GetValPos_2()
        self.GetValPos_3()
        self.GetValPos_4()
        
        ##GRAPHS
        # Variables for graph plotting
        self.update_interval = 2000 # Time (ms) between polling/animation updates
        self.graph_duration = 60 # Time (s) of grap length

        # Parameters
        self.x_len = int(round(((self.graph_duration*1000)/self.update_interval),0)) # Number of points to display
        self.y1_range = [-10, 120]  # Range of possible Y values to display left axis
        self.y2_range = [-10, 120]  # Range of possible Y values to display right axis
        # Create graph fiugre
        self.fig = figure.Figure(facecolor= 'black', figsize=(3.25, 2),dpi=75)
        self.ax1 = self.fig.add_subplot(1, 1, 1,facecolor = 'black')
        self.fig.subplots_adjust(left=0.18, right=0.8, bottom = 0.2, top = 0.95)
        # Create a Tk Canvas widget out of figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        # Instantiate a new set of axes that shares the same x-axis
        self.ax2 = self.ax1.twinx()
                
        # Layout of  axes
        # Axis one (left)
        color = 'tab:blue'
        self.ax1.set_ylabel('KUHLW.TEMP. [C]', color=color, weight = 'bold')
        self.ax1.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, gridOn = True)
        color = 'tab:orange'
        self.ax1.tick_params(axis='x', labelcolor=color, pad = 0)
        self.ax1.set_xlabel('ZEIT [s]', color=color,labelpad= 0, weight = 'bold',)
        self.ax1.set_ylim(self.y1_range)
        self.ys1 = [0] * self.x_len
        self.xs = list(range(0, self.x_len))
        self.ax1.set_xticks([0,self.x_len])
        self.ax1.set_xticklabels([int(self.graph_duration),0])    
        
        # Axis 2 (right)
        color = 'tab:orange'
        self.ax2.set_ylabel('ÖLTEMP. [C]', color=color, weight = 'bold')
        self.ax2.tick_params(axis='y', labelcolor=color, pad = 1, length = 0)
        self.ax2.tick_params(axis='x', labelcolor=color, pad = 0)
        self.ax2.set_ylim(self.y2_range)
        self.ys2 = [0] * self.x_len
        # PLot lines
        color = 'tab:blue'
        self.line1, = self.ax1.plot(self.xs, self.ys1,linewidth=1, color=color)
        color = 'tab:orange'
        self.line2, = self.ax2.plot(self.xs, self.ys2,linewidth=1, color=color)
       

        
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
        self.ValPos_1.set(get_signal.OilTemp(self))
        self.TimerInterval = 1000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_1)
    
    def GetValPos_2(self):
        self.ValPos_2.set(get_signal.OilPress(self))
        self.TimerInterval = 125 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_2)   
        
    def GetValPos_3(self):
        self.ValPos_3.set(get_signal.ClntTemp(self))
        self.TimerInterval = 1000 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_3)
    
    def GetValPos_4(self):
        self.ValPos_4.set(get_signal.BatVolt(self))
        self.TimerInterval = 125 # Update interval of this sensor value
        self.after(self.TimerInterval,self.GetValPos_4)      
    
    # This function is called periodically from FuncAnimation  
    def animate(self, i, ys1, ys2, x_len, line1, line2):
        # Append new sensor value to line plot list.
        ys1.append(get_signal.ClntTemp(self))
        ys2.append(get_signal.OilTemp(self))

        # Limit y list to set number of items
        ys1 = ys1[-self.x_len:]
        ys2 = ys2[-self.x_len:]
        # Update line with new Y values
        line1.set_ydata(ys1)
        line2.set_ydata(ys2)
     
        return line1, line2,

    
class PageTwo(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller = controller


## sensors    
#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, bus=1) #change bus in case of multiple ADC's
## Create instances of sensors:    
class get_signal:
    def OilTemp(self):
        #self.value = adc.read_adc(0, gain=1)     
        self.value = random.randint(-20, 120)
        return self.value

    def OilPress(self):
        #self.value = abs(round((((4.096/2047)*adc.read_adc(1, gain=1)-0.475)/4)*9,1))
        self.value = random.randint(0,80)/10
        return self.value    

    def ClntTemp(self):
        self.R = random.randint(200,10000)
        #self.U= round((4.096/2047)*adc.read_adc(2, gain=1),2)
        #self.R = ((5*220)/self.U)-220
        #Rlu = [10000, 2600, 340, 200, 100]
        #Tlu = [-10, 20, 80, 100, 120]
            
        if self.R >= 2600:
            self.value = int(-10+(30.0)*((self.R-10000.0)/(2600.0-10000.0)))
        elif self.R >= 340:
            self.value = int(20+(60.0)*((self.R-2600.0)/(340.0-2600.0)))
        elif self.R >= 200:
            self.value = int(80+(20.0)*((self.R-340.0)/(200.0-340.0)))
        elif self.R >= 100:  
            self.value = int(100+(20.0)*((self.R-200.0)/(100.0-200.0)))
        else:  
            print('Coolant sensor out of range')
        return self.value 

    def BatVolt(self):
        #self.value = adc.read_adc(3, gain=1)
        self.value = random.randint(0,150)/10
        return self.value  
    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

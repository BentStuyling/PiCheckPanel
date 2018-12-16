import tkinter as tk
from tkinter.font import Font
import random, time
#import Adafruit_ADS1x15
import matplotlib.figure as figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()
global ActivePage

 
class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.switch_frame(StartPage)
        # Fonts
        global LabelFont
        LabelFont = Font(family='Arial', size=25, weight = 'bold')
        global Labelcolor
        Labelcolor = 'white'
        global ValueFont
        ValueFont = Font(family="DS-Digital", size=45, weight = 'bold')
        global Valuecolor
        Valuecolor = 'orange'
        global UnitFont
        UnitFont = Font(family="DS-Digital", size=30, weight = 'bold')
        global Unitcolor
        Unitcolor = 'orange'    
      
        # set the title bar text
        self.title('Bentron E30')
        # Uncomment to remove title bar:
        #self.overrideredirect(1)
        # Configre window            
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(480, 640))
        #self.configure(background='white')
        # Creat key binds
        self.bind('<Escape>',self.Destroy)
        self.bind('<F11>',self.fullscreen)
        self.bind('<F10>',self.smallwindow)
        # create Mainframe window
        
     
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def Destroy(self,event):
        self.switch_frame(StartPage)
        
         
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))
        

class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        
        #Fonts
        label = tk.Label(self, text="This is the start page")
        self.configure(background='black')
        label.pack(side="top", fill="x", pady=10)
        print('stamp')
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()

class PageOne(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.bind('<F9>',self.test)

        

    
    
        # Crate frames for labels and values to display
        # Title frame
        frame_lable_Title = tk.Frame(self,width = 480, height =60, bg = 'black')
        frame_lable_Title.grid(row=0)
        frame_lable_Title.grid_propagate(0)
        # Line canvas
        linecanvas_1 = tk.Canvas(self, width = 480, height =4, bg = 'black', highlightthickness=0)
        linecanvas_1.grid(row = 1)
        linecanvas_1.grid_propagate(0)
        # First row frames for lables and values
        frame_lable_row_1 = tk.Frame(self,width = 480, height =70, bg = 'black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self,width = 480, height =60, bg = 'black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon row frames for lables and values
        frame_lable_row_2 = tk.Frame(self,width = 480, height =70, bg = 'black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self,width = 480, height =60, bg = 'black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width = 480, height =10, bg = 'black', highlightthickness=0)
        linecanvas_2.grid(row = 6)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Frame(self,width = 480, height =306, bg = 'black')
        Plotframe.grid(row=7)
        Plotframe.grid_propagate(0)
        
        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'MOTOR').place(relx = .5, rely =0.5, anchor = 'center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1,480, 1, fill = 'white', width = 2)
        # Oil Temperature:
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'ÖLTEMP').place(x = 30, y =20)
        self.OilTemp = tk.IntVar()
        tk.Label(frame_value_row_1,font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilTemp).place(x = 110, y =20, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'C').place(x = 110, y =28, anchor ='w')

        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'ÖLDRUCK').place(x = 260, y= 20)
        self.OilPress = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilPress).place(x = 350, y =20, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'BAR').place(x = 350, y =28, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'KUHLW.').place(x = 30, y =20)
        self.ClntTemp = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,bg = 'black', textvariable = self.ClntTemp).place(x = 110, y =20, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'C').place(x = 110, y =28, anchor ='w')        

        #Battery Voltage:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'UBATT').place(x = 260, y= 20)
        self.BatVolt = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.BatVolt).place(x = 350, y =20, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'V').place(x = 350, y =28, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 480, 4, fill = 'black')
        
        # Variables for graph plotting
        self.update_interval = 2000 # Time (ms) between polling/animation updates
        self.graph_duration = 60 # Time (s) of grap length

        
        # Parameters
        self.x_len = int(round(((self.graph_duration*1000)/self.update_interval),0))      # Number of points to display
        self.y1_range = [-10, 120]  # Range of possible Y values to display left axis
        self.y2_range = [-10, 120]  # Range of possible Y values to display right axis
        # Create graph fiugre
        self.fig = figure.Figure( facecolor= 'black', figsize=(3.3, 2),dpi=150)
        self.ax1 = self.fig.add_subplot(1, 1, 1,facecolor = 'black')
        self.fig.subplots_adjust(left=0.18, right=0.8, bottom = 0.2, top = 0.95)
        # Instantiate a new set of axes that shares the same x-axis
        self.ax2 = self.ax1.twinx()
        
        
        # Layout of  axes
        # Axis one (left)
        color = 'tab:blue'
        self.ax1.set_ylabel('KUHLW.TEMP. [C]', color=color, weight = 'bold')
        self.ax1.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, gridOn = True)
        color = 'tab:orange'
        self.ax1.tick_params(axis='x', labelcolor=color, pad = 0)
        self.ax1.set_xlabel('TIME [s]', color=color,labelpad= 0, weight = 'bold',)
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
        
        color = 'tab:blue'
        self.line1, = self.ax1.plot(self.xs, self.ys1,linewidth=1, color=color)
        color = 'tab:orange'
        self.line2, = self.ax2.plot(self.xs, self.ys2,linewidth=1, color=color)
        
        
        
        # Create a blank line. We will update the line in animate
        
       
        
        # Create a Tk Canvas widget out of our figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        #canvas_plot = self.canvas.get_tk_widget()

        # Add a standard 1 pixel padding to all widgets
        for w in Plotframe.winfo_children():
            w.grid(padx=1, pady=1)

        #Call Get [value] which will call itself after a delay
        self.GetOilTemp()
        self.GetOilPress()
        self.GetClntTemp()
        self.GetBatVolt()
        

        
        # Call animate() function periodically
        
        self.ani = animation.FuncAnimation(self.fig,
            self.animate,
            fargs=(self.ys1,self.ys2,self.x_len, self.line1, self.line2),
            interval=self.update_interval,
            blit=True)
        
    def GetOilTemp(self):
        GAIN = 1
        #self.value = adc.read_adc(0, gain=GAIN)
        self.value = random.randint(-20,120)
        self.OilTemp.set(self.value)
                      
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetOilTemp)
        
    def GetOilPress(self):
        #self.value = abs(round((((4.096/2047)*adc.read_adc(1, gain=1)-0.475)/4)*9,1))
        self.value = random.randint(0,80)/10
        self.OilPress.set(self.value)
               
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetOilPress)

    def GetClntTemp(self):
        self.R = random.randint(200,10000)
        #self.U= round((4.096/2047)*adc.read_adc(2, gain=1),2)
        #self.R = ((5*220)/self.U)-220
        Rlu = [10000, 2600, 340, 200, 100]
        Tlu = [10, 20, 80, 100, 120]
        if self.R >= 2600:
            self.ClntTemp.set(int(-10+(30.0)*((self.R-10000.0)/(2600.0-10000.0))))
        elif self.R >= 340:
            self.ClntTemp.set(int(20+(60.0)*((self.R-2600.0)/(340.0-2600.0))))
        elif self.R >= 200:
            self.ClntTemp.set(int(80+(20.0)*((self.R-340.0)/(200.0-340.0))))
        elif self.R >= 100:  
            self.ClntTemp.set(int(100+(20.0)*((self.R-200.0)/(100.0-200.0))))
        else:  
            print('clt sensor out of range')
        #self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 1000
        
       
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        GAIN = 1
        #self.value = adc.read_adc(3, gain=GAIN)
        self.value = random.randint(0,150)/10
        self.BatVolt.set(self.value)
        self.BatVolt
                      
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetBatVolt)
    
    # This function is called periodically from FuncAnimation
    def animate(self, i, ys1, ys2, x_len, line1, line2):
        try:
            new_value1 = random.randint(-10,120)
            new_value2 = random.randint(-10,120)
        except:
            pass
        print('running')
        # Add y to list
        ys1.append(new_value1)
        ys2.append(new_value2)

        # Limit y list to set number of items
        ys1 = ys1[-self.x_len:]
        ys2 = ys2[-self.x_len:]
        # Update line with new Y values
        line1.set_ydata(ys1)
        line2.set_ydata(ys2)
     
        return line1, line2,
    
    def test(self,event):
        master.switch_frame(StartPage).pack()

class PageTwo(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #self.GetOilPress()
        label = tk.Label(self, text='two')
        label.pack(side="top", fill="x", pady=10)

        
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        


if __name__ == "__main__":
    
    app = MainApp()
    app.mainloop()

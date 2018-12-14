import tkinter as tk
from tkinter.font import Font
import random, time
#import Adafruit_ADS1x15
import datetime as dt
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

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
        LabelFont = Font(family="Arial", size=25, weight = 'bold' )
        Labelcolor = 'white'
        ValueFont = Font(family="DS-Digital", size=45, weight = 'bold')
        Valuecolor = 'orange'
        UnitFont = Font(family="DS-Digital", size=30, weight = 'bold')
        Unitcolor = 'orange'
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
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'OELTEMP').place(x = 10, y =20)
        self.OilTemp = tk.IntVar()
        tk.Label(frame_value_row_1,font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilTemp).place(x = 90, y =20, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'C').place(x = 90, y =28, anchor ='w')

        #pressure
        tk.Label(frame_lable_row_1, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'OELDRUCK').place(x = 240, y= 20)
        self.OilPress = tk.IntVar()
        tk.Label(frame_value_row_1, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.OilPress).place(x = 330, y =20, anchor ='e')
        tk.Label(frame_value_row_1,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'BAR').place(x = 330, y =28, anchor ='w')        

        #Coolant Temperature:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'KUHLW.').place(x = 10, y =20)
        self.ClntTemp = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont,fg =Valuecolor,bg = 'black', textvariable = self.ClntTemp).place(x = 90, y =20, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'C').place(x = 90, y =28, anchor ='w')        

        #Battery Voltage:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, bg = 'black', text = 'UBATT').place(x = 240, y= 20)
        self.BatVolt = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,bg = 'black', textvariable = self.BatVolt).place(x = 330, y =20, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,bg = 'black', text = 'V').place(x = 330, y =28, anchor ='w')        

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 480, 4, fill = 'black')
        
        # Graph plotting section:
        # Create figure for plotting
        self.fig = figure.Figure(facecolor= 'black', figsize=(3.3, 2), dpi =150)
        self.fig.subplots_adjust(left=0.18, right=0.8, bottom = 0.2, top = 0.95)
        self.ax1 = self.fig.add_subplot(1, 1, 1, facecolor = 'black')
        
        # Instantiate a new set of axes that shares the same x-axis
        self.ax2 = self.ax1.twinx()
        
        # Empty x and y lists for storing data to plot later
        self.xs = []
        self.variables_1 = []
        self.variables_2 = []
        
        # Variables for holding temperature and light data
        self.variable_1 = tk.DoubleVar()
        self.variable_2 = tk.DoubleVar()
        
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
        
        # Variables for graph plotting
        self.update_interval = 1000 # Time (ms) between polling/animation updates
        self.graph_duration = 60 # Time (s) of grap length
        
        # Call animate() function periodically
        self.fargs = (self.ax1, self.ax2, self.xs, self.variables_1, self.variables_2, self.variable_1, self.variable_2, self.update_interval,self.graph_duration)
        self.ani = animation.FuncAnimation(self.fig, self.animate,fargs=self.fargs,interval=self.update_interval) 
        
    def GetOilTemp(self):
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
        GAIN = 1
        #self.value = adc.read_adc(2, gain=GAIN)
        self.value = random.randint(-20,120)
        self.ClntTemp.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 1000
        self.after(self.TimerInterval,self.GetClntTemp)
   
    def GetBatVolt(self):
        GAIN = 1
        #self.value = adc.read_adc(3, gain=GAIN)
        self.value = random.randint(0,150)/10
        self.BatVolt.set(self.value)
                       
        # Now repeat call
        self.TimerInterval = 125
        self.after(self.TimerInterval,self.GetBatVolt)
    
    # This function is called periodically from FuncAnimation
    def animate(self,i, ax1, ax2, xs, variables_1, variables_2, variable_1, variable_2, update_interval, graph_duration):
        start = time.time()
        print("start")
        # Update data to display temperature and light values
        try:
            new_variable_1 = random.randint(-10,120)
            new_variable_2 = random.randint(-10,120)
        except:
            pass
    
        # Append timestamp to x-axis list
        timestamp = mdates.date2num(dt.datetime.now())
        xs.append(timestamp)

        # Append sensor data to lists for plotting
        variables_1.append(new_variable_1)
        variables_2.append(new_variable_2)
    
        # Limit lists to a set number of elements and graph length
        max_elements = int(round(((graph_duration*1000)/update_interval),0))
        xs = xs[-max_elements:]
        variables_1 = variables_1[-max_elements:]
        variables_2 = variables_2[-max_elements:]
        
        # Clear, format, and plot light values first (behind)
        color = 'tab:orange'
        ax1.clear()
        ax1.set_ylabel('KUHLW. [C]', color=color, weight = 'bold')
        ax1.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, gridOn = True)
        ax1.tick_params(axis='x', labelcolor=color, pad = 0)
        #ax1.fill_between(xs, variables_1, 0, linewidth=2, color=color, alpha=0.3)
        ax1.plot(xs, variables_1, linewidth=2, color=color)
        
        # Clear, format, and plot temperature values (in front)
        color = 'tab:blue'
        ax2.clear()
        ax2.set_ylabel('OELTEMP [C]', color=color,weight = 'bold')
        ax2.tick_params(axis='y', labelcolor=color, pad = 1, length = 0)
        ax2.plot(xs, variables_2, linewidth=2, color=color)
        
        # Format timestamps to be more readable
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
        self.fig.autofmt_xdate()
        print(start-time.time())
        print("finish")
    
        # Make sure plots stay visible or invisible as desired
        #ax1.collections[0].set_visible(True)
        ax1.get_lines()[0].set_visible(True)
        ax2.get_lines()[0].set_visible(True)

       
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #Fonts
        # set the title bar text
        self.title('Bentron E30')
        # Uncomment to remove title bar:
        self.overrideredirect(1)
        # Configre window            
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(480, 640))
        self.configure(background='black')
        # Creat key binds
        self.bind('<Escape>',self.Destroy)
        self.bind('<F11>',self.fullscreen)
        self.bind('<F10>',self.smallwindow)
        # create Mainframe window
        Mainframe(self).grid()
        # now start
        self.mainloop()    
        
    def Destroy(self,event):
        Mainframe.destroy(self)
        
         
    def fullscreen(self,event):
        self.attributes('-fullscreen', True)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))


                      
# create an Window object
# it will run itself
if __name__ == '__main__':
    # run Window class
    Window()
    
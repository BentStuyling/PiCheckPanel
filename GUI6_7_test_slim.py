## Digital HUD check panel for BMW E30 based on Raspberry Pi

import tkinter as tk
from tkinter.font import Font
import random, time, csv
import matplotlib.figure as figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import subprocess

Warning = 'none'

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.pagenr = 3
        #Initialize fullscreen (window resolution)
        self.attributes('-fullscreen', False)
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
        self.pagenr=3 
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

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
        
    def toggle_frame(self,frame_class):
        
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
    

    def fullscreen(self,event):
        self.attributes('-fullscreen', False)   
        
    def smallwindow(self,event):
        self.attributes('-fullscreen', False)   
        self.geometry('{}x{}'.format(240, 320))
    

        
   
#For now Empty status Page
class Status(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
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

        #Fuel Rate:
        tk.Label(frame_lable_row_2, font=LabelFont, fg=Labelcolor, 
                 bg = 'black', text = 'GEBRG.').place(x = 120, y= 4)
        self.ValPos_4 = tk.IntVar()
        tk.Label(frame_value_row_2, font = ValueFont, fg =Valuecolor,
                 bg = 'black', textvariable = self.ValPos_4).place(x = 200, y =15, anchor ='e')
        tk.Label(frame_value_row_2,font = UnitFont, fg =Unitcolor,
                 bg = 'black', text = 'L/h').place(x = 200, y =19, anchor ='w')        

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
    
    def GetValPos_4(self):
        self.ValPos_4.set(get_signal.BatVolt(self))
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

#For now Empty Page    
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

#For now Empty Page    
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

Vin = 5.25
class get_signal:
    
    def OilTemp(self):
        self.U = random.uniform(3,5)
        #self.U= (4.096/32768)*adc_1.read_adc(1, gain=1)
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
        self.value = round(random.uniform(0,80)/10,1)
        #self.newvalue = abs(round((((4.096/32768)*adc_1.read_adc(0, gain=1)-0.475)/4)*9,1))
        return self.value
        
    def ClntTemp(self):
        self.U = random.uniform(3,4)
        #self.U= (4.096/32768)*adc_1.read_adc(2, gain=1)
        self.R= 330*((Vin/self.U)-1)
        if 1 < self.R <24000:
            self.temp =  (211749.2077)/(1 + (self.R/(1.274787*10**-14))**0.185661) -113.7
            self.value= round(self.temp,2)
            return self.value
        else:
            self.value = "--"
            return self.value
    
    def BatVolt(self):
        self.value = '{:.2f}'.format(round(random.uniform(0,14),2))
        #self.value = '{:.1f}'.format(round(adc_1.read_adc(3, gain=1)*(4.069/32768)*((3.3+1)/1)*1.022, 1))
        return self.value  
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

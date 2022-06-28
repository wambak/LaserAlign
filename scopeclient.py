from tkinter import *
import socket, threading
import time
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import urllib.request
import os

class grafit(Frame):
    def plotit(self):
        start_time = time.time()

        while True:
            try :
                    data = ''
                    #f = urllib.request.urlopen('http://localhost:5022/?COMMAND=curve?')
                    f = urllib.request.urlopen('http://134.79.229.21/?COMMAND=curve?')
                    data = f.read().decode()
                    print('received '+data)

                    wfm = [ float(u) for u in data.split(',') ]
                    # print(len(wfm))

                    # CALLING WFMPRE TO CONVERT WFM TO MS AND VOLTS
                    f2 = urllib.request.urlopen('http://134.79.229.21/?COMMAND=wfmpre?')
                    wfmpre = f2.read().decode()
                    # print(wfmpre)

                    # EXAMPLE WFMPRE:
                    #wfmpre = '1;8;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";8.0E-4;0.0E0;-5.4E1;"V"'
                    t = [ 1.0e6*(float(wfmpre.split(';')[8])*float(i)+float(wfmpre.split(';')[10])) for i in range(0,len(wfm)) ]
                    volt = [ 1.0e3*(( (dl/256) - float(wfmpre.split(';')[14]) )*float(wfmpre.split(';')[12]) - float(wfmpre.split(';')[13])) for dl in wfm ]

                    # print(f"t: {len(t)}")
                    # print(f"volt: {len(volt)}")

                    # FINDING PEAK / UPSTROKE SIZE:

                    # begin search for start of upstroke after 50us:
                    fiftymus = np.argmax( np.array(t) > 50.0 )
                    print("fiftymus: " , fiftymus)
                    volt_subset = volt[:fiftymus]
                    max_index = np.argmax(volt_subset)
                    print("max index: ", max_index)
                    # search for minimum either 50 points back or less in the subset:
                    start = max_index - 50
                    print("start: ", start)
                    if start < 0 : start = 0
                    try :
                        peak = volt_subset[max_index] - np.min( np.array(volt_subset)[start:max_index] )
                    except ValueError:
                        print('max_index',str(max_index))
                        print(volt_subset)

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    self.xar.append((time.time() - start_time))
                    self.yar.append(peak)

                    if len(self.xar) > 5000:
                        self.xar.pop(0)
                        self.yar.pop(0)
                    plt.clf()

                    # PLOTTTING PEAKS:
                    plt.subplot(211)
                    plt.plot(self.xar, self.yar,'bo-')
                    plt.title("Upstroke/Peak History")
                    plt.ylabel('Millivolts')
                    plt.xlabel('Time (s)')

                    # PLOTTING WAVEFORM:
                    plt.subplot(212)
                    plt.plot(t,volt,'go-')
                    plt.title("Most recent waveform")
                    plt.ylabel("MilliVolts")
                    plt.xlabel(u"Time (\u03bcs)")

                    plt.subplots_adjust(hspace=0.6, wspace=0.6)
                    self.plot_widget.grid(row=0, column=0, rowspan=2)

                    # WIDGET TO SEE MOST RECENT PEAK
                    T = Text(self.window, height = 1, width = 5, font=("Courier", 64))
                    peak = round(peak, 1)
                    T.insert(END, peak)
                    T.grid(row=0, column=1)
                    T.config(foreground="blue")

                    self.fig.canvas.draw_idle()

                    # originally 5:
                    time.sleep(1.0)
            except Exception as exc:
                    os._exit(0)
                    pass    

    def on_closing(self):
        os._exit(0)


    def __init__(self):

        self.xar = []
        self.yar = []
        self.window = Tk()

        # INITIAL GUI PAGE:
        self.window.title('Fiber Alignment Tool')
        self.fig = plt.figure(1)
        self.fig.text(0.5,0.04,'LOADING...',ha ='center',va = 'center')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0)
        self.curve = '-51,-51,-50,-50,-50,-50,-50,-50,-50,-50,-50,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-48,-48,-48,-47,-47,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-50,-50,-50,-50,-50,-50,-50,-50,-50,-50,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-56,-55,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-57,-56,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-56,-57,-57,-57,-57,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-54,-55,-54,-55,-55,-54\n'

        self.fig.canvas.draw()

        self.plotter = threading.Thread(target=self.plotit)
        self.plotter.setDaemon(True) # MAKES CODE THREAD SAFE
        self.plotter.start()
        exit_button = Button(self.window, text="Exit", command=self.on_closing)
        exit_button.grid(row=1, column=1)
        self.window.mainloop()

appl = grafit()

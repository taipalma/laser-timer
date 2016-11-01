from Tkinter import *
import tkMessageBox
import time
import threading
import USBthread

class Stopwatch:

    def __init__(self):

        # Simple status flag
        # False mean the timer is not running
        # True means the timer is running (counting)
        self.__state = False
        self.__laserActive = False

        self.__mainWindow = Tk()
        self.__mainWindow.title('Stopwatch')

        # Variable to terminate Threads
        self.__isTerminated = False

        self.__start = 0.0
        self.__elapsedtime = 0.0
        self.__timeString = ""

        self.__lapstart = 0.0
        self.__laptime = 0.0        

        # The format is padding all the 
        self.__pattern = '{0:02d}:{1:02d}:{2:02d}'

        # A file for results
        self.__file = open("./results.csv", "a")  

        # Variables for mode: 1 = 40 yd dash, 2 = 20 yd shuttle, 3 = 3 cone drill
        self.__mode = 1
        self.__modeText = StringVar()
        self.__modeText.set('dash') 

        # Labels:
        self.__timeText = Label(self.__mainWindow, text="00:00:00", font=("Helvetica", 100))
        self.__modeLabel = Label(self.__mainWindow, text="mode:")
        self.__athleteLabel = Label(self.__mainWindow, text="athlete:")
        self.__teamLabel = Label(self.__mainWindow, text="team:")
        
        # Fillers to get nicer outlook
        self.__fillerLabel1 = Label(self.__mainWindow, text="")
        self.__fillerLabel2 = Label(self.__mainWindow, text="")
        
        # Buttons
        self.__startButton = Button(self.__mainWindow, text='Start / Stop',font=("Helvetica", 50), command=self.start)
        self.__saveButton = Button(self.__mainWindow, text='Save', command=self.save)
        self.__resetButton = Button(self.__mainWindow, text='Reset', command=self.reset)
        self.__quitButton = Button(self.__mainWindow, text='Quit', command=self.exit)
        
        # Radio Buttons 
        self.__RadioButton1 = Radiobutton(self.__mainWindow, text="40 yd dash", variable=self.__modeText, value="dash", command=self.selected)
        self.__RadioButton2 = Radiobutton(self.__mainWindow, text="20 yd shuttle", variable=self.__modeText, value="shuttle", command=self.selected)
        self.__RadioButton3 = Radiobutton(self.__mainWindow, text="3 cone drill", variable=self.__modeText, value="cone", command=self.selected)

        # Entries
        self.__athleteEntry = Entry(self.__mainWindow)
        self.__teamEntry = Entry(self.__mainWindow)
        
        # Grid:
        self.__timeText.grid(row=0, column=0,columnspan=4)
        self.__modeLabel.grid(row=3, column=0, sticky=E)
        self.__athleteLabel.grid(row=3, column=2, sticky=E)
        self.__teamLabel.grid(row=4, column=2, sticky=E)
        
        self.__fillerLabel1.grid(row=2, column=0)
        self.__fillerLabel2.grid(row=6, column=0)

        self.__startButton.grid(row=1, column=0, columnspan=4)
        self.__saveButton.grid(row=7, column=1)
        self.__resetButton.grid(row=7, column=2)
        self.__quitButton.grid(row=7, column=3)

        self.__RadioButton1.grid(row=3, column=1, sticky=W)
        self.__RadioButton2.grid(row=4, column=1, sticky=W)
        self.__RadioButton3.grid(row=5, column=1, sticky=W)

        self.__athleteEntry.grid(row=3, column=3, sticky=W)
        self.__teamEntry.grid(row=4, column=3, sticky=W)
    
        # Thread for USB communication
        threadPool = []
        
        for threads in range(1):
            usbThread = USBthread.USBthread(self)
            usbThread.start()
            threadPool.append(usbThread) 
  

        self.update_timeText()
        self.__mainWindow.mainloop()

    # Note: Python 2.6 or higher is required for .format() to work
    def update_timeText(self):
        if (self.__state):
            self.__elapsedtime = time.time() - self.__start
            elap = self.__elapsedtime
            minutes = int(elap/60)
            seconds = int(elap - minutes*60.0)
            hseconds = int((elap - minutes*60.0 - seconds)*100) 
            self.__timeString = self.__pattern.format(minutes, seconds, hseconds)
            # Update the timeText Label box with the current time
            self.__timeText.configure(text=self.__timeString)
            # Call the update_timeText() function after 1 centisecond
        self.__mainWindow.after(10, self.update_timeText)

    # To start the timer
    def start(self):     
        if self.__state == False:
            self.__start = time.time() - self.__elapsedtime
            self.__state = True
        else: 
            self.__state = False

    # Save results
    def save(self):
        athlete = self.__athleteEntry.get()
        team = self.__teamEntry.get()
        time = self.__timeString
 
        if self.__mode == 1:
            mode = "40 yd dash"
        elif self.__mode == 2:
            mode = "20 yd shuttle"
        elif self.__mode == 3:
            mode = "3 cone drill"

        line = team + ";" + athlete + ";" + mode + ";" + time + "\n"          
        self.__file.write(line)

        print mode + " " + athlete + " " + time  

        tkMessageBox.showinfo("", "Saved")


    # To reset the timer to 00:00:00
    def reset(self):
        self.__start = 0.0
        self.__elapsedtime = 0.0
        self.__lapstart = 0.0
        self.__laptime = 0.0  
        self.__timeText.configure(text='00:00:00')

    # To exit our program
    def exit(self):
        self.__isTerminated = True
        self.__file.close()
        self.__mainWindow.destroy()

    def isTerminated(self):
        return self.__isTerminated 
 
    # Stop the clock using usb-signal
    def usbStop(self):
        if self.__mode == 1:
            self.__state = False           
        elif self.__mode == 2 and self.__elapsedtime > 0.6:
            if self.__lapstart == 0.0:
                self.__lapstart = time.time()
            else:
                self.__laptime = time.time() - self.__lapstart
            if self.__laptime > 0.6:
                self.__state = False
        elif self.__mode == 3 and self.__elapsedtime > 5:
            self.__state = False
               

    def selected(self):
        if self.__modeText.get() == "dash":
            self.__mode = 1
        elif self.__modeText.get() == "shuttle":
            self.__mode = 2
        elif self.__modeText.get() == "cone":
            self.__mode = 3
  
 
def main():
    ui = Stopwatch()

main()

    


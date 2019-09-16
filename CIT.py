from platform   import system
from subprocess import call
from tkinter import *
import time


class Buttons:
    def __init__(self, masterRoot): #code for gui
        self.masterRoot = masterRoot
        topFrame = Frame(masterRoot)
        bottomFrame = Frame(masterRoot)
        topFrame.pack()
        bottomFrame.pack()
        
        self.running = False
        self.server = "8.8.8.8"
        self.interval = 3
        self.curStat = StringVar()
        self.curStat.set("Not Pinging")

        self.buttStart = Button(topFrame, text="Start", fg="green", command=self.start)
        self.buttStop = Button(topFrame, text="Stop", fg="red", command=self.stop)

        self.buttStart.grid(row=0, column=3)
        self.buttStop.grid(row=0, column=5)

        self.labelServer = Label(topFrame, text="Server:")
        self.labelServer.grid(row=1, column=3)

        self.entryServer = Entry(topFrame)
        self.entryServer.grid(row=2, column=3)
        self.entryServer.insert(0, "8.8.8.8")

        self.buttServer = Button(topFrame, text="Update Server", command=self.updateServer)
        self.buttServer.grid(row=3, column=3)
        
        self.labelInterval = Label(topFrame, text="Interval(Seconds):")
        self.labelInterval.grid(row=1, column=5)

        self.entryInterval = Entry(topFrame)
        self.entryInterval.grid(row=2, column=5)
        self.entryInterval.insert(0, "3")

        self.buttInterval = Button(topFrame, text="Update Interval", command=self.updateInterval)
        self.buttInterval.grid(row=3, column=5)

        self.statBar = Label(bottomFrame, textvariable=self.curStat, bd=1, relief=SUNKEN, anchor=W)
        self.statBar.pack(side=BOTTOM, fill=X)

        self.text = Text(bottomFrame, height=8, width=45)
        self.scroller = Scrollbar(bottomFrame, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroller.set)
        self.scroller.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

    def start(self): #fuction for start button, calls loop
        if self.running == False:
            self.running = True
            self.pingLoop()
        self.curStat.set("Pinging...")

    def pingLoop(self): #loop to continue pinging the server, based on bool running, set by start/stop
        if self.running == True:
            response = self.ping(self.server)
            if response != 0:
                self.text.insert("end", "No response at " + time.ctime() + "\n")
            else:
                self.text.insert("end", time.ctime() + "\n")
            self.text.see("end")
            self.masterRoot.after(self.interval*1000, self.pingLoop)

    def stop(self): #function for stop button
        if self.running == True:
            self.running = False
        self.curStat.set("Not Pinging")

    def ping(self, server): #function to ping server, takes server as parameter
        os = '-n' if system().lower()=='windows' else '-c'
        command = ['ping', os, '1', server]
        response = call(command, shell=True)
        return response

    def updateServer(self): #function for updateserver button
        if self.running == False:
            self.server = self.entryServer.get()
            
    def updateInterval(self): #function for updateInterval button
        if self.running == False:
            self.interval = int(self.entryInterval.get())
            

if __name__ == "__main__":
    root = Tk()
    b = Buttons(root)
    root.mainloop()
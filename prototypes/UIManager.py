from tkinter import *

class UIManager():

    def __init__(self, client_machine):
        """
        Initialize the UIManager. 

        @param client_machine: Reference to ClientMachine instance to use. Is of type ClientMachine
        """
        self.client_machine = client_machine
        self.setup()


    def setup(self):
        # create a tkinter window
        root = Tk()             
        
        # Open window having dimension 100x100
        root.geometry('100x100')
        
        # Create a Button
        start_btn = Button(root, text = 'Start', bd = '5', command = self.on_start)

        stop_btn = Button(root, text = 'Stop', bd = '5', command = self.on_stop)

        queue_1_btn = Button(root, text = 'Queue 1', bd = '5', command = self.queue_1)
        queue_2_btn = Button(root, text = 'Queue 2', bd = '5', command = self.queue_2)
        
        # Set the position of button on the top of window.  
        start_btn.pack(side = 'top')
        stop_btn.pack(side = 'top')
        
        root.mainloop()
    
    def on_start(self):
        self.client_machine.state_machine.send("start")
    def on_stop(self):
        self.client_machine.state_machine.send("stop")
    
    def queue_1(self):
        self.client_machine.state_machine.send("queue_1")
    def queue_2(self):
        self.client_machine.state_machine.send("queue_2")


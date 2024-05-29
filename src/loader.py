import threading
import time

import tkinter as tk


class cLoader:
    def __init__(self):    
        self.__init_attribute()
    
    def __init_attribute(self):
        self.parent = None
        
        self.array_frame = [None for _ in range(100)]
        self.index_start = 0
        self.index_end = 0
        
        self.is_stop = False
        
        self.function_update_body = None
        
    def __init_widget(self):
        self.frame = tk.Frame(self.parent)
        
        size = len(self.array_frame)
        for i in range(size):
            frame = tk.Frame(self.frame)
            self.array_frame[i] = frame
              
    def __set_position(self):
        self.frame.grid_rowconfigure(0, weight=1)
        
        size = len(self.array_frame)
        for i in range(size):
            self.frame.grid_columnconfigure(i, weight=1)
        
        for i in range(size):
            frame = self.array_frame[i]
            frame.grid(row=0, column=i, sticky="nsew")
    
    
    def start(self, delay = 5):
        size = len(self.array_frame)
        wait = delay/size
        thread = threading.Thread(target=self.__start, args=(wait,))
        thread.start()   
            
    def __start(self, wait):
        size = len(self.array_frame)
        
        for i in range(size):
            if(self.is_stop):
               return 
            frame = self.array_frame[i] 
            frame.config(bg="#3bf707")    
            time.sleep(wait)   
        
        self.__reset()
        
    def stop(self):
        self.is_stop = True
        
        size = len(self.array_frame)
        
        for i in range(size):
            frame = self.array_frame[i] 
            frame.config(bg="#3bf707")
        
        time.sleep(0.1)
        self.__reset()
    
    def step(self, percent, status):
        size = len(self.array_frame)
        self.index_end = int(percent * size / 100) -1
        
        if(percent > 100):
            self.index_end = size-1
        
        # print(self.index_end)
        
        thread = threading.Thread(target=self.__step)
        thread.start()             
        
        if(self.function_update_body != None):
            self.function_update_body(status)
    
    def __step(self):
        size = len(self.array_frame)
        
        for i in range(self.index_start, self.index_end, 1):
            frame = self.array_frame[i] 
            frame.config(bg="#3bf707")
        
        self.index_start = self.index_end
        
        # print(self.index_end)
        if(self.index_end == (size-1)):
            self.__reset()
        
    
    def __reset(self):
        size = len(self.array_frame)
        
        self.index_start = 0
        self.index_end = 0
        
        self.is_stop = False
        
        for i in range(size):
            frame = self.array_frame[i] 
            frame.config(bg="SystemButtonFace")
                
    
    def set_parent(self, parent):
        self.parent = parent
        
        self.__init_widget()
        self.__set_position()
    

c_loader =  cLoader()
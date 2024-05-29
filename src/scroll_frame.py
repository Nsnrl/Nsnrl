import tkinter as tk

class cFrame_Scroll():
    def __init__(self,root, **options):
        outerFrame = tk.Frame(root)
        canvas = tk.Canvas(outerFrame, highlightthickness=0, bg="#ffffff")
        scrollbar = tk.Scrollbar(outerFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        # scrollbar = tk.Scrollbar(outerFrame, orient="horizontal", command=canvas.xview)
        # scrollbar.pack(side="bottom", fill="x")
        canvas.pack(fill="both", expand=1, anchor="nw")
        self.frame = tk.Frame(canvas, **options)
        wrapFrameId = canvas.create_window((0,0), window=self.frame, anchor="nw")
        canvas.config(yscrollcommand=scrollbar.set)
        
        canvas.bind("<Configure>", lambda event: self.onFrameConfigure())
        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)) # on mouse enter
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>")) # on mouse leave
        self.outerFrame, self.canvas, self.vsb, self.frame, self.wrapFrameId = outerFrame, canvas, scrollbar, self.frame, wrapFrameId 
        
    def onFrameConfigure(self):
        canvas = self.canvas
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(self.wrapFrameId, width=canvas.winfo_width())
        
    def on_mouse_wheel(self, event, scale=3):
        canvas = self.canvas
        #only care event.delta is - or +, scroll down or up
        if event.delta<0:
            canvas.yview_scroll(scale, "units")
        else:
            canvas.yview_scroll(-scale, "units")

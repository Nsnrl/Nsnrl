# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
import time
import threading

import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from src.utils import*
from src.loader import c_loader
from src.scroll_frame import cFrame_Scroll


# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class cMainWindow:
    def __init__(self):
        self.__init_variable()
        
        self.__create_window()
        self.__init_widget()
        
        self.__connect_button()
        self.__config_widget()
        
        self.__set_position()


    def __init_variable(self):
        self.list_path = []
        self.list_status = []

        self.header = ["Zonage", "Section Parcelle", "Parcelle", "Num-Voie", "Adresse Foncier", "Superficie", "civilite", "Nom/Prenom", "Adresse Proprio", "Code Postale", "Commune", "Date | Courrier | Num"]
        
                       
    def __create_window(self):
        self.window = tk.Tk() 
        
        self.window.geometry("1200x800")
        # self.window.state('zoomed')
         
        title = f"Heilmann Software - 0.3"
        self.window.title(title)   
        
        self.window.iconbitmap("res/convertir.ico")
        
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
    
    def __init_widget(self):
        self.frame_button = tk.LabelFrame(self.window, text="")
        self.frame_body = tk.LabelFrame(self.window, text="Processus")
        self.frame_loading = tk.Frame(self.window)
        
        #FRAME BUTTON
        self.frame_button_load_folder = tk.Frame(self.frame_button)
        self.button_load_folder = tk.Button(self.frame_button_load_folder, text="Load Folder")
        
        self.frame_label_number_file = tk.Frame(self.frame_button)
        self.label_number_file = tk.Label(self.frame_label_number_file, text="Number of Files: ")

        self.frame_label_number_error = tk.Frame(self.frame_button)
        self.label_number_error = tk.Label(self.frame_label_number_error, text="Number of Errors: ")

        self.frame_button_generate_csv = tk.Frame(self.frame_button)
        self.button_generate_csv = tk.Button(self.frame_button_generate_csv, text="Generate CSV")
        
        #FRAME BUTTON
        self.c_frame_scroll = cFrame_Scroll(self.frame_body)
        
        
        #LOADER
        c_loader.set_parent(self.frame_loading)


    def __connect_button(self):
        self.button_load_folder.config(command=self.__on_click_load_folder)
        self.button_generate_csv.config(command=self.__on_click_generate_csv)
        
    def __config_widget(self):
        #--------------------------------------- Connect function
        c_loader.function_update_body = self.__add_status
        
        #--------------------------------------- Set Image Button
        self.__set_button_load_folder_image()
        self.__set_button_generate_csv_image()
        
        #---------------------------------------
        self.button_load_folder.bind("<Enter>", self.__on_button_enter)
        self.button_load_folder.bind("<Leave>", self.__on_button_leave)

        self.button_generate_csv.bind("<Enter>", self.__on_button_enter)
        self.button_generate_csv.bind("<Leave>", self.__on_button_leave)


    def __set_position(self):
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=3)
        self.window.grid_rowconfigure(1, weight=16)
        self.window.grid_rowconfigure(2, weight=1)
        
        self.frame_button.grid(column=0, row=0, sticky="nsew")
        self.frame_body.grid(column=0, row=1, sticky="nsew")
        self.frame_loading.grid(column=0, row=2, sticky="nsew")
        
        
        #BUTTON
        self.frame_button.grid_rowconfigure(0, weight=1)
        self.frame_button.grid_columnconfigure(0, weight=1)
        self.frame_button.grid_columnconfigure(1, weight=1)
        self.frame_button.grid_columnconfigure(2, weight=1)
        self.frame_button.grid_columnconfigure(3, weight=1)
        
        self.frame_button_load_folder.grid(column=0, row=0, sticky='nsew')
        self.frame_label_number_file.grid(column=1, row=0, sticky='nsew')
        self.frame_label_number_error.grid(column=2, row=0, sticky='nsew')
        self.frame_button_generate_csv.grid(column=3, row=0, sticky='nsew')
        
        self.frame_button_load_folder.pack_propagate(False)
        self.frame_label_number_file.pack_propagate(False)
        self.frame_label_number_error.pack_propagate(False)
        self.frame_button_generate_csv.pack_propagate(False)
        
        self.button_load_folder.pack(expand=True, fill=tk.BOTH)
        self.label_number_file.pack(expand=True, fill=tk.X)
        self.label_number_error.pack(expand=True, fill=tk.X)
        self.button_generate_csv.pack(expand=True, fill=tk.BOTH)
        
        #BODY
        self.c_frame_scroll.outerFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        #LOADER
        c_loader.frame.pack(expand=True, fill=tk.BOTH)
        
     
     # BUTTON
    
    
    #--set image--
    def __set_button_load_folder_image(self):
        image_path = r"res/load_folder.png"

        original_image = Image.open(image_path)
        image = original_image.resize(size=(40,40))
        self.image_button_load_folder = ImageTk.PhotoImage(image)
        
        self.button_load_folder.config(image=self.image_button_load_folder, compound=tk.TOP)
    
    def __set_button_generate_csv_image(self):
        image_path = r"res/csv.png"

        original_image = Image.open(image_path)
        image = original_image.resize(size=(40,40))
        self.image_button_generate_csv = ImageTk.PhotoImage(image)
        
        self.button_generate_csv.config(image=self.image_button_generate_csv, compound=tk.TOP)
      
       
    # --on enter/leave--
    def __on_button_enter(self, event):
        event.widget.config(bg="darkgrey", cursor="hand2")

    def __on_button_leave(self, event):
        event.widget.config(bg="SystemButtonFace", cursor="")
        
        
    # --on click--
    def __on_click_load_folder(self):
        folder_path = filedialog.askdirectory()
        if(not folder_path):
            return

        c_loader.start(0.3)
        
        # Format path
        list_path = get_list_path(folder_path)
        rename_files(folder_path, list_path)
        self.list_path = get_list_path(folder_path)
        
        
        # update label
        self.label_number_file.config(text=f"Number of Files: {len(list_path)}")
        
        # update body contain
        self.__fill_body(self.list_path)
        

        # c_loader.stop()
        
    def __on_click_generate_csv(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("csv files", "*.csv")])
        if(not output_path):
            return
        
        thread = threading.Thread(target=self.__on_click_generate_csv_TH, args=(output_path,))
        thread.start()
        
    def __on_click_generate_csv_TH(self, output_path):
        #start 
        data = get_list_information(self.list_path)

        # init variables
        list_error_personne_morale = []
        list_error_personne_physique = []

        list_personne_physique = []
        list_personne_morale = []
        
        # get lists from data
        if( "list_error_personne_physique" in data):
            list_error_personne_physique = data["list_error_personne_physique"]
        if( "list_error_personne_morale" in data):
            list_error_personne_morale = data["list_error_personne_morale"]
        
        list_error = list_error_personne_physique + list_error_personne_morale
        
        # update label    
        number_error = len(list_error_personne_physique) + len(list_error_personne_morale)
        self.label_number_error.config(text=f"Number of Errors: {number_error}")
        
        # update body
        self.__update_body()
            
        # get list personne
        if( "list_personne_physique" in data):
            list_personne_physique = data["list_personne_physique"]
        if( "list_personne_morale" in data):
            list_personne_morale = data["list_personne_morale"]
            
        # fill data_csv
        data_csv = [self.header]
        for personne in list_personne_physique:
            row = personne.get_csv_row(self.header)
            data_csv.append(row)
        for personne in list_personne_morale:
            row = personne.get_csv_row(self.header)
            data_csv.append(row)
            
        formated_data = format_data_csv(data_csv)        

        #create csv
        create_csv(output_path, formated_data)
        
        c_loader.stop()
        
        
        
    #BODY
    def __fill_body(self, list_path):
        self.c_frame_scroll = cFrame_Scroll(self.frame_body)
        for path in list_path:
            label = tk.Label(self.c_frame_scroll.frame, text=path)
            label.pack(expand=True, anchor="w", pady=2)
            
        self.c_frame_scroll.outerFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
            
    def __update_body(self):
        self.c_frame_scroll = cFrame_Scroll(self.frame_body)
        self.list_status
        for i in range(len(self.list_path)):
            path = self.list_path[i]
            
            status = 0
            if(i < len(self.list_status)):
                status = self.list_status[i]
                
            if(status == 2):
                text = f"{path} - NOK"
                label = tk.Label(self.c_frame_scroll.frame, text=text, fg="red")
            elif(status == 1):
                text = f"{path} - OK"
                label = tk.Label(self.c_frame_scroll.frame, text=text, fg="green")
            elif(status == 0):
                text = f"{path}"
                label = tk.Label(self.c_frame_scroll.frame, text=text, fg="blue")
                
            label.pack(expand=True, anchor="w", pady=2)
        self.c_frame_scroll.outerFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def __add_status(self, status):
        self.list_status.append(status)
        self.__update_body()
        
    # FUNCTION
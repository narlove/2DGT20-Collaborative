import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as customTkinter
import json
import os
from admin_menu import build_admin_menu
from teacher_menu import TeacherAbsenceTracker 
import customtkinter as customTkinter
from customtkinter import CTkToplevel
import time

#Sign up mnu
def sign_up_menu(rootWindow=tk.Tk):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_path = os.path.join(file_dir, "Desktop.png")
    json_file_path = os.path.join(file_dir, "users.json")
    root = CTkToplevel(rootWindow)
    root.title("Sign Up Menu")
    root.geometry("800x580")
    root.resizable(width=False, height=False)
    #Gives the GUI a background
    background_image = tk.PhotoImage(file = desktop_path)
    graphicL = customTkinter.CTkLabel(root,image = background_image, text=" ")
    graphicL.pack()
    root.protocol("WM_DELETE_WINDOW", lambda: quit())
    #Label
    label = customTkinter.CTkLabel(root, text = "Please enter your Name and Surname", text_color = '#680067', bg_color = '#F9F4F5', font = ("Cooper Black", 14))
    label.place(x = 270, y = 310)
    #Gives user place to type Password
    entry_password2 = customTkinter.CTkEntry(root, bg_color = '#F9F4F5', placeholder_text = "Password", show = '*')
    entry_password2.place(x = 330, y = 380)
    #Gives user place to type username
    entry_name2 = customTkinter.CTkEntry(root, bg_color = '#F9F4F5', placeholder_text = "Name Surname")
    entry_name2.place(x = 330, y = 340)
    # inserts user name and password into JSon file
    def Sign_Up():
        splitNames = entry_name2.get().split(' ')
        teacherCode=splitNames[1][:2]+splitNames[0][:1]

        # code to add to the dictionary
        with open(json_file_path, 'r') as readfile:
            data = json.load(readfile)

        data[teacherCode] = {
            "username": entry_name2.get().replace(' ', '.'),
            "password": entry_password2.get(),
            "name": entry_name2.get(),
            "isAdmin": False
        }
        #Code to add to the Json 
        with open(json_file_path, "w") as outfile:
            json.dump(data, outfile)
        quit()
    #submit button
    button_enter2 = customTkinter.CTkButton(root,bg_color = '#F9F4F5',fg_color = '#680067', hover_color = '#b142c1', height = 29, width = 50, text ="Sign up",font=customTkinter.CTkFont("arial"),command=Sign_Up)
    button_enter2.place(x = 370, y = 420)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as customTkinter
import json
import os

from admin_menu import build_admin_menu
from sign_up import sign_up_menu 
from teacher_menu import build_teacher_window

file_dir = os.path.dirname(os.path.abspath(__file__))
desktop_path = os.path.join(file_dir, "Desktop.png")
users_path = os.path.join(file_dir, "users.json")

window1 = customTkinter.CTk()
window1.protocol("WM_DELETE_WINDOW", lambda: quit())

# need the image
background_image = tk.PhotoImage(file = desktop_path)
graphicL = tk.Label(window1, image = background_image)
graphicL.pack()

#creates the Width Variable in proportion of the users screen
width = window1.winfo_screenwidth()

#creates the Height Variable in proportion to the users screen
height = window1.winfo_screenheight()

center_x = width // 2
center_y = height // 2

window1.config(bg= '#240046')

def submit_functionality(event = None):
    username = entry_name.get()
    password = entry_password.get()

    if username == '' or password == '':
        messagebox.showwarning('An error occured', 'Ensure you enter both a username and a password.')
        return

    with open(users_path, 'r') as f:
        data = json.load(f)

        foundUser = False
        foundPass = False

        for profile in data:
            if username != data[profile]["username"]: continue
            foundUser = True

            fullProfile = data[profile]

            if password != fullProfile["password"]: continue
            foundPass = True
            if fullProfile['isAdmin'] == True:
                build_admin_menu(window1)
                window1.withdraw()
            else:
                teacherMenu = build_teacher_window(rootWindow=window1)
                window1.update()

                window1.withdraw()   

        if foundUser == False or foundPass == False:
            messagebox.showerror('An error occured', 'Ensure the password and username match.')

        if foundUser == True and foundPass == True:
            window1.withdraw()

def open_sign_up(event = None):
    sign_up_menu(window1)
    window1.withdraw()

#creates window 
window1.geometry('800x580')
window1.resizable(width=False, height=False)

#creates a question on the window
label_morning = customTkinter.CTkLabel(window1, text = "Goodmorning, Doing a little Light sorting?", text_color = '#680067', bg_color = '#F9F4F5', font = ("Cooper Black", 14))
label_morning.place(x = 247, y = 320)

entry_password = customTkinter.CTkEntry(window1, bg_color = '#F9F4F5', placeholder_text = "Password", show = '*')
entry_password.place(x = 330, y = 420)

entry_name = customTkinter.CTkEntry(window1, bg_color = '#F9F4F5', placeholder_text = "Username")
entry_name.place(x = 330, y = 390)

sign_up=customTkinter.CTkButton(window1,bg_color='#F9F4F5', fg_color='#680067', hover_color = '#b142c1',height = 29, width = 50, text="Sign Up", command=open_sign_up)
sign_up.place(x=370,y=480)

button_enter = customTkinter.CTkButton(window1,bg_color = '#F9F4F5',fg_color = '#680067', hover_color = '#b142c1', height = 29, width = 50, text ="Sign In",font=customTkinter.CTkFont("arial"),command = submit_functionality)
button_enter.place(x = 470, y = 420)

if not os.path.exists(users_path):
    messagebox.showwarning('An error may have occured', 'There have been no profiles previously established. If you believe this to be an error, please ensure your users.json file is intact and in the same directory as the root file (main.py)')
    with open(users_path, 'a') as f:
        pass

window1.bind('<Return>',submit_functionality)

window1.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as customTkinter

import json

from admin_menu import build_admin_menu

window1 = customTkinter.CTk()
window1.protocol("WM_DELETE_WINDOW", lambda: quit())

# need the image
#background_image = tk.PhotoImage(file = 'Desktop.png')
#graphicL = tk.Label(window1, image = background_image)
#graphicL.pack()

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
    
    foundUser = False
    foundPass = False

    with open('users.json', 'r') as f:
        data = json.load(f)
        for profile in data:
            if username != data[profile]["username"]: continue
            foundUser = True

            fullProfile = data[profile]

            if password != fullProfile["password"]: continue
            foundPass = True

            if fullProfile['isAdmin'] == True:
                build_admin_menu(window1)
            else:
                print('not working yet')
                quit()

            window1.withdraw()

        if foundUser == False or foundPass == False:
            messagebox.showerror('An error occured', 'Ensure the password and username match.')

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

button_enter = customTkinter.CTkButton(window1,bg_color = '#F9F4F5',fg_color = '#680067', hover_color = '#b142c1', height = 29, width = 50, text = "Enter", command = submit_functionality)
button_enter.place(x = 470, y = 420)

window1.mainloop()
import csv
from tkinter import*
from tkinter import  ttk
import tkinter as tk
import time 
import tkcalendar
import customtkinter as customTkinter
from PIL import Image
from tkinter import messagebox
import json

window1=customTkinter.CTk()
background_image=tk.PhotoImage(file='Desktop.png')
graphicL=tk.Label(window1,image=background_image)
graphicL.pack()
#creates the Width Variable in proportion of the users screen
width= window1.winfo_screenwidth()
#creates the Height Variable in proportion to the users screen
height=window1.winfo_screenheight()
center_x=width//2
center_y=height//2
window1.config(bg='#240046')

def submit_functionality(event = None):
    username = NameE.get()
    password = PasswordE.get()

    if username == '' or password == '':
        messagebox.showwarning('An error occured', 'Ensure you enter both a username and a password.')
        return
    
    foundUser = False
    foundPass = False

    with open('main-kaiden/users.json', 'r') as f:
        data = json.load(f)
        for profile in data:
            if username != data[profile]["username"]: continue
            foundUser = True

            fullProfile = data[profile]

            if password != fullProfile["password"]: continue
            foundPass = True

            

            window1.destroy()
            
#put merge code here
        if foundUser == False or foundPass == False:
            messagebox.showerror('An error occured', 'Ensure the password and username match.')



#creates window 
window1.geometry('800x580')

#creates a question on the window
MorningL=customTkinter.CTkLabel(window1,text="Goodmorning, Doing a little Light sorting?",text_color='#680067',bg_color='#F9F4F5',font=("Cooper Black", 14))
MorningL.place(x=247,y=320)


PasswordE=customTkinter.CTkEntry(window1,bg_color='#F9F4F5', placeholder_text="Password", show='*')
PasswordE.place(x=(330),y=(420))

NameE=customTkinter.CTkEntry(window1,bg_color='#F9F4F5', placeholder_text="Username")
NameE.place(x=(330),y=(390))

enterB=customTkinter.CTkButton(window1,bg_color='#F9F4F5',fg_color='#680067' , hover_color='#b142c1',height=29,width=50,text="Enter",command=submit_functionality)
enterB.place(x=(470),y=(420))



window1.mainloop()


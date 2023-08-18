from tkinter import ttk, messagebox
from tkcalendar import *
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import csv
import time
from datetime import datetime, date
import os

def build_teacher_window(rootWindow: tk.Tk):
    UserApp = ctk.CTkToplevel(rootWindow)
    UserApp.geometry('800x580')
    UserApp.resizable(width=False, height=False)

    script_directory = os.path.dirname(os.path.abspath(__file__))
    background_image_location = os.path.join(script_directory, 'UserGUI.png')

    background_image = tk.PhotoImage(file = background_image_location)
    graphicL = tk.Label(UserApp, image = background_image)
    graphicL.pack()

    csv_file_path = os.path.join(script_directory, "teacher_absences.csv")
    absences = []

    def check_csv_file():
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["teacher code", "start time", "start date", "end time", "end date"])

    def write_data(): #command for submit button
        #user info
        TeacherCode = nameEntry.get()
        Startdate = startDateEntry.get()
        StartTime = startTimeEntry.get()
        Enddate = endDateEntry.get()
        EndTime = endTimeEntry.get()
        leavetype = combobox_var.get()

        #errors to make sure data is correct
        if leavetype==("Absence type"):
            messagebox.showerror('An error occured', 'Please choose your absence type.')
        
        elif Enddate < Startdate: #makes it so that user cannot choose invalid dates
            messagebox.showerror('An error occured', 'You have chosen an end date before your starting date.')
        elif TeacherCode == "": #doesnt allow Name to be blank
            messagebox.showerror('An error occured', 'Please insert your credentials.')
        elif Enddate == Startdate:
            if EndTime <= StartTime: #if day is the same teacher cannot choose end time before starting time
                    messagebox.showerror('An error occured', 'You must choose an end time after your starting time.')
            else:
                with open(csv_file_path, mode="a", newline="") as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow([TeacherCode, Startdate, StartTime, Enddate, EndTime])
                    messagebox.showinfo('Success', 'Absence successfully submitted.')
        else: #finally writes down the information in a CSV file
            with open("teacher absences.csv",mode="a", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([TeacherCode, Startdate, StartTime, Enddate, EndTime])
                messagebox.showinfo('Success', 'Absence successfully submitted.')

    #return to main page
    def returnToMain():
        UserApp.destroy()
        UserApp.deiconify

    def pick_date1(event):
        global cal1, date_window

        date_window = Toplevel()
        date_window.grab_set()
        date_window.title('select start of leave')
        date_window.geometry('250x220+590+370')
        cal1 = Calendar(date_window, selectmode="day", date_pattern="dd/mm/yy")
        cal1.place(x=0, y=0)
        submit_btn = Button(date_window, text="submit", command=grab_date1)
        submit_btn.place(x=100, y=190)
    
    #grab date1 command
    def grab_date1():
        startDateEntry.delete(0, END)
        startDateEntry.insert(0, cal1.get_date())
        date_window.destroy() #destroys window

    def pick_date2(event):
        global cal2, date_window

        date_window = Toplevel()
        date_window.grab_set()
        date_window.title('select end of leave')
        date_window.geometry('250x220+590+370')
        cal2 = Calendar(date_window, selectmode="day", date_pattern="dd/mm/yy")
        cal2.place(x = 0, y=0)

        submit_btn = Button(date_window, text="submit", command=grab_date2)
        submit_btn.place(x=100, y=190)

    def grab_date2():
        endDateEntry.delete(0, END)
        endDateEntry.insert(0, cal2.get_date())
        date_window.destroy()

    nameEntry = ctk.CTkEntry(master=UserApp, placeholder_text="Teacher Code", width=150, height=37, font=("Comic Sans", 16))
    nameEntry.place(x=337, y=100)

    startDateEntry = ctk.CTkEntry(master=UserApp, placeholder_text="Start Date", width=150, height=37)
    startDateEntry.place(x=187, y=162)
    startDateEntry.bind("<1>", pick_date1)

    endDateEntry = ctk.CTkEntry(master=UserApp, placeholder_text="End Date", width=150, height=37)
    endDateEntry.place(x=487, y=162)
    endDateEntry.bind("<1>", pick_date2)

    startTime_var = ctk.StringVar(value="option 8")
    startTimeEntry = ctk.CTkComboBox(UserApp, dropdown_fg_color="#f9f4f5", width=150, height=37, values=["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"], variable=startTime_var)
    startTime_var.set("Start Time")
    startTimeEntry.place(x=187, y=230)

    endTime_var = ctk.StringVar(value="option 8")
    endTimeEntry = ctk.CTkComboBox(UserApp, dropdown_fg_color="#f9f4f5",width=150, height=37, values=["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"], variable=endTime_var)
    endTime_var.set("End Time")
    endTimeEntry.place(x=487, y=230)

    combobox_var = ctk.StringVar(value="option 5")
    combobox = ctk.CTkComboBox(UserApp,dropdown_fg_color="#f9f4f5" ,width=150, height=37, values=["sick leave", "parental leave", "long service leave", "unpaid time off", "personal leave"], variable=combobox_var)
    combobox_var.set("Absence type")
    combobox.place(x=337, y=300)

    returnToLoginButton = ctk.CTkButton(UserApp, text="Return", height=50, width=150, fg_color="#f9f4f5", text_color="black", hover_color="#e8e3e4", command=returnToMain)
    returnToLoginButton.place(x=64,y=500)

    submitButton = ctk.CTkButton(UserApp, text="Submit", height=50, width=150, fg_color="#f9f4f5", text_color="black", hover_color="#e8e3e4", command=write_data)
    submitButton.place(x=586,y=500)

    UserApp.mainloop()

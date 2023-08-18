import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as customTkinter

from PIL import ImageTk, Image

from datetime import date
import time
from copy import copy

import os

import csv
import json

import sorting_algorithm

file_dir = os.path.dirname(os.path.abspath(__file__))
absencedata_path = os.path.join(file_dir, "teacher_absences.csv")
teacherlist_path = os.path.join(file_dir, "teacherlist.csv")
records_path = os.path.join(file_dir, "records.csv")

desktop_path = os.path.join(file_dir, "Desktop.png")

with open(absencedata_path, 'a') as f, open(teacherlist_path, 'a') as g:
    # just to create the files if they dont exist
    pass

# <FUNCTIONS>

def edit_file(
    options: dict[str, bool] = {"teacherlist.csv": False, "teacher_absences.csv": False},
    teacherTree: ttk.Treeview = None,
    absenceTree: ttk.Treeview = None,
):
    # if an option is not filled in, fill it in with false
    try:
        options["teacherlist.csv"]
    except (KeyError):
        options["teacherlist.csv"] = False

    try:
        options["teacher_absences.csv"]
    except KeyError:
        options["teacher_absences.csv"] = False

    for key, value in options.items():
        if value == True:
            treeVar = teacherTree if key == "teacherlist.csv" else absenceTree
            if treeVar == None:
                raise TypeError(
                    "The correct treeview variable needs to be provided for the file to be edited correctly."
                )
            with open(os.path.join(file_dir, f'temp{key}'), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')

                for row in treeVar.get_children():
                    tempRow = treeVar.item(row)
                    rowValues = tempRow["values"]

                    # made dynamic boys 😎
                    toWrite = []
                    for value in rowValues:
                        toWrite.append(value)
                    writer.writerow(toWrite)

            os.remove(file_dir + f'\\{key}')
            os.rename(file_dir + f'\\temp{key}', file_dir + f'\\{key}')

# reader needs to be a csv reader passed in
def sort_teachers_by_reliefs_EDIT(reader: list[list], teachersTree: ttk.Treeview):
    tempDict = {}

    try:
        for row in reader:
            tempDict[row[0]] = int(row[1])
    except ValueError:
        quit()  # make a correct return here

    sortedDict = sorting_algorithm.sort(tempDict)

    for item in teachersTree.get_children():
        teachersTree.delete(item)

    count = 0
    for key, value in sortedDict.items():
        count += 1
        teachersTree.insert("", tk.END, text="item" + str(count), values=[key, value])

    edit_file({"teacherlist.csv": True}, teacherTree=teachersTree)

# Create Function to go back to Login Page
def go_back_to_login():
    root.destroy()
    main_window.deiconify()

def delete_labels():
    for label in root.winfo_children():
        if type(label) == ttk.Label or type(label) == tk.Frame:
            label.destroy()

# Create Function into buttons from the main area
def show_entry(entry_text):

    for label in main_area.winfo_children():
        if type(label) == ttk.Label or type(label) == tk.Frame:
            label.destroy()
    label = ttk.Label(main_area, text=entry_text)
    label.pack()

# Home
def Home():
    for label in main_area.winfo_children():
        if type(label) == ttk.Label or type(label) == tk.Frame:
            label.destroy()
    for button in main_area.winfo_children():
        if type(button) == ttk.Button or type(button) == tk.Frame:
            button.destroy()
    return_button = ttk.Button(
        main_area, text="Return to Login", style="TButton", command=go_back_to_login
    )
    return_button.pack()

# function to draw up the treeview that should exist in the manage staff section
def build_manage_staff():
    # need this to ensure the vbar gets put side by side, cause the current widget is already managed by pack

    for label in main_area.winfo_children():
        if type(label) == ttk.Label or type(label) == tk.Frame or type(ttk.Treeview):
            label.destroy()
    for button in main_area.winfo_children():
        if type(button) == ttk.Button or type(button) == tk.Frame:
            button.destroy()
    treeviewGridDiv = tk.Frame(main_area)
    treeviewGridDiv.pack()
    absencesTree = ttk.Treeview(
        treeviewGridDiv,
        show="headings",
        columns=["code", "startTime", "startDate", "endTime", "endDate", "relief"],
        height=5,
    )  # table

    columnWidth = 70

    # to make it a for loop, so we don't have to have 10 ugly lines and it can be slightly dynamic
    columns = {
        "code": "Code",
        "startTime": "Start Time",
        "startDate": "Start Date",
        "endTime": "End Time",
        "endDate": "End Date",
        "relief": "Sub Code",
    }

    for key, value in columns.items():
        absencesTree.column(key, width=columnWidth)
        absencesTree.heading(key, text=value)

    absencesTree.grid(row=1, column=1)
    vbar = ttk.Scrollbar(
        treeviewGridDiv, orient=tk.VERTICAL, command=absencesTree.yview
    )
    absencesTree.configure(yscrollcommand=vbar.set)
    vbar.grid(row=1, column=2, sticky="ns")

    # checking that any data is not after the current time
    # if time to optimise, use the edit_file function for this probably (might need slight changes thats why its not done now)
    currentTime = time.time()
    with open(absencedata_path, 'r') as csvfile, open(os.path.join(file_dir, f'tempabsencedata.csv'), 'w', newline='') as wcsvfile, open(records_path, 'a', newline='') as rcsvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(wcsvfile, delimiter=',')
        recordsWriter = csv.writer(rcsvfile, delimiter=',')

        toWrite = []
        recordsToWrite = []
        for row in reader:
            try:
                constructedTime = time.strptime(f'{row[3]} {row[4]}', '%H:%M %d/%m/%Y')
                constructedSeconds = time.mktime(constructedTime)
            except ValueError:
                messagebox.showerror('An error occured', 'Your absence data file is not correctly formatted. Please call an administrator to resolve the issue.')
                quit()

            if constructedSeconds > currentTime:
                toWrite.append(row)
            else:
                recordsToWrite.append(row)

        # reappending to temp file
        for row in toWrite:
            writer.writerow(row)

        for row in recordsToWrite:
            recordsWriter.writerow(row)

    os.remove(os.path.join(file_dir, f'teacher_absences.csv'))
    os.rename(os.path.join(file_dir, f'tempabsencedata.csv'), os.path.join(file_dir, f'teacher_absences.csv'))

    for item in absencesTree.get_children():
        absencesTree.delete(item)

    # read data from the csv (yes, same code - needs to be in a function, in an optimised world)
    with open(absencedata_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in reader:
            count += 1
            absencesTree.insert(
                "",
                tk.END,
                text="item" + str(count),
                values=[row[0], row[1], row[2], row[3], row[4], row[5]],
            )
    # <RIGHT>

    def draw_data(event=None):
        topLevel = tk.Toplevel(root)
        topLevel.geometry("400x400")
        topLevel.resizable(width=False, height=False)
        topLevel.title("Select a substitute")

        selected = absencesTree.focus()

        if selected == '' or selected == None:
            topLevel.destroy()
            return

        item = absencesTree.item(selected)

        teachersTree = ttk.Treeview(
            topLevel, show="headings", columns=["code", "semReliefs"], height=18
        )  # table

        columnWidth = 125

        teachersTree.column("code", width=columnWidth)
        teachersTree.column("semReliefs", width=columnWidth)

        teachersTree.heading("code", text="Code")
        teachersTree.heading("semReliefs", text="Semester reliefs")

        teachersTree.grid(row=0, column=0)
        vbar = ttk.Scrollbar(topLevel, orient=tk.VERTICAL, command=teachersTree.yview)
        teachersTree.configure(yscrollcommand=vbar.set)
        vbar.grid(row=0, column=1, sticky="ns")

        for item_ in teachersTree.get_children():
            teachersTree.delete(item_)

        # read data from the csv (yes, same code - needs to be in a function, in an optimised world)
        with open(teacherlist_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            argument = [row for row in reader]

        sort_teachers_by_reliefs_EDIT(reader=argument, teachersTree=teachersTree)

        def select_sub(event=None):
            selectedTeacher = teachersTree.focus()
            teacherItem = teachersTree.item(selectedTeacher)

            if selectedTeacher == '' or selectedTeacher == None:
                return

            # check if the subteacherscode is assigned to any other teacher

            # HOW?!:
            # get all teachers in absencetree
            # if the teacher gotten is at the same index ['item'] = 0 as the one we are checking
            # ignore it
            # otherwise, check if the sub code we are attempting to set (subTeacherCode) belongs to anyone else

            # check if this (teacherItem["values"][0]) is preexist as a teacher code in the absences tree

            for items in absencesTree.get_children():
                seralizedItem = absencesTree.item(items)

                # check here that its not the same line
                if seralizedItem['text'] == item['text']:
                    continue

                # then here should be whether it is preexisting
                if seralizedItem['values'][5] == teacherItem["values"][0]:
                    tempbool = messagebox.askokcancel('Are you sure you want to do this?', 'This subsitute is already assigned to another absence.')
                    if tempbool == False:
                        return
                    break

            if item['values'][5] != 'n/a':
                subTeacherCode = item['values'][5]

                if subTeacherCode != 'n/a':
                    askOkBool = messagebox.askokcancel('Are you sure you want to do this?', 'You are current attempting to override the substitute previously assigned to this teacher. Are you sure you want to do this?')
                    if askOkBool == False:
                        return

                # on absences tree, check for which teacher has this code
                for teacherTreeItem in teachersTree.get_children():
                    newItem = teachersTree.item(teacherTreeItem)

                    # and remove this as a semester relief
                    if newItem["values"][0] == subTeacherCode:
                        newItem["values"][1] -= 1
                        teachersTree.item(
                            teacherTreeItem,
                            text=newItem["text"],
                            values=newItem["values"],
                        )

                        break

            item["values"][5] = teacherItem["values"][0]
            absencesTree.item(selected, text=item["text"], values=item["values"])

            teacherItem["values"][1] += 1
            teachersTree.item(
                selectedTeacher, text=teacherItem["text"], values=teacherItem["values"]
            )

            edit_file(
                {"teacherlist.csv": True, "teacher_absences.csv": True},
                teacherTree=teachersTree,
                absenceTree=absencesTree,
            )

            topLevel.destroy()

        teachersTree.bind("<Double-Button-1>", select_sub)

    # </RIGHT>

    absencesTree.bind("<Double-Button-1>", draw_data)

def build_view_records(event=None):
    for label in main_area.winfo_children():
            if type(label) == ttk.Label or type(label) == tk.Frame or type(ttk.Treeview):
                label.destroy()
    for button in main_area.winfo_children():
        if type(button) == ttk.Button or type(button) == tk.Frame:
            button.destroy()

    treeviewGridDiv = tk.Frame(main_area)
    treeviewGridDiv.pack()

    absencesTree = ttk.Treeview(
        treeviewGridDiv,
        show="headings",
        columns=["code", "startTime", "startDate", "endTime", "endDate", "relief"],
        height=5,
    )  # table

    columnWidth = 70

    # to make it a for loop, so we don't have to have 10 ugly lines and it can be slightly dynamic
    columns = {
        "code": "Code",
        "startTime": "Start Time",
        "startDate": "Start Date",
        "endTime": "End Time",
        "endDate": "End Date",
        "relief": "Sub Code",
    }

    for key, value in columns.items():
        absencesTree.column(key, width=columnWidth)
        absencesTree.heading(key, text=value)

    absencesTree.grid(row=1, column=1)
    vbar = ttk.Scrollbar(
        treeviewGridDiv, orient=tk.VERTICAL, command=absencesTree.yview
    )
    absencesTree.configure(yscrollcommand=vbar.set)
    vbar.grid(row=1, column=2, sticky="ns")

    # read data from the csv (yes, same code - needs to be in a function, in an optimised world)
    with open(records_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in reader:
            count += 1
            absencesTree.insert(
                "",
                tk.END,
                text="item" + str(count),
                values=[row[0], row[1], row[2], row[3], row[4], row[5]],
            )

    # <RIGHT>

# </FUNCTIONS>

def build_admin_menu(rootWindow=tk.Tk):
    global root
    global main_window
    main_window = rootWindow
    root = tk.Toplevel(rootWindow)
    root.title("Relief Teacher Selector")
    root.geometry("800x475")
    root.resizable(width=False, height=False)
    # Create a frame for the sidebar
    sidebar = tk.Frame(
        root, width=200, bg="#fff", height=500, relief="sunken", borderwidth=2
    )
    sidebar.pack(expand=False, fill="both", side="left", anchor="nw")

    # Create buttons in the sidebar with icons (using Unicode characters)
    home_button = ttk.Button(
        sidebar,
        text="🏠 Home",
        style="TButton",
        width=20,
        padding=(10, 5),
        command=Home
    )
    home_button.grid(row=1, column=1, ipady=10, ipadx=10)

    manage_staff_button = ttk.Button(
        sidebar,
        text="👥 Manage Staff",
        width=20,
        style="TButton",
        padding=(10, 50),
        command=build_manage_staff,
    )
    manage_staff_button.grid(row=50, column=1, ipady=10, ipadx=10)

    view_records_button = ttk.Button(
        sidebar,
        text="👀 View Records",
        width=20,
        style="TButton",
        padding=(10, 50),
        command=build_view_records,
    )
    view_records_button.grid(row=150, column=1, ipady=10, ipadx=10)
    

    # Create a frame for the main area
    
    global main_area

    main_area = tk.Frame(root)
    main_area.pack(expand=True, fill="both", side="right")

    # Colour scheme
    primary_purple = "#6A1B9A"
    secondary_purple = "#8E24AA"
    text_color = "#FFFFFF"
    bg_color = "#F3E5F5"

    # Set theme
    style = ttk.Style(root)
    style.theme_use("default")
    style.configure("TButton", font=("Arial", 12), background=primary_purple, foreground=text_color)
    style.map("TButton", background=[("active", secondary_purple)])

    # Apply colour scheme to sidebar
    sidebar.config(bg=primary_purple)

    # Apply colour scheme to main area
    main_area.config(bg=bg_color)

    # Add padding and alignment
    home_button.grid(row=1, column=1, ipady=10, ipadx=10, padx=20, pady=10)
    manage_staff_button.grid(row=2, column=1, ipady=10, ipadx=10, padx=20, pady=10)
    view_records_button.grid(row=3, column=1, ipady=10, ipadx=10, padx=20, pady=10)

    Home()

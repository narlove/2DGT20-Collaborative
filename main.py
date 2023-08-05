import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import date
from copy import copy

import os

import csv

import sorting_algorithm

# <FUNCTIONS>

def edit_file(options: dict[str, bool] = {'teacherlist.csv': False, 'absencedata.csv': False}, teacherTree: ttk.Treeview = None, absenceTree: ttk.Treeview = None):
    # if an option is not filled in, fill it in with false
    try:
        options['teacherlist.csv']
    except (KeyError):
        options['teacherlist.csv'] = False

    try:
        options['absencedata.csv']
    except KeyError:
        options['absencedata.csv'] = False

    for key, value in options.items():
        if value == True:
            treeVar = teacherTree if key == 'teacherlist.csv' else absenceTree
            if treeVar == None: raise TypeError('The correct treeview variable needs to be provided for the file to be edited correctly.')
            with open(f'temp{key}', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')

                for row in treeVar.get_children():
                    tempRow = treeVar.item(row)
                    rowValues = tempRow['values']

                    # made dynamic boys 😎
                    toWrite = []
                    for value in rowValues:
                        toWrite.append(value)
                    writer.writerow(toWrite)

            basePath = os.getcwd()
            os.remove(basePath + f'/{key}')
            os.rename(basePath + f'/temp{key}', basePath + f'/{key}')

# reader needs to be a csv reader passed in
def sort_teachers_by_reliefs_EDIT(reader: list[list], teachersTree: ttk.Treeview):
    tempDict = {}

    try:
        for row in reader:
            tempDict[row[0]] = int(row[1])
    except ValueError:
        quit() # make a correct return here       

    sortedDict = sorting_algorithm.sort(tempDict)

    for item in teachersTree.get_children():
        teachersTree.delete(item)

    count = 0
    for key, value in sortedDict.items():
        count += 1
        teachersTree.insert('', tk.END, text="item"+str(count), values=[key, value])
        
    edit_file({ 'teacherlist.csv': True }, teacherTree=teachersTree)

def delete_labels():
    for label in (walrus := main_area.winfo_children()):
        if type(label) == ttk.Label or type(label) == tk.Frame:
            label.destroy()

    print(walrus)

# Create Function into buttons from the main area
def show_entry(entry_text):
    label = ttk.Label(main_area, text=entry_text)
    label.pack()

# function to draw up the treeview that should exist in the manage staff section
def build_manage_staff():
    # need this to ensure the vbar gets put side by side, cause the current widget is already managed by pack
    treeviewGridDiv = tk.Frame(main_area)
    treeviewGridDiv.pack()

    absencesTree = ttk.Treeview(
        treeviewGridDiv,
        show="headings",
        columns=["code", "startTime", "startDate", "endTime", "endDate", "relief"], 
        height=5
    )  # table

    columnWidth = 70

    # to make it a for loop, so we don't have to have 10 ugly lines and it can be slightly dynamic
    columns = {
        'code': 'Code',
        'startTime': 'Start Time',
        'startDate': 'Start Date',
        'endTime': 'End Time',
        'endDate': 'End Date',
        'relief': 'Sub Code'
    }

    for key, value in columns.items():
        absencesTree.column(key, width=columnWidth)
        absencesTree.heading(key, text=value)

    absencesTree.grid(row=1, column=1)
    vbar = ttk.Scrollbar(treeviewGridDiv, orient=tk.VERTICAL, command=absencesTree.yview)
    absencesTree.configure(yscrollcommand=vbar.set)
    vbar.grid(row=1, column=2, sticky='ns')

    for item in absencesTree.get_children():
        absencesTree.delete(item)

    # read data from the csv (yes, same code - needs to be in a function, in an optimised world)
    with open('absencedata.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in reader:
            count += 1
            absencesTree.insert('', tk.END, text="item"+str(count), values=[row[0], row[1], row[2], row[3], row[4], row[5]])

    # <RIGHT>

    def draw_data(event=None):
        topLevel = tk.Toplevel(root)
        topLevel.geometry('400x400')
        topLevel.resizable(width=False, height=False)
        topLevel.title('Select a substitute')

        selected = absencesTree.focus()
        item = absencesTree.item(selected)

        teachersTree = ttk.Treeview(
            topLevel,
            show="headings",
            columns=["code", "semReliefs"], 
            height=18
        )  # table

        columnWidth = 125

        teachersTree.column('code', width=columnWidth)
        teachersTree.column('semReliefs', width=columnWidth)

        teachersTree.heading('code', text='Code')
        teachersTree.heading('semReliefs', text='Semester reliefs')

        teachersTree.grid(row=0, column=0)
        vbar = ttk.Scrollbar(topLevel, orient=tk.VERTICAL, command=teachersTree.yview)
        teachersTree.configure(yscrollcommand=vbar.set)
        vbar.grid(row=0, column=1, sticky='ns')

        for item in teachersTree.get_children():
            teachersTree.delete(item)

        # read data from the csv (yes, same code - needs to be in a function, in an optimised world)
        with open('teacherlist.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            argument = [row for row in reader]
        
        sort_teachers_by_reliefs_EDIT(reader=argument, teachersTree=teachersTree)

            # count = 0
            # for row in reader:
            #     count += 1
            #     teachersTree.insert('', tk.END, text="item"+str(count), values=[row[0], row[1]])

        def select_sub(event=None):
            selectedTeacher = teachersTree.focus()
            teacherItem = teachersTree.item(selectedTeacher)

            if item['values'][5] != 'n/a':
                subTeacherCode = item['values'][5]
                
                # on absences tree, check for which teacher has this code
                for teacherTreeItem in teachersTree.get_children():
                    newItem = teachersTree.item(teacherTreeItem)

                    # and remove this as a semester relief
                    if newItem['values'][0] == subTeacherCode:
                        newItem['values'][1] -= 1
                        teachersTree.item(teacherTreeItem, text=newItem['text'], values=newItem['values'])

                        break

            item['values'][5] = teacherItem['values'][0]
            absencesTree.item(selected, text=item['text'], values=item['values'])

            teacherItem['values'][1] += 1
            teachersTree.item(selectedTeacher, text=teacherItem['text'], values=teacherItem['values'])

            edit_file({ 'teacherlist.csv': True, 'absencedata.csv': True}, teacherTree=teachersTree, absenceTree=absencesTree)

            topLevel.destroy()

        teachersTree.bind("<Double-Button-1>", select_sub)

    # </RIGHT>

    absencesTree.bind("<Double-Button-1>", draw_data)

# </FUNCTIONS>

root = tk.Tk()
root.title("Relief Teacher Selector")
root.geometry("800x475")
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", lambda: quit())

# Set style
style = ttk.Style(root)
style.theme_use("default")
style.configure("Home_label", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Home_label', background=[('selected', '#347083')])  # change the color of selected row

# Set style for Button
style.configure('TButton', font=('Arial', 12), bd=0, anchor='w')
style.map('TButton', background=[('active', '#eee')])  # change to a light gray color on hover

# Create a frame for the sidebar
sidebar = tk.Frame(root, width=200, bg='#fff', height=500, relief='sunken', borderwidth=2)
sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

# Create buttons in the sidebar with icons (using Unicode characters)
home_button = ttk.Button(sidebar, text="🏠 Home", style='TButton', width=20, padding=(10, 5), command=lambda: show_entry("Home"))
home_button.grid(row=1, column=1, ipady=10, ipadx=10)

manage_staff_button = ttk.Button(sidebar, text="👥 Manage Staff", width=20, style='TButton', padding=(10, 50), command=build_manage_staff)
manage_staff_button.grid(row=50, column=1, ipady=10, ipadx=10)

manage_lessons_button = ttk.Button(sidebar, text="📅 Manage Lessons", width=20, style='TButton', padding=(10, 50), command=lambda: show_entry("Manage Lessons"))
manage_lessons_button.grid(row=100, column=1, ipady=10, ipadx=10)

view_records_button = ttk.Button(sidebar, text="👀 View Records", width=20, style='TButton', padding=(10, 50), command=lambda: show_entry("View Records"))
view_records_button.grid(row=150, column=1, ipady=10, ipadx=10)

# Create a frame for the main area
main_area = tk.Frame(root, bg='white')
main_area.pack(expand=True, fill='both', side='right')

Home_Label=ttk.Label(main_area, text= "Home" )

# Create button to clear all labels
clear_button = ttk.Button(main_area, text="Clear Labels", command=delete_labels)
clear_button.pack()

root.mainloop()

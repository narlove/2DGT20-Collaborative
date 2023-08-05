import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import date
from copy import copy

import os

import csv

import sorting_algorithm
        
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", lambda: quit())
root.geometry('900x400')
root.title('Administrator menu')

root.resizable(width=False, height=False)

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
    print(sortedDict)

    for item in teachersTree.get_children():
        teachersTree.delete(item)

    count = 0
    for key, value in sortedDict.items():
        count += 1
        teachersTree.insert('', tk.END, text="item"+str(count), values=[key, value])
        
    edit_file({ 'teacherlist.csv': True }, teacherTree=teachersTree)

# </FUNCTIONS>

# <BANNER>
outerBannerDiv = ttk.Frame(root)
outerBannerDiv.pack(side='top', ipadx=500)

banner = ttk.Label(outerBannerDiv, text='', font=('Sarabun', 30, 'bold'), background='#a31b37', padding=15, anchor='n', width=100)
banner.place(x=0, y=0)

innerBannerDiv = tk.Frame(outerBannerDiv, bg='#a31b37')
innerBannerDiv.pack(pady=12.5, side='top')

text = tk.Label(innerBannerDiv, text='placeholder', foreground='white', bg='#a31b37', font=('Sarabun', 30, 'bold'))
text.grid(column=0, row=0)

text.grid_configure(padx=(0, 30))

# </BANNER>

# <MAIN>

leftBodyDiv = tk.Frame(root)
leftBodyDiv.pack(side='left', padx=(50, 0))

rightBodyDiv = tk.Frame(root)
rightBodyDiv.pack(side='right', padx=(0, 50))

# </MAIN>

# <LEFT>

absenteeLabel = tk.Label(leftBodyDiv, text='Leave requests')
absenteeLabel.grid(column=1, row=0)

absencesTree = ttk.Treeview(
    leftBodyDiv,
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
vbar = ttk.Scrollbar(leftBodyDiv, orient=tk.VERTICAL, command=absencesTree.yview)
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

# </LEFT>

root.mainloop()
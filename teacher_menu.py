import csv
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import tkcalendar
from tkcalendar import DateEntry 

# Initialize the TeacherAbsenceTracker class
class TeacherAbsenceTracker:
    def __init__(self, rootWindow = tk.Tk):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.csv_file_path = os.path.join(self.script_directory, "absencedata.csv")
        self.absences = []

        self.rootWindow = rootWindow
        
        self.selected_start_time = tk.StringVar()  # Initialize the selected start time
        self.selected_end_time = tk.StringVar()    # Initialize the selected end time

    # Check if the CSV file exists. If not, create the file with header columns.
    def check_csv_file(self):
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["teacher code", "start time", "start date", "end time", "end date"])

    # Save the teacher absences to the CSV file
    def save_absences(self):
        with open(self.csv_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            for absence in self.absences:
                teacher_code = absence["teacher_code"]
                start_time = absence["start_time"]
                start_date = absence["start_date"]
                end_time = absence["end_time"]
                end_date = absence["end_date"]
                writer.writerow([teacher_code, start_time, start_date, end_time, end_date, "n/a"])

    # Start the application by checking CSV file, loading existing absences, and creating the GUI
    def run(self):
        self.check_csv_file()
        self.load_absences()
        self.create_gui()

    # Load teacher absences from the CSV file into the absences list
    def load_absences(self):
        try:
            with open(self.csv_file_path, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        teacher_code, start_time, start_date, end_time, end_date = row[:5]
                        self.absences.append({
                            "teacher_code": teacher_code,
                            "start_time": start_time,
                            "start_date": start_date,
                            "end_time": end_time,
                            "end_date": end_date
                        })
                    except ValueError:
                        print(f"Skipping invalid row: {row}")
        except FileNotFoundError:
            pass

    # Submit a new absence request for a teacher
    def submit_absence(self):
        teacher_code = self.entry_teacher_code.get()
        start_date = self.entry_start_date.get_date().strftime("%d/%m/%Y")
        start_time = self.selected_start_time.get()  # Use the selected start time from the dropdown
        end_time = self.selected_end_time.get()  # Use the selected end time from the dropdown
        end_date = self.entry_end_date.get_date().strftime("%d/%m/%Y")

        if not teacher_code or not start_date or not start_time or not end_time or not end_date:
            messagebox.showerror("Error", "All fields are required.")
            return

        absence_data = {
            "teacher_code": teacher_code,
            "start_time": start_time,
            "start_date": start_date,
            "end_time": end_time,
            "end_date": end_date,
            "relief": "n/a"
        }
        self.absences.append(absence_data)
        self.save_absences()

        messagebox.showinfo("Success", "Absence submitted successfully.")
        self.clear_input_fields()

    # Clear input fields after submitting an absence
    def clear_input_fields(self):
        self.entry_teacher_code.delete(0, tk.END)
        self.selected_start_time.set("")  # Clear the selected start time
        self.selected_end_time.set("")  # Clear the selected end time
        self.entry_start_date.set_date(None)  # Clear the start date entry
        self.entry_end_date.set_date(None)  # Clear the end date entry

    # Create the GUI for the application
    def create_gui(self):
        self.window = tk.Toplevel(self.rootWindow)
        self.window.protocol("WM_DELETE_WINDOW", lambda: quit())
        self.window.geometry('1150x400')
        self.window.title('Teacher Absence Tracker')
        self.window.resizable(width=False, height=False)

        outerBannerDiv = ttk.Frame(self.window)
        outerBannerDiv.pack(side='top', ipadx=500)

        banner = ttk.Label(outerBannerDiv, text='', font=('Sarabun', 30, 'bold'), background='#a31b37', padding=15, anchor='n', width=100)
        banner.place(x=0, y=0)

        innerBannerDiv = tk.Frame(outerBannerDiv, bg='#a31b37')
        innerBannerDiv.pack(pady=12.5, side='top')

        text = tk.Label(innerBannerDiv, text='Teacher Absence Tracker', foreground='white', bg='#a31b37', font=('Sarabun', 30, 'bold'))
        text.grid(column=0, row=0)

        text.grid_configure(padx=(0, 30))

        leftBodyDiv = tk.Frame(self.window)
        leftBodyDiv.pack(side='left', padx=(50, 0))

        rightBodyDiv = tk.Frame(self.window)
        rightBodyDiv.pack(side='right', padx=(0, 50))

        # Display teacher absences in a Treeview widget
        absenteeLabel = tk.Label(leftBodyDiv, text='Teacher Leave requests')
        absenteeLabel.grid(column=1, row=0)

        columnWidth = 125  # You can adjust this value based on your preference

        # Create the Treeview widget
        self.absencesTree = ttk.Treeview(
            leftBodyDiv,
            show="headings",
            columns=["teacher_name", "start_time", "start_date", "end_time", "end_date", "relief"],
            height=5
        )

        # Configure columns and headings
        columns = {
            "teacher_name": 'Teacher Code',
            "start_time": 'Start Time',
            "start_date": 'Start Date',
            "end_time": 'End Time',
            "end_date": 'End Date',
            "relief": "Substitute Code"
        }

        for col_id, col_heading in columns.items():
            self.absencesTree.column(col_id, width=columnWidth)
            self.absencesTree.heading(col_id, text=col_heading)

        # Set up Treeview layout and scrollbar
        self.absencesTree.grid(row=1, column=1)
        vbar = ttk.Scrollbar(leftBodyDiv, orient=tk.VERTICAL, command=self.absencesTree.yview)
        self.absencesTree.configure(yscrollcommand=vbar.set)
        vbar.grid(row=1, column=2, sticky='ns')

        # Clear any existing items
        for item in self.absencesTree.get_children():
            self.absencesTree.delete(item)

        # Load existing absences into the Treeview
        with open(self.csv_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                count += 1
                if len(row) >= 5:
                    teacher_code, start_time, start_date, end_time, end_date, relief = row
                else:
                    # Handle rows with fewer than 5 values
                    teacher_code = start_time = start_date = end_time = end_date = ""
                    for i, value in enumerate(row):
                        if i == 0:
                            teacher_code = value
                        elif i == 1:
                            start_time = value
                        elif i == 2:
                            start_date = value
                        elif i == 3:
                            end_time = value
                        elif i == 4:
                            end_date = value
                        elif i == 5:
                            relief = value
                self.absencesTree.insert('', tk.END, values=[teacher_code, start_time, start_date, end_time, end_date, "n/a"])

        # Display input fields and submission button on the right side
        label_teacher_code = tk.Label(rightBodyDiv, text="Teacher Code:")
        label_teacher_code.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.entry_teacher_code = tk.Entry(rightBodyDiv)
        self.entry_teacher_code.grid(row=4, column=1, padx=5, pady=5)

        # Dropdown menu for selecting start time
        start_time_label = tk.Label(rightBodyDiv, text="Start Time:")
        start_time_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        start_time_values = ["08:00", "09:00", "10:00", "11:00", "12:00",
                             "13:00", "14:00", "15:00", "16:00", "17:00"]
        start_time_menu = ttk.Combobox(rightBodyDiv, textvariable=self.selected_start_time, values=start_time_values)
        start_time_menu.grid(row=5, column=1, padx=5, pady=5)

        # Dropdown menu for selecting end time
        end_time_label = tk.Label(rightBodyDiv, text="End Time:")
        end_time_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        end_time_values = ["08:00", "09:00", "10:00", "11:00", "12:00",
                           "13:00", "14:00", "15:00", "16:00", "17:00"]
        end_time_menu = ttk.Combobox(rightBodyDiv, textvariable=self.selected_end_time, values=end_time_values)
        end_time_menu.grid(row=6, column=1, padx=5, pady=5)

        label_start_date = tk.Label(rightBodyDiv, text="Start Date:")
        label_start_date.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

        self.entry_start_date = tkcalendar.DateEntry(rightBodyDiv)
        self.entry_start_date.grid(row=7, column=1, padx=5, pady=5)

        label_end_date = tk.Label(rightBodyDiv, text="End Date:")
        label_end_date.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

        self.entry_end_date = tkcalendar.DateEntry(rightBodyDiv)
        self.entry_end_date.grid(row=8, column=1, padx=5, pady=5)

        # Create the "Submit" button
        submit_button = tk.Button(rightBodyDiv, text="Submit Absence", command=self.submit_absence)
        submit_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10)


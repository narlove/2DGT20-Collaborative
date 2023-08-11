import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import tkcalendar 

# Initialize the TeacherAbsenceTracker class
class TeacherAbsenceTracker:
    def __init__(self, rootWindow = tk.Tk):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.csv_file_path = os.path.join(self.script_directory, "teacher_absences.csv")
        self.absences = []

        self.rootWindow = rootWindow

        self.lesson_periods = ["Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4"]
        self.lesson_to_index = {lesson: idx for idx, lesson in enumerate(self.lesson_periods)}

    # Check if the CSV file exists. If not, create the file with header columns.
    def check_csv_file(self):
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["full_name", "date_str", "lesson_name"])

    # Save the teacher absences to the CSV file
    def save_absences(self):
        with open(self.csv_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["full_name", "date_str", "lesson_name"])
            for absence in self.absences:
                full_name, date_str, lesson = absence
                lesson_name = self.lesson_periods[lesson]
                writer.writerow([full_name, date_str, lesson_name])

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
                        full_name, date_str, lesson_name = row[:3]
                        if lesson_name.isdigit():
                            lesson = int(lesson_name)
                        else:
                            lesson = self.lesson_to_index.get(lesson_name)
                        if lesson is not None and lesson in range(len(self.lesson_periods)):
                            self.absences.append([full_name, date_str, lesson])
                    except ValueError:
                        print(f"Skipping invalid row: {row}")
        except FileNotFoundError:
            pass

    # Submit a new absence request for a teacher
    def submit_absence(self):
        start_date = self.calendar.get_date()
        lesson = self.selected_lesson.get()

        if not start_date or not lesson:
            messagebox.showerror("Error", "All fields are required.")
            return

        lesson_index = self.lesson_to_index.get(lesson)

        if lesson_index is None:
            messagebox.showerror("Error", "Invalid lesson period.")
            return

        absence_data = [self.entry_full_name.get(), start_date.strftime("%Y-%m-%d"), lesson_index]
        self.absences.append(absence_data)
        self.save_absences()

        messagebox.showinfo("Success", "Absence submitted successfully.")
        self.clear_input_fields()

    # Clear input fields after submitting an absence
    def clear_input_fields(self):
        self.calendar.delete(0, tk.END)
        self.selected_lesson.set("")

    # Create the GUI for the application
    def create_gui(self):
        self.window = tk.Toplevel(self.rootWindow)
        self.window.protocol("WM_DELETE_WINDOW", lambda: quit())
        self.window.geometry('1000x400')
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

        self.absencesTree = ttk.Treeview(
            leftBodyDiv,
            show="headings",
            columns=["teacher_name", "dates", "lesson_period"],
            height=5
        )  

        # Set column widths and headings for the Treeview
        columnWidth = 200
        columns = {
            'teacher_name': 'Teacher Name',
            'dates': 'Dates',
            'lesson_period': 'Lesson Period'
        }

        for key, value in columns.items():
            self.absencesTree.column(key, width=columnWidth)
            self.absencesTree.heading(key, text=value)

        self.absencesTree.grid(row=1, column=1)
        vbar = ttk.Scrollbar(leftBodyDiv, orient=tk.VERTICAL, command=self.absencesTree.yview)
        self.absencesTree.configure(yscrollcommand=vbar.set)
        vbar.grid(row=1, column=2, sticky='ns')

        for item in self.absencesTree.get_children():
            self.absencesTree.delete(item)

        # Load existing absences into the Treeview
        with open(self.csv_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                count += 1
                full_name, date_str, lesson_name = row
                self.absencesTree.insert('', tk.END, text="item" + str(count), values=[full_name, date_str, lesson_name])


        # Display input fields and submission button on the right side
        label_full_name = tk.Label(rightBodyDiv, text="Full Name:")
        label_full_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.entry_full_name = tk.Entry(rightBodyDiv)
        self.entry_full_name.grid(row=0, column=1, padx=5, pady=5)

        label_dates = tk.Label(rightBodyDiv, text="Select Dates:")
        label_dates.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.calendar = tkcalendar.DateEntry(rightBodyDiv, width=12, background='#A31B37',
                                  foreground='white', borderwidth=2)
        self.calendar.grid(row=1, column=1, padx=5, pady=5)

        label_lesson = tk.Label(rightBodyDiv, text="Select Lesson Period:")
        label_lesson.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.selected_lesson = tk.StringVar(rightBodyDiv)
        self.lesson_dropdown = ttk.Combobox(rightBodyDiv, textvariable=self.selected_lesson,
                                            values=self.lesson_periods, width=15)
        self.lesson_dropdown.grid(row=2, column=1, padx=5, pady=5)

        button_frame = tk.Frame(rightBodyDiv)
        button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_absence)
        submit_button.pack(side=tk.LEFT, padx=5)

if __name__ == '__main__':
    root = tk.Tk()
    newInstance = TeacherAbsenceTracker(root)
    newInstance.run()

    root.withdraw()

    root.mainloop()
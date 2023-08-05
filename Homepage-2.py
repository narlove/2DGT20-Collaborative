import tkinter as tk
from tkinter import ttk

def delete_labels():
    for label in main_area.winfo_children():
        if type(label) == ttk.Label:
            label.destroy()

root = tk.Tk()
root.title("Relief Teacher Selector")
root.geometry("800x475")

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

manage_staff_button = ttk.Button(sidebar, text="👥 Manage Staff", width=20, style='TButton', padding=(10, 50), command=lambda: show_entry("Manage Staff"))
manage_staff_button.grid(row=50, column=1, ipady=10, ipadx=10)

manage_lessons_button = ttk.Button(sidebar, text="📅 Manage Lessons", width=20, style='TButton', padding=(10, 50), command=lambda: show_entry("Manage Lessons"))
manage_lessons_button.grid(row=100, column=1, ipady=10, ipadx=10)

view_records_button = ttk.Button(sidebar, text="👀 View Records", width=20, style='TButton', padding=(10, 50), command=lambda: show_entry("View Records"))
view_records_button.grid(row=150, column=1, ipady=10, ipadx=10)

# Create a frame for the main area
main_area = tk.Frame(root, bg='white')
main_area.pack(expand=True, fill='both', side='right')

# Create Function into buttons from the main area
def show_entry(entry_text):
    label = ttk.Label(main_area, text=entry_text)
    label.pack()

Home_Label=ttk.Label(main_area, text= "Home" )

# Create button to clear all labels
clear_button = ttk.Button(main_area, text="Clear Labels", command=delete_labels)
clear_button.pack()

root.mainloop()

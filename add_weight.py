import tkinter as tk
from tkinter import ttk, messagebox

import add_exercise_log
import database_functions


class AddWeight(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        # def insert_weight(my_cursor, lifter_id, weight, date, notes):
        # Create cursor and set the database connection
        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()
        self.updated = False
        frame1 = tk.Frame(self)
        frame1.pack()

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Set the window title and geometry
        self.title("Add Weigh In")
        self.geometry("400x400")

        self.grid_frame = tk.Frame(frame1)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lifter_label = tk.Label(self.grid_frame, text="Select Lifter")
        self.lifter_combo = ttk.Combobox(self.grid_frame)
        self.lifter_combo["values"] = [lifter[1] for lifter in self.get_lifters()]
        self.lifter_combo["state"] = "readonly"

        self.weight_label = tk.Label(self.grid_frame, text="Enter Weight:")
        self.weight_entry = tk.Entry(self.grid_frame)

        self.date_label = tk.Label(self.grid_frame, text="Date (YYYY-MM-DD)")
        self.date_entry = tk.Entry(self.grid_frame)

        self.notes_label = tk.Label(self.grid_frame, text="Enter Notes:")
        self.notes_entry = tk.Entry(self.grid_frame)
        # self.notes_entry.configure(width=20, height=5)

        self.enter_weight_button = tk.Button(self.grid_frame, text="Enter Weight", command=self.add_weight)
        self.back_button = tk.Button(self.grid_frame, text="Back", command=self.go_back)

        self.list_weights = tk.Listbox(frame2)

        self.lifter_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.lifter_combo.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.weight_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.weight_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.date_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry.grid(row=2, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.notes_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.notes_entry.grid(row=3, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.enter_weight_button.grid(row=4, column=0)
        self.back_button.grid(row=4, column=1)
        self.list_weights.pack(fill=tk.BOTH, expand=True)
        self.lifter_combo.bind("<<ComboboxSelected>>", self.update_weight_history)

    def get_lifters(self):
        # Get the list of exercises from the database
        lifters = database_functions.get_lifters(self.my_cursor)
        # Extract the lifter id and names from the tuples
        lifter_names = [(lifter[0], lifter[1]) for lifter in lifters]
        return lifter_names

    def add_weight(self):
        lifter_id = add_exercise_log.get_item_id(self.lifter_combo, self.get_lifters())
        weight = self.weight_entry.get()
        date = self.date_entry.get()
        notes = self.notes_entry.get()

        database_functions.insert_weight(self.my_cursor, lifter_id, weight, date, notes)

    def update_weight_history(self, event):
        selected_lifter = add_exercise_log.get_item_id(self.lifter_combo, self.get_lifters())
        weight_history = database_functions.get_weight_history(self.my_cursor, selected_lifter)
        self.list_weights.delete(0, tk.END)  # Clear the listbox
        for weight_entry in weight_history:
            self.list_weights.insert(tk.END, weight_entry)

    def go_back(self):
        if self.updated:
            result = messagebox.askyesno("Commit?", "Changes have been made to the database, would you like to commit?")
            if result:
                database_functions.commit_changes(self.mydb)
            else:
                messagebox.showinfo("Notification", "Changes have not been committed")
        self.destroy()
        self.master.deiconify()

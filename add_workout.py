import tkinter as tk
from tkinter import messagebox

import database_functions


class AddWorkout(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        # Create cursor and set the database connection
        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()
        self.updated = False

        # Set the window title and geometry
        self.title("Add Workout")
        self.geometry("400x400")

        # Create and pack first frame to hold entry fields for adding new workouts
        frame1 = tk.Frame(self)
        frame1.pack()

        # Create and pack second frame to hold exercises by workout at bottom of page
        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create label and entry for date
        self.date_label = tk.Label(frame1, text="Date:")
        self.date_entry = tk.Entry(frame1)

        # Create label and entry for notes
        self.note_label = tk.Label(frame1, text="Notes:")
        self.note_entry = tk.Entry(frame1)

        # Create button to execute adding workout and a button to return to main window
        self.add_button = tk.Button(frame1, text="Add Workout",
                                    command=lambda: self.add_workout())
        self.back_button = tk.Button(frame1, text="Back", command=self.go_back)

        # Place labels, entries and buttons
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.note_label.grid(row=1, column=0, padx=5, pady=5)
        self.note_entry.grid(row=1, column=1, padx=5, pady=5)
        self.add_button.grid(row=2, column=0, padx=5, pady=5)
        self.back_button.grid(row=2, column=1, padx=5, pady=5)

        # Create and place a resizeable listbox to hold and display workouts already in the database.
        self.workout_listbox = tk.Listbox(frame2)
        self.workout_listbox.pack(fill=tk.BOTH, expand=True)

        # Populates list box when window is created
        self.update_workout_listbox()

    # Called when window is first created and when a workout is inserted into the database. Re-queries the database and
    # populates workout listbox.
    def update_workout_listbox(self):
        self.workout_listbox.delete(0, "end")  # Clear the current items in the listbox
        workouts = database_functions.get_workouts(self.my_cursor)  # Get latest workouts from database
        for workout in workouts:
            self.workout_listbox.insert("end", f"{workout[0]} | Date: {workout[1]} Notes: {workout[2]}")

    # Called when add workout button is pressed. Attempts to insert a new workout into the database with data from
    # the Entries
    def add_workout(self):
        database_functions.add_workout(self.my_cursor, self.date_entry.get(), self.note_entry.get())
        if self.update_workout_listbox():  # Call method to update the listbox after a new workout is added
            self.date_entry.delete(0, "end")  # Clear date entry
            self.note_entry.delete(0, "end")  # Clear note entry
            self.updated = True

    # If workouts have been added to the database, prompts the user to commit, and commits when yes is selected. Then
    # destroys self and returns to main window.
    def go_back(self):
        if self.updated:
            result = messagebox.askyesno("Commit?", "Changes have been made to the database, would you like to commit?")
            if result:
                database_functions.commit_changes(self.mydb)
            else:
                messagebox.showinfo("Notification", "Changes have not been committed")
        self.destroy()
        self.master.deiconify()

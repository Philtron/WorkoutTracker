import tkinter as tk
from tkinter import messagebox

import database_functions


class MainWindow(tk.Tk):
    def __init__(self, db_connection):
        super().__init__()

        self.mydb = db_connection

        self.title("Workout App")
        self.geometry("500x500")

        menu_frame = tk.Frame(self)
        menu_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create buttons for each menu option
        add_workout_button = tk.Button(menu_frame, text="Enter new workout", command=self.add_workout)
        add_workout_button.pack(fill="both", expand=True)

        add_exercise_button = tk.Button(menu_frame, text="Enter new exercise", command=self.add_exercise)
        add_exercise_button.pack(fill="both", expand=True)

        list_lifters_button = tk.Button(menu_frame, text="List lifters", command=self.list_lifters)
        list_lifters_button.pack(fill="both", expand=True)

        list_exercises_button = tk.Button(menu_frame, text="List exercises", command=self.list_exercises)
        list_exercises_button.pack(fill="both", expand=True)

        list_workouts_button = tk.Button(menu_frame, text="List workouts", command=self.list_workouts)
        list_workouts_button.pack(fill="both", expand=True)

        exit_button = tk.Button(menu_frame, text="Exit", command=self.quit)
        exit_button.pack(fill="both", expand=True)

    def add_workout(self):
        messagebox.showinfo("Add Workout")
        # add_workout(self.my_cursor)
        # self.mydb.commit()

    def add_exercise(self):
        messagebox.showinfo("Add Exercise")

        # workout_id = input("Enter the workout ID you want to attach this exercise log entry to: ")
        # add_exercise(self.my_cursor, workout_id)
        # self.mydb.commit()

    def list_lifters(self):
        # messagebox.showinfo("List Lifters")
        my_cursor = self.mydb.cursor()
        lifters = database_functions.get_lifters(my_cursor)

        lifter_window = tk.Toplevel(self)
        lifter_window.title("Lifters")
        lifter_window.geometry("200x200")

        lifter_listbox = tk.Listbox(lifter_window)
        lifter_listbox.pack(fill="both", expand=True)

        for lifter in lifters:
            lifter_listbox.insert("end", f"{lifter[1]}, (ID: {lifter[0]})")

    def list_exercises(self):
        messagebox.showinfo("List Exercises")

        database_functions.get_exercises(self.mydb.cursor())

    def list_workouts(self):
        messagebox.showinfo("List Workouts")

        database_functions.get_workouts(self.mydb.cursor())

# app = MainWindow()
# app.mainloop()

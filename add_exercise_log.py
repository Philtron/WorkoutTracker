import tkinter as tk
from tkinter import messagebox

import database_functions


def get_id(id_string):
    split_list = id_string.split(", ")
    return int(split_list[0][1:])


class AddExercise(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        # Create cursor and set database connection
        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()

        # Boolean to track a change being made, used when exiting the window to prompt for a commit
        self.updated = False

        # Set the window title and geometry
        self.title("Add Exercise Log")
        self.geometry("300x300")

        # Creates a resizeable grid frame to hold input widgets, labels and buttons
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        # Create OptionMenu and label to allow user to select from existing workouts
        self.workout_label = tk.Label(self.grid_frame, text="Workouts")
        self.workout_options = tk.StringVar(self.grid_frame)
        self.workout_options.set("")
        self.workout_option_menu = tk.OptionMenu(self.grid_frame, self.workout_options, *self.get_workouts())

        # Create OptionMenu and label to allow user to select from list of existing exercises
        self.exercise_label = tk.Label(self.grid_frame, text="Exercises")
        self.exercise_options = tk.StringVar(self.grid_frame)
        self.exercise_options.set("")
        self.exercise_option_menu = tk.OptionMenu(self.grid_frame, self.exercise_options, *self.get_exercises())

        # Create OptionMenu and label to allow user to select from list of existing lifters
        self.lifter_label = tk.Label(self.grid_frame, text="Lifters")
        self.lifter_options = tk.StringVar(self.grid_frame)
        self.lifter_options.set("")
        self.lifter_option_menu = tk.OptionMenu(self.grid_frame, self.lifter_options, *self.get_lifters())

        # Create labels and entries for user to enter values for the log
        self.weight_label = tk.Label(self.grid_frame, text="Weight")
        self.weight_entry = tk.Entry(self.grid_frame)
        self.set_num_label = tk.Label(self.grid_frame, text="Set Number: ")
        self.set_num_entry = tk.Entry(self.grid_frame)
        self.reps_label = tk.Label(self.grid_frame, text="Number of Reps: ")
        self.reps_entry = tk.Entry(self.grid_frame)
        self.notes_label = tk.Label(self.grid_frame, text="Notes: ")
        self.notes_entry = tk.Entry(self.grid_frame)

        # Create button to execute insert into database, and a button to return to main window.
        self.enter_set_button = tk.Button(self.grid_frame, text="Enter Set", command=self.add_set)
        self.back_button = tk.Button(self.grid_frame, text="Back", command=self.go_back)

        # Place all created widgets
        self.workout_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.workout_option_menu.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.lifter_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.lifter_option_menu.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.exercise_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.exercise_option_menu.grid(row=2, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.set_num_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.set_num_entry.grid(row=3, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.weight_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.weight_entry.grid(row=4, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.reps_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.reps_entry.grid(row=5, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.notes_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.notes_entry.grid(row=6, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.enter_set_button.grid(row=7, column=0, pady=10)
        self.back_button.grid(row=7, column=1, pady=10)

        # Set the columns and rows weight to resize with the window.
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.rowconfigure(0, weight=1)
        self.grid_frame.rowconfigure(1, weight=1)
        self.grid_frame.rowconfigure(2, weight=1)
        self.grid_frame.rowconfigure(3, weight=1)
        self.grid_frame.rowconfigure(4, weight=1)
        self.grid_frame.rowconfigure(5, weight=1)
        self.grid_frame.rowconfigure(6, weight=1)
        self.grid_frame.rowconfigure(7, weight=1)

    # Query the database for all exercises and returns a list of tuples with the ids and names of each exercise
    def get_exercises(self):
        # Get the list of exercises from the database
        exercises = database_functions.get_exercises(self.my_cursor)
        exercise_names = [(exercise[0], exercise[1]) for exercise in
                          exercises]  # Extract the exercise names from the tuples
        return exercise_names

    # Query the database for all lifters and returns a list if tuples with the ids and names of each lifter
    def get_lifters(self):
        # Get the list of exercises from the database
        lifters = database_functions.get_lifters(self.my_cursor)
        # Extract the lifter id and names from the tuples
        lifter_names = [(lifter[0], lifter[1]) for lifter in lifters]
        return lifter_names

    # Query the database and returns a list of all workouts that have been entered in the database.
    def get_workouts(self):
        # Get the list of exercises from the database
        workouts = database_functions.get_workouts(self.my_cursor)
        return workouts

    # Checks if all fields and drops downs have a value using the validate_inputs() method, then attempts to use
    # those values to insert a new exercise log entry into the database.
    def add_set(self):
        if self.validate_inputs():
            selected_workout = self.workout_options.get()
            workout_id = get_id(selected_workout)

            selected_lifter = self.lifter_options.get()
            lifter_id = get_id(selected_lifter)

            selected_exercise = self.exercise_options.get()
            exercise_id = get_id(selected_exercise)

            set_number = self.set_num_entry.get()
            weight = self.weight_entry.get()
            reps = self.reps_entry.get()
            notes = self.notes_entry.get()

            if database_functions.add_exercise(self.my_cursor, workout_id, exercise_id, lifter_id, weight,
                                               reps, set_number, notes):
                self.set_num_entry.delete(0, "end")  # Clear date entry
                self.reps_entry.delete(0, "end")  # Clear note entry
                self.updated = True

    # Validates that all dropdowns and fields have entered values.
    def validate_inputs(self):
        """
        Validates that all necessary inputs have been selected or entered by the user.
        Returns True if all inputs are valid, False otherwise.
        """
        # Check that all necessary MenuOptions have a value selected
        if not self.exercise_options.get() or not self.lifter_options.get() or not self.workout_options.get():
            messagebox.showerror("Error", "Please select an option for all dropdown menus.")
            return False

        # Check that all necessary entries have been filled out
        if not self.set_num_entry.get() or not self.weight_entry.get() or not self.reps_entry.get():
            messagebox.showerror("Error", "Please fill out all fields.")
            return False

        return True

    # If exercises have been added to the database, prompts the user to commit, and commits when yes is selected. Then
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

import tkinter as tk

import database_functions


class AddExercise(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        # val = (workout_id, exercise_id, lifter_id, weight, reps, set_number, notes)
        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()

        self.title("Add Exercise Log")
        self.geometry("400x400")

        self.exercise_label = tk.Label(text="Exercises")
        self.exercise_options = tk.StringVar(self)
        self.exercise_options.set("")
        self.exercise_option_menu = tk.OptionMenu(self, self.exercise_options, *self.get_exercises())
        self.exercise_option_menu.pack()

        self.lifter_label = tk.Label(text="Lifters")
        self.lifter_options = tk.StringVar(self)
        self.lifter_options.set("")
        self.lifter_option_menu = tk.OptionMenu(self, self.lifter_options, *self.get_lifters())
        self.lifter_option_menu.pack()

        self.workout_label = tk.Label(text="Workouts")
        self.workout_options = tk.StringVar(self)
        self.workout_options.set("")
        self.workout_option_menu = tk.OptionMenu(self, self.workout_options, *self.get_workouts())
        self.workout_option_menu.pack()

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack()

    def get_exercises(self):
        # Get the list of exercises from the database
        exercises = database_functions.get_exercises(self.my_cursor)
        exercise_names = [exercise[1] for exercise in exercises]  # Extract the exercise names from the tuples
        return exercise_names

    def get_lifters(self):
        # Get the list of exercises from the database
        lifters = database_functions.get_lifters(self.my_cursor)
        # Extract the lifter id and names from the tuples
        lifter_names = [(lifter[0], lifter[1]) for lifter in lifters]
        return lifter_names

    def get_workouts(self):
        # Get the list of exercises from the database
        workouts = database_functions.get_workouts(self.my_cursor)
        # Extract the lifter id and names from the tuples
        # lifter_names = [(lifter[0], lifter[1]) for lifter in lifters]
        return workouts

    def go_back(self):
        self.destroy()
        self.master.deiconify()
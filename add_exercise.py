import tkinter as tk

import database_functions


class AddExercise(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        # val = (workout_id, exercise_id, lifter_id, weight, reps, set_number, notes)

        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()

        self.title("Add Exercise Log")
        self.geometry("300x300")
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        self.exercise_label = tk.Label(self.grid_frame, text="Exercises")
        self.exercise_options = tk.StringVar(self.grid_frame)
        self.exercise_options.set("")
        self.exercise_option_menu = tk.OptionMenu(self.grid_frame, self.exercise_options, *self.get_exercises())

        self.lifter_label = tk.Label(self.grid_frame, text="Lifters")
        self.lifter_options = tk.StringVar(self.grid_frame)
        self.lifter_options.set("")
        self.lifter_option_menu = tk.OptionMenu(self.grid_frame, self.lifter_options, *self.get_lifters())

        self.workout_label = tk.Label(self.grid_frame, text="Workouts")
        self.workout_options = tk.StringVar(self.grid_frame)
        self.workout_options.set("")
        self.workout_option_menu = tk.OptionMenu(self.grid_frame, self.workout_options, *self.get_workouts())

        self.back_button = tk.Button(self.grid_frame, text="Back", command=self.go_back)

        self.exercise_label.grid(row=0, column=0, sticky=tk.W)
        self.exercise_option_menu.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.lifter_label.grid(row=1, column=0, sticky=tk.W)
        self.lifter_option_menu.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.workout_label.grid(row=2, column=0, sticky=tk.W)
        self.workout_option_menu.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.back_button.grid(row=3, column=0, columnspan=2)

        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.rowconfigure(0, weight=1)
        self.grid_frame.rowconfigure(1, weight=1)
        self.grid_frame.rowconfigure(2, weight=1)
        self.grid_frame.rowconfigure(3, weight=1)
        # self.exercise_label = tk.Label(self, text="Exercises")
        # self.exercise_options = tk.StringVar(self)
        # self.exercise_options.set("")
        # self.exercise_option_menu = tk.OptionMenu(self, self.exercise_options, *self.get_exercises())
        #
        # self.lifter_label = tk.Label(self, text="Lifters")
        # self.lifter_options = tk.StringVar(self)
        # self.lifter_options.set("")
        # self.lifter_option_menu = tk.OptionMenu(self, self.lifter_options, *self.get_lifters())
        #
        # self.workout_label = tk.Label(self, text="Workouts")
        # self.workout_options = tk.StringVar(self)
        # self.workout_options.set("")
        # self.workout_option_menu = tk.OptionMenu(self, self.workout_options, *self.get_workouts())
        #
        # self.back_button = tk.Button(self, text="Back", command=self.go_back)
        #
        # self.workout_label.grid(row=0, column=0,sticky=tk.W)
        # self.workout_option_menu.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E)
        # self.lifter_label.grid(row=1, column=0, sticky=tk.W)
        # self.lifter_option_menu.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E)
        # self.exercise_label.grid(row=2, column=0, sticky=tk.W)
        # self.exercise_option_menu.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E)
        # self.back_button.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E)



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
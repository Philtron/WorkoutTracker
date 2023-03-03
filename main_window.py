import sys
import tkinter as tk
import add_exercise_log
import add_workout
import database_functions


# Grabs selected item from listbox
def get_selected_item(listbox):
    selection = listbox.curselection()
    if selection:
        return selection[0]
    else:
        return None


class MainWindow(tk.Tk):
    def __init__(self, db_connection):
        super().__init__()

        # Initialize instance variables
        self.mydb = db_connection

        # Set title and dimensions
        self.title("Workout App")
        self.geometry("250x600")

        # Create menu frame to hold buttons
        menu_frame = tk.Frame(self)
        menu_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create buttons for each menu item. Add images to each button Tkinter is ugly without makeup
        self.add_workout_image = tk.PhotoImage(file='Images/add_workout.PNG')
        self.add_workout_button = tk.Button(menu_frame, image=self.add_workout_image, text="Enter New Workout",
                                            fg='white',
                                            font=("TkDefaultFont", 18), compound='center', command=self.add_workout)
        self.add_workout_button.pack(fill="both", expand=True)

        self.add_exercise_image = tk.PhotoImage(file='Images/add_exercise.PNG')
        self.add_exercise_button = tk.Button(menu_frame, image=self.add_exercise_image, text="Enter Exercise Log",
                                             font=("TkDefaultFont", 18), fg='white', compound='center',
                                             command=self.add_exercise)
        self.add_exercise_button.pack(fill="both", expand=True)

        self.list_lifters_image = tk.PhotoImage(file='Images/list_lifters.PNG')
        self.list_lifters_button = tk.Button(menu_frame, image=self.list_lifters_image, text="List Lifters", fg='white',
                                             font=("TkDefaultFont", 18), compound='center', command=self.list_lifters)
        self.list_lifters_button.pack(fill="both", expand=True)

        self.list_exercises_image = tk.PhotoImage(file='Images/list_exercises.PNG')
        self.list_exercises_button = tk.Button(menu_frame, image=self.list_exercises_image, text="List Exercises",
                                               fg='white',
                                               font=("TkDefaultFont", 18), compound='center',
                                               command=self.list_exercises)
        self.list_exercises_button.pack(fill="both", expand=True)

        self.list_workouts_image = tk.PhotoImage(file="Images/list_workouts.PNG")
        self.list_workouts_button = tk.Button(menu_frame, image=self.list_workouts_image, text="List Workouts",
                                              fg='white',
                                              font=("TkDefaultFont", 18), compound='center', command=self.list_workouts)
        self.list_workouts_button.pack(fill="both", expand=True)

        self.commit_image = tk.PhotoImage(file='Images/commit.PNG')
        self.commit_button = tk.Button(menu_frame, image=self.commit_image, text="Commit Changes", fg='white',
                                       font=("TKDefaultFont", 18), compound='center',
                                       command=lambda: database_functions.commit_changes(self.mydb))
        self.commit_button.pack(fill='both', expand=True)
        self.exit_image = tk.PhotoImage(file='Images/exit.PNG')
        self.exit_button = tk.Button(menu_frame, image=self.exit_image, text="Exit", fg='white',
                                     font=("TkDefaultFont", 18),
                                     compound='center', command=lambda: sys.exit(0))
        self.exit_button.pack(fill="both", expand=True)

        self.pretty_workout_button = tk.Button(self, text="Pretty Workouts", command=lambda: self.pretty_workouts())
        self.pretty_workout_button.pack(fill="both", expand=True)

    # Hide self and create and display add_workout window
    def add_workout(self):
        self.withdraw()
        add_workout_window = add_workout.AddWorkout(self.mydb, master=self)
        add_workout_window.mainloop()

    # Hide self and create and display add_exercise window
    def add_exercise(self):
        self.withdraw()
        add_exercise_window = add_exercise_log.AddExercise(self.mydb, master=self)
        add_exercise_window.mainloop()

    # Called by list lifters button. Queries the database and displays results in a listbox in a pop out window
    def list_lifters(self):
        my_cursor = self.mydb.cursor()
        lifters = database_functions.get_lifters(my_cursor)

        lifter_window = tk.Toplevel(self)
        lifter_window.title("Lifters")
        lifter_window.geometry("200x200")

        lifter_listbox = tk.Listbox(lifter_window)
        lifter_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        for lifter in lifters:
            lifter_listbox.insert("end", f"{lifter[1]}, (ID: {lifter[0]})")

    # Called by list exercises button. Queries the database and displays results in a listbox in a pop out window
    def list_exercises(self):
        my_cursor = self.mydb.cursor()
        exercises = database_functions.get_exercises(my_cursor)

        exercises_window = tk.Toplevel(self)
        exercises_window.title("Exercise List")
        exercises_window.geometry("400x400")

        exercise_listbox = tk.Listbox(exercises_window)
        exercise_listbox.pack(padx=10, pady=10, fill='both', expand=True)

        for exercise in exercises:
            exercise_listbox.insert("end", f"{exercise[1]}, (ID: {exercise[0]})")

    # Called by list workouts button. Queries the database and displays results in a listbox in a pop out window using
    # the add_to_exercise_listbox() method.
    def list_workouts(self):
        my_cursor = self.mydb.cursor()
        workouts = database_functions.get_workouts(my_cursor)

        workouts_window = tk.Toplevel(self)
        workouts_window.title("Workouts")
        workouts_window.geometry("1000x500")

        listbox_frame = tk.Frame(workouts_window)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

        workouts_listbox = tk.Listbox(workouts_window)
        workouts_listbox.pack(padx=10, pady=10, fill='both', expand=True)

        for workout in workouts:
            workouts_listbox.insert("end", f"{workout[0]} | Date: {workout[1]} Notes: {workout[2]}")

        sel_button = tk.Button(workouts_window, text="Get Selected Item",
                               command=lambda: self.add_to_exercise_listbox(workouts_listbox, exercise_listbox))
        sel_button.pack()

        exercise_listbox = tk.Listbox(workouts_window)
        exercise_listbox.pack(padx=10, pady=10, fill='both', expand=True)

    # Function to populate exercise listbox. Clears the listbox before grabbing the selected item using the
    # get_selected_item() function
    def add_to_exercise_listbox(self, workouts_listbox, exercise_listbox):
        exercise_listbox.delete(0, tk.END)
        index = get_selected_item(workouts_listbox)
        if index is not None:
            value = workouts_listbox.get(index)
            workout_id = int(value.split()[0])
            logs = database_functions.get_exercise_from_workout_id(self.mydb.cursor(), workout_id)
            for log in logs:

                insert_string = string = "EXERCISE ID: {:<10} WORKOUT ID: {:<10} EXERCISE: {:<30} LIFTER: {:<20} " \
                                         "WEIGHT: {:<10} REPS: {:<10} SET #: {:<10} NOTES: {}"
                formatted_string = insert_string.format(log[0], log[1], log[2], log[3], log[4], log[5], log[6], log[7])
                exercise_listbox.insert("end", formatted_string)

    def pretty_workouts(self):
        my_cursor = self.mydb.cursor()
        workouts = database_functions.get_workouts(my_cursor)

        pretty_workouts_window = tk.Toplevel(self)
        pretty_workouts_window.title("Pretty Workouts")
        pretty_workouts_window.geometry("500x500")

        workout_listbox = tk.Listbox(pretty_workouts_window)
        workout_listbox.pack(padx=10, pady=10, fill='both', expand=True)
        for workout in workouts:
            workout_listbox.insert("end", f"{workout[0]} | Date: {workout[1]} Notes: {workout[2]}")


        # id_label = tk.Label(pretty_workouts_window, text="ID")
        # id_entry = tk.Entry(pretty_workouts_window)
        pretty_listbox = tk.Listbox(pretty_workouts_window)
        get_id_button = tk.Button(pretty_workouts_window, text="Get Workout",
                                  command=lambda: self.get_pretty(workout_listbox, pretty_listbox))
        # id_label.pack()
        # id_entry.pack()
        get_id_button.pack()

        pretty_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def get_pretty(self, workout_listbox, list_box):
        index = get_selected_item(workout_listbox)
        value = workout_listbox.get(index)
        workout_id = int(value.split()[0])

        my_cursor = self.mydb.cursor()
        # Retrieve the exercise logs for the selected workout
        exercise_logs = database_functions.pretty_workout(my_cursor, workout_id)
        # Group the exercise logs by lifter name and exercise name
        lifter_groups = {}
        for log in exercise_logs:
            lifter_name = log[0]
            exercise_name = log[1]
            weight = log[2]
            reps = log[3]
            sets = log[4]

            if lifter_name not in lifter_groups:
                lifter_groups[lifter_name] = {}

            if exercise_name not in lifter_groups[lifter_name]:
                lifter_groups[lifter_name][exercise_name] = []

            lifter_groups[lifter_name][exercise_name].append((weight, reps, sets))

        # Build the output string
        output_string = ""
        for lifter_name, exercise_groups in lifter_groups.items():
            output_string += lifter_name + "\n"
            for exercise_name, exercise_logs in exercise_groups.items():
                output_string += exercise_name + ", "
                for exercise_log in exercise_logs:
                    weight = exercise_log[0]
                    reps = exercise_log[1]
                    sets = exercise_log[2]
                    output_string += f"{weight}, set {sets} rep {reps}, "
                output_string = output_string[:-2] + "\n"
        print(output_string)
        list_box.delete(0, tk.END)
        rows = output_string.split("\n")
        for row in rows:
            list_box.insert("end", row)

import tkinter as tk
from tkinter import messagebox
import database_functions


class MainWindow(tk.Tk):
    def __init__(self, db_connection):
        super().__init__()

        self.mydb = db_connection

        self.title("Workout App")
        self.geometry("250x400")

        menu_frame = tk.Frame(self)
        menu_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create buttons for each menu option
        self.add_workout_image = tk.PhotoImage(file='add_workout.PNG')
        add_workout_button = tk.Button(menu_frame, image=self.add_workout_image, text="Enter New Workout", fg='white',
                                       font=("TkDefaultFont", 18),compound='center', command=self.add_workout)
        add_workout_button.pack(fill="both", expand=True)

        self.add_exercise_image = tk.PhotoImage(file='add_exercise.PNG')
        add_exercise_button = tk.Button(menu_frame, image=self.add_exercise_image,  text="Enter New Exercise",
                                        font=("TkDefaultFont", 18), fg='white', compound='center',
                                        command=self.add_exercise)
        add_exercise_button.pack(fill="both", expand=True)

        self.list_lifters_image = tk.PhotoImage(file='list_lifters.PNG')
        list_lifters_button = tk.Button(menu_frame, image=self.list_lifters_image,  text="List Lifters", fg='white',
                                        font=("TkDefaultFont", 18), compound='center', command=self.list_lifters)
        list_lifters_button.pack(fill="both", expand=True)

        self.list_exercises_image = tk.PhotoImage(file='list_exercises.PNG')
        list_exercises_button = tk.Button(menu_frame,image=self.list_exercises_image, text="List Exercises", fg='white',
                                          font=("TkDefaultFont", 18), compound='center', command=self.list_exercises)
        list_exercises_button.pack(fill="both", expand=True)

        self.list_workouts_image = tk.PhotoImage(file="list_workouts.PNG")
        list_workouts_button = tk.Button(menu_frame, image=self.list_workouts_image,  text="List Workouts", fg='white',
                                         font=("TkDefaultFont", 18), compound='center', command=self.list_workouts)
        list_workouts_button.pack(fill="both", expand=True)

        self.exit_image = tk.PhotoImage(file='exit.PNG')
        exit_button = tk.Button(menu_frame, image=self.exit_image,  text="Exit", fg='white', font=("TkDefaultFont", 18),
                                compound='center', command=self.quit)
        exit_button.pack(fill="both", expand=True)

        # self.my_image = tk.PhotoImage(file='button.png')
        # image_button = tk.Button(menu_frame, image=self.my_image, text="Test", fg='white', font=("TkDefaultFont", 18),
        #                          command=self.clicked, compound='center', padx=10, pady=10)
        # image_button.pack(fill='both', expand=True)


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
        lifter_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        for lifter in lifters:
            lifter_listbox.insert("end", f"{lifter[1]}, (ID: {lifter[0]})")

    def list_exercises(self):
        # messagebox.showinfo("List Exercises")
        my_cursor = self.mydb.cursor()
        exercises = database_functions.get_exercises(my_cursor)

        exercises_window = tk.Toplevel(self)
        exercises_window.title("Exercise List")
        exercises_window.geometry("400x400")

        exercise_listbox = tk.Listbox(exercises_window)
        exercise_listbox.pack(padx=10, pady=10, fill='both', expand=True)

        for exercise in exercises:
            exercise_listbox.insert("end", f"{exercise[1]}, (ID: {exercise[0]})")



    def list_workouts(self):
        messagebox.showinfo("List Workouts")

        database_functions.get_workouts(self.mydb.cursor())

# app = MainWindow()
# app.mainloop()

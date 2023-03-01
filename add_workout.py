import tkinter as tk
import database_functions
import main_window


class AddWorkout(tk.Toplevel):
    def __init__(self, db_connection, master=None):
        super().__init__(master)

        self.mydb = db_connection
        self.my_cursor = self.mydb.cursor()

        self.title("Add Workout")
        self.geometry("400x400")
        frame1 = tk.Frame(self)
        frame1.pack()
        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.date_label = tk.Label(frame1, text="Date:")
        self.date_entry = tk.Entry(frame1)

        self.note_label = tk.Label(frame1, text="Notes:")
        self.note_entry = tk.Entry(frame1)

        self.add_button = tk.Button(frame1, text="Add Workout",
                                    command=lambda: self.add_workout())
        self.back_button = tk.Button(frame1, text="Back", command=self.go_back)

        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.note_label.grid(row=1, column=0, padx=5, pady=5)
        self.note_entry.grid(row=1, column=1, padx=5, pady=5)
        self.add_button.grid(row=2, column=0, padx=5, pady=5)
        self.back_button.grid(row=2, column=1, padx=5, pady=5)

        self.workout_listbox = tk.Listbox(frame2)
        self.workout_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_workout_listbox()

    def update_workout_listbox(self):
        self.workout_listbox.delete(0, "end")  # Clear the current items in the listbox
        workouts = database_functions.get_workouts(self.my_cursor)  # Get latest workouts from database
        for workout in workouts:
            self.workout_listbox.insert("end", f"{workout[0]} | Date: {workout[1]} Notes: {workout[2]}")

    def add_workout(self):
        database_functions.add_workout(self.my_cursor, self.date_entry.get(), self.note_entry.get())
        self.update_workout_listbox()  # Call method to update the listbox after a new workout is added
        self.date_entry.delete(0, "end")  # Clear date entry
        self.note_entry.delete(0, "end")  # Clear note entry

    def go_back(self):
        self.destroy()
        self.master.deiconify()
        # main_window_window = main_window.MainWindow(self.mydb)
        # main_window_window.mainloop()

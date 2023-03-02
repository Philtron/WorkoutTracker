import tkinter as tk
from tkinter import messagebox
from database_functions import connect_to_database
from main_window import MainWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Log In")
        self.geometry("275x150")

        # Create Title label
        self.title_label = tk.Label(self, text="Log In", font=("TkDefaultFont", 21))
        self.title_label.grid(row=0, column=0, sticky="N", padx=10, pady=10)

        # Create grid frame to hold input fields
        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=1, column=0, padx=25)

        # Create username label and entry field
        self.user_name_label = tk.Label(self.grid_frame, text='User Name')
        self.user_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.user_name_entry = tk.Entry(self.grid_frame)
        self.user_name_entry.grid(row=0, column=1, sticky="E")

        # Create password label and entry field
        self.password_label = tk.Label(self.grid_frame, text='Password')
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.grid_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        # Create login button
        self.login_button = tk.Button(self.grid_frame, text="Log In", command=self.login)
        self.login_button.grid(row=2, column=0, pady=10)

    # Login function that verifies user credentials and opens main window
    def login(self):
        # Get username and password from entry fields
        username = self.user_name_entry.get()
        password = self.password_entry.get()

        # Attempt to connect to database
        db_connection = connect_to_database(username, password)

        # If connection is successful, destroy login window and open main window
        if db_connection is not None:
            self.destroy()
            MainWindow(db_connection)
        # If connection is unsuccessful, show error message
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

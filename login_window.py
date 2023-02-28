import tkinter as tk
from tkinter import messagebox
from database_functions import connect_to_database
from main_window import MainWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Log In")
        self.geometry("275x150")

        # Create a label with larger text and center it horizontally
        self.title_label = tk.Label(self, text="Log In", font=("TkDefaultFont", 21))
        self.title_label.grid(row=0, column=0, sticky="N", padx=10, pady=10)

        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=1, column=0, padx=25)

        self.user_name_label = tk.Label(self.grid_frame, text='User Name')
        self.user_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.user_name_entry = tk.Entry(self.grid_frame)
        self.user_name_entry.grid(row=0, column=1, sticky="E")

        self.password_label = tk.Label(self.grid_frame, text='Password')
        self.password_label.grid(row=1, column=0)

        self.password_entry = tk.Entry(self.grid_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.grid_frame, text="Log In", command=self.login)
        self.login_button.grid(row=2, column=0, pady=10)

        # Set the grid frame to expand in both directions
        self.grid_frame.grid_rowconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(0, weight=1)

    def login(self):
        # Get the text from the username and password fields
        username = self.user_name_entry.get()
        password = self.password_entry.get()

        # Call the connect_to_database function from the database_functions module
        db_connection = connect_to_database(username, password)

        # Display a message box indicating whether the login was successful or not
        if db_connection is not None:
            # messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.destroy()
            MainWindow(db_connection)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


login_window = LoginWindow()
login_window.mainloop()

from tkinter import messagebox

import mysql.connector


# Function to connect to the database, takes no arguments
# Prompts the user for their database credentials and connects to the workout database
def connect_to_database(username, password):
    try:
        # Attempt to connect with credentials
        my_db = mysql.connector.connect(user=username, password=password, host='localhost', database='workout')
        print("Connected to database successfully!")
        # Return connection object
        return my_db
    except (mysql.connector.Error, mysql.connector.errors.InterfaceError) as error:
        # If connection fails, print error message and return None
        print(f"Failed to connect to database: {error}")
        messagebox.showerror("Error:", f"{error}")


# Get all exercises from the exercises table, takes a cursor as an argument
# Executes an SQL query to select all rows from the exercises table and prints them to the console
def get_exercises(my_cursor):
    my_cursor.execute("SELECT * FROM exercises")
    return my_cursor.fetchall()


# Get all lifters from the lifters table, takes a cursor as an argument
# Executes an SQL query to select all rows from the lifters table and prints them to the console
def get_lifters(my_cursor):
    my_cursor.execute("SELECT * FROM lifters")
    return my_cursor.fetchall()


# Get all workouts from the workouts table, takes a cursor as an argument
# Executes an SQL query to select all rows from the workouts table and prints them to the console
# Also prompts the user to select a workout by ID and calls the get_exercise_from_workout_id function
def get_workouts(my_cursor):
    my_cursor.execute("SELECT * FROM workouts")
    return my_cursor.fetchall()


def get_weight_history(my_cursor, selected_lifter):
    my_cursor.execute(f"SELECT * FROM bodyweight_log WHERE lifter_id = {selected_lifter}")

    return my_cursor.fetchall()


def pretty_workout(my_cursor, workout_id):
    my_cursor.execute(f"SELECT l.name AS lifter_name, e.name AS exercise_name,el.weight, el.reps, el.sets "
                      f"FROM exercise_log AS el JOIN exercises AS e ON el.exercise_id = e.exercise_id "
                      f"JOIN lifters AS l ON el.lifter_id = l.lifter_id WHERE el.workout_id = {workout_id}"
                      f" ORDER BY el.elog_id ASC;")
    return my_cursor.fetchall()


# Get all exercise logs attached to a specific workout, takes a cursor and a workout ID as arguments
# Executes an SQL query to select all exercise logs from the exercise_log table that match the given workout ID
# Prints the exercise logs to the console then returns the logs
def get_exercise_from_workout_id(my_cursor, workout_id):
    my_cursor.execute(f"SELECT exercise_log.elog_id, exercise_log.workout_id, exercises.name, lifters.name, "
                      f"exercise_log.weight, exercise_log.reps, exercise_log.sets, exercise_log.notes FROM "
                      f"exercise_log INNER JOIN exercises ON exercise_log.exercise_id = exercises.exercise_id INNER "
                      f"JOIN lifters ON exercise_log.lifter_id = lifters.lifter_id WHERE workout_id = {workout_id} "
                      f"ORDER BY elog_id ASC")
    logs = my_cursor.fetchall()

    return logs


# Add a new workout to the workouts table, takes a cursor as an argument
# Prompts the user for a date and notes, then inserts the new workout into the workouts table
# Returns True if the workout was successfully added, False otherwise
def add_workout(my_cursor, date, notes):
    workout_updated = False

    try:
        sql = "INSERT INTO workouts(date, notes) VALUES(%s, %s)"
        val = (date, notes)
        query = sql % val
        print(f"Running: {query}")
        my_cursor.execute(sql, val)
        workout_updated = True
    except (mysql.connector.Error, mysql.connector.errors.InterfaceError) as error:
        print(f"Error adding workout to database: {error}")
        messagebox.showerror("Error:", f"Error adding to database: {error}")

    return workout_updated


# Add a new exercise log to the exercise_log table, takes a cursor and a workout ID as arguments
# Prompts the user for a lifter ID, exercise ID, weight, reps, and sets, then inserts the new exercise log
# into the exercise_log table
# Returns True if the exercise log was successfully added, False otherwise
def add_exercise(my_cursor, workout_id, exercise_id, lifter_id, weight, reps, set_number, notes):
    try:
        sql = "INSERT INTO exercise_log(workout_id, exercise_id, lifter_id, weight, reps, sets, notes) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s) "
        val = (workout_id, exercise_id, lifter_id, weight, reps, set_number, notes)
        query = sql % val
        print(f"Running: {query}")
        my_cursor.execute(sql, val)
        exercise_updated = True
    except mysql.connector.Error as error:
        exercise_updated = False
        print(f"Error: {error}")
        messagebox.showerror("Error:", f"{error}")

    return exercise_updated


def insert_weight(my_cursor, lifter_id, weight, date, notes):
    try:
        print(f"INSERT INTO bodyweight_log(lifter_id, weight, date, notes) "
              f"VALUES({lifter_id}, {weight}, {date}, {notes})")

        my_cursor.execute(f"INSERT INTO bodyweight_log(lifter_id, weight, date, notes) "
                          f"VALUES({lifter_id}, {weight}, '{date}', '{notes}')")

    except (mysql.connector.Error, mysql.connector.errors.InterfaceError) as error:
        print(f"Error adding workout to database: {error}")
        messagebox.showerror("Error:", f"Error adding to database: {error}")


# Attempts to commit any changes made this session to the database. Notifies the user with a messagebox of the success
def commit_changes(connection):
    try:
        connection.commit()
        messagebox.showinfo("Confirmation", "Changes have been committed.")
    except (mysql.connector.Error, mysql.connector.errors.InterfaceError) as error:
        messagebox.showerror("Error:", f"{error}")



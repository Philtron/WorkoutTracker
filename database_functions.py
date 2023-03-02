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


# Get all exercise logs attached to a specific workout, takes a cursor and a workout ID as arguments
# Executes an SQL query to select all exercise logs from the exercise_log table that match the given workout ID
# Prints the exercise logs to the console then returns the logs
def get_exercise_from_workout_id(my_cursor, workout_id):
    my_cursor.execute(f"SELECT exercise_log.elog_id, exercise_log.workout_id, exercises.name, lifters.name, "
                      f"exercise_log.weight, exercise_log.reps, exercise_log.sets, exercise_log.notes FROM "
                      f"exercise_log INNER JOIN exercises ON exercise_log.exercise_id = exercises.exercise_id INNER "
                      f"JOIN lifters ON exercise_log.lifter_id = lifters.lifter_id WHERE workout_id = {workout_id}")
    logs = my_cursor.fetchall()

    # If any logs were found, print them with a header
    if len(logs) > 0:
        header = "Exercise Log ID | Workout ID | Exercise | Lifter | Weight | Reps | Sets | Notes"
        print(f"Exercise logs for workout {workout_id}:")
        print(header)
        for log in logs:
            print(log)
    else:
        print(f"No exercise logs found for workout {workout_id}")
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


# Attempts to commit any changes made this session to the database. Notifies the user with a messagebox of the success
def commit_changes(connection):
    try:
        connection.commit()
        messagebox.showinfo("Confirmation", "Changes have been commited.")
    except (mysql.connector.Error, mysql.connector.errors.InterfaceError  )as error:
        messagebox.showerror("Error:", f"{error}")


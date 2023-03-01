import mysql.connector


# Function to connect to the database, takes no arguments
# Prompts the user for their database credentials and connects to the workout database
def connect_to_database(username, password):
    # Prompt user for database username and password.
    # username = input("Enter your username: ")
    # password = input("Enter your password: ")
    try:
        # Attempt to connect with credentials
        my_db = mysql.connector.connect(user=username, password=password, host='localhost', database='workout')
        print("Connected to database successfully!")
        # Return connection object
        return my_db
    except mysql.connector.Error as err:
        # If connection fails, print error message and return None
        print(f"Failed to connect to database: {err}")


# Get all exercises from the exercises table, takes a cursor as an argument
# Executes an SQL query to select all rows from the exercises table and prints them to the console
def get_exercises(my_cursor):
    my_cursor.execute("SELECT * FROM exercises")
    return my_cursor.fetchall()
    # exercises = my_cursor.fetchall()
    #
    # print("Exercises List:")
    # for i, exercise in enumerate(exercises):
    #     print(f"Exercise ID:{exercise[0]}: {exercise[1]} ", end="")
    #     if (i + 1) % 4 == 0:
    #         print()
    # print()


# Get all lifters from the lifters table, takes a cursor as an argument
# Executes an SQL query to select all rows from the lifters table and prints them to the console
def get_lifters(my_cursor):
    my_cursor.execute("SELECT * FROM lifters")
    return my_cursor.fetchall()
    # lifters = my_cursor.fetchall()
    # print("Lifters List")
    # for lifter in lifters:
    #     print(f"Name: {lifter[1]} Lifter ID: {lifter[0]}")
    # print()


# Get all workouts from the workouts table, takes a cursor as an argument
# Executes an SQL query to select all rows from the workouts table and prints them to the console
# Also prompts the user to select a workout by ID and calls the get_exercise_from_workout_id function
def get_workouts(my_cursor):
    my_cursor.execute("SELECT * FROM workouts")
    workouts = my_cursor.fetchall()
    print("Workouts list")
    for workout in workouts:
        print(workout)
    print()
    workout_selection = input("Enter a workout id to view attached exercise logs or enter 0 to continue: ")
    while workout_selection != '0':
        get_exercise_from_workout_id(my_cursor, workout_selection)
        workout_selection = input("Enter a workout id to view attached exercise logs or enter 0 to continue: ")


# Get all exercise logs attached to a specific workout, takes a cursor and a workout ID as arguments
# Executes an SQL query to select all exercise logs from the exercise_log table that match the given workout ID
# Prints the exercise logs to the console
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


# Add a new workout to the workouts table, takes a cursor as an argument
# Prompts the user for a date and notes, then inserts the new workout into the workouts table
# Returns True if the workout was successfully added, False otherwise
def add_workout(my_cursor):
    try:

        date = input("Enter date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        sql = "INSERT INTO workouts(date, notes) VALUES(%s, %s)"
        val = (date, notes)
        query = sql % val
        print(f"Running: {query}")
        my_cursor.execute(sql, val)
        workout_updated = True
        return workout_updated
    except mysql.connector.Error as e:
        workout_updated = False
        print(f"Error adding working to database: {e}")
        return -1, workout_updated


# Add a new exercise log to the exercise_log table, takes a cursor and a workout ID as arguments
# Prompts the user for a lifter ID, exercise ID, weight, reps, and sets, then inserts the new exercise log
# into the exercise_log table
# Returns True if the exercise log was successfully added, False otherwise
def add_exercise(my_cursor, workout_id):
    keep_going = True
    while keep_going:
        # Prompt user to select a lifter and an exercise
        get_lifters()
        lifter_id = input("Enter Lifter ID:")
        get_exercises(my_cursor)
        exercise_id = input("Enter exercise ID: ")
        num_sets = input("How many sets?")
        keep_going = False
        # For each set, prompt the user for weight, reps, and notes and insert the new exercise log into the
        # exercise_log table
        for i in range(int(num_sets)):
            set_number = i + 1
            print(f"Set Number: {set_number}")
            weight = input("Enter weight: ")
            reps = input("Enter reps: ")
            notes = input("Enter notes: ")

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
        # Prompt the user to add another exercise to the current workout
        add_another = input("Add another exercise to this workout? y/n: ").lower()
        if add_another == 'y':
            keep_going = True

    return exercise_updated

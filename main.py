import mysql.connector


def connect_to_database():
    # Prompt user for their username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Connect to the database using the user's credentials
    try:
        my_db = mysql.connector.connect(user=username, password=password, host='localhost', database='workout')
        print("Connected to database successfully!")
        return my_db
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")


def get_exercises(my_cursor):
    # Select all exercises from database
    my_cursor.execute("SELECT * FROM exercises")
    exercises = my_cursor.fetchall()
    # Print list of exercises
    print("Exercise List:")
    for i, exercise in enumerate(exercises):
        print(f"Exercise ID:{exercise[0]}: {exercise[1]} ", end="")
        if (i + 1) % 4 == 0:
            print()
    print()


def get_lifters(my_cursor):
    my_cursor.execute("SELECT * FROM lifters")
    lifters = my_cursor.fetchall()
    print("Lifter List")
    for lifter in lifters:
        print(f"Name: {lifter[1]} Lifter ID: {lifter[0]}")
    print()


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


def get_exercise_from_workout_id(my_cursor, workout_id):
    my_cursor.execute(f"SELECT exercise_log.elog_id, exercise_log.workout_id, exercises.name, lifters.name, "
                      f"exercise_log.weight, exercise_log.reps, exercise_log.sets, exercise_log.notes FROM "
                      f"exercise_log INNER JOIN exercises ON exercise_log.exercise_id = exercises.exercise_id INNER "
                      f"JOIN lifters ON exercise_log.lifter_id = lifters.lifter_id WHERE workout_id = {workout_id}")
    logs = my_cursor.fetchall()
    header = "Exercise Log ID | Workout ID| Exercise | Lifter | Weight | Reps | Sets | Notes"
    if len(logs) > 0:
        print(f"Exercise logs for workout {workout_id}:")
        print(header)
        for log in logs:
            print(log)
    else:
        print(f"No exercise logs found for workout {workout_id}")


def add_workout(my_cursor):
    try:
        # Prompt user for workout information
        date = input("Enter date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")

        # Insert new workout into database
        sql = "INSERT INTO workout(date, notes) VALUES(%s, %s)"
        val = (date, notes)
        query = sql % val
        print(f"Running: {query}")
        my_cursor.execute(sql, val)
        # workout_id = my_cursor.lastrowid
        workout_updated = True
        # return workout_id, workout_updated
        return workout_updated
    except mysql.connector.Error as e:
        workout_updated = False
        print(f"Error adding working to database: {e}")
        return -1, workout_updated


def add_exercise(my_cursor, workout_id):
    # Prompt user for exercise information
    num_sets = input("How many sets?")
    lifter_id = input("Enter Lifter ID:")
    for i in range(int(num_sets)):

        set_number = i + 1
        print(f"Set Number: {set_number}")
        if i == 0:
            get_exercises(my_cursor)
            which_id = input(f"Use current workout id {workout_id}, or enter new one? enter 'c' for current or 'n' for "
                             f"new one").lower()
            if which_id == 'c':
                pass
            elif which_id == 'n':
                workout_id = input("Enter workout_id")
        exercise_id = input("Enter exercise ID: ")
        weight = input("Enter weight: ")
        reps = input("Enter reps: ")
        notes = input("Enter notes: ")

        try:
            # Insert exercise log into database
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

    return exercise_updated


if __name__ == '__main__':

    mydb = connect_to_database()
    my_cursor = mydb.cursor()
    get_lifters(my_cursor)
    # workout_id = add_workout(my_cursor)
    # print(f"Workout ID: {workout_id}")
    message = '''What would you like to do?
    1. Enter new workout.
    2. Enter new exercise.
    3. List lifters
    4. List exercises.
    5. List workouts.
    6. Exit.
    Enter your selection: '''
    user_input = int(input(message))
    print(user_input)
    workout_id = ''
    workout_updated = False
    exercise_updated = False

    while user_input != 6:
        if user_input == 1:
            # Prompt user for workout information
            # workout_id, workout_updated = add_workout(my_cursor)
            workout_updated = add_workout(my_cursor)
        elif user_input == 2:
            get_workouts(my_cursor)

            workout_id = input("Enter the workout ID you want to attach this exercise log entry to: ")
            exercise_updated = add_exercise(my_cursor, workout_id)
            # if workout_id:
            #     # Prompt user for exercise information
            #     exercise_updated = add_exercise(my_cursor, workout_id)
            # else:
            #     print('Need to add a workout first..')
            #     workout_id, workout_updated = add_workout(my_cursor)
            #     exercise_updated = add_exercise(my_cursor, workout_id)
        elif user_input == 3:
            get_lifters(my_cursor)
        elif user_input == 4:
            get_exercises(my_cursor)
        elif user_input == 5:
            get_workouts(my_cursor)
        user_input = int(input(message))

    mydb.commit()
    updates = ''
    if workout_updated:
        updates += 'Workout updated'
    if exercise_updated:
        updates += '\nExercise log updated'
    print(updates)

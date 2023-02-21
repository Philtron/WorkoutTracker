from database_functions import connect_to_database, get_exercises, get_lifters, get_workouts, add_workout, add_exercise


# Display options to user and return their selection
def display_menu():
    message = '''What would you like to do?
    1. Enter new workout.
    2. Enter new exercise.
    3. List lifters.
    4. List exercises.
    5. List workouts.
    6. Exit.
    Enter your selection: '''
    user_input = int(input(message))
    return user_input


if __name__ == '__main__':
    # Connect to the database and get a cursor object
    mydb = connect_to_database()
    my_cursor = mydb.cursor()

    # Get user input and set variables to initial values
    user_input = display_menu()
    workout_id = ''
    workout_updated = False
    exercise_updated = False

    # continue to get user input until they enter 6 to exit.
    while user_input != 6:
        # call the appropriate function based on user input
        if user_input == 1:
            workout_updated = add_workout(my_cursor)
        elif user_input == 2:
            get_workouts(my_cursor)
            workout_id = input("Enter the workout ID you want to attach this exercise log entry to: ")
            exercise_updated = add_exercise(my_cursor, workout_id)
        elif user_input == 3:
            get_lifters(my_cursor)
        elif user_input == 4:
            get_exercises(my_cursor)
        elif user_input == 5:
            get_workouts(my_cursor)

        # get the next user input
        user_input = display_menu()

    # Commit any updates made to the database
    mydb.commit()

    # Print a message indicating what updates were made
    updates = ''
    if workout_updated:
        updates += 'Workout updated'
    if exercise_updated:
        updates += '\nExercise log updated'
    print(updates)

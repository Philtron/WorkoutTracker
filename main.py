from database_functions import connect_to_database, get_exercises, get_lifters, get_workouts, add_workout, add_exercise
# from database_functions import *


if __name__ == '__main__':

    mydb = connect_to_database()
    my_cursor = mydb.cursor()
    get_lifters(my_cursor)
    message = '''What would you like to do?
    1. Enter new workout.
    2. Enter new exercise.
    3. List lifters
    4. List exercises.
    5. List workouts.
    6. Exit.
    Enter your selection: '''
    user_input = int(input(message))
    # print(user_input)
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

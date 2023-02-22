DROP DATABASE workout;
CREATE DATABASE IF NOT EXISTS workout;
use workout;

CREATE TABLE exercises (
  exercise_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  primary_muscle_group VARCHAR(50) NOT NULL,
  secondary_muscle_group VARCHAR(50),
  push_or_pull ENUM('push', 'pull') NOT NULL,
  notes TEXT
);

CREATE TABLE lifters (
  lifter_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  weight DECIMAL(5,2) NOT NULL,
  birthday DATE NOT NULL,
  notes TEXT
);

CREATE TABLE workouts (
  workout_id INT PRIMARY KEY AUTO_INCREMENT,
  date DATE NOT NULL,
  notes TEXT
);

CREATE TABLE exercise_log (
  elog_id INT PRIMARY KEY AUTO_INCREMENT,
  workout_id INT NOT NULL,
  exercise_id INT NOT NULL,
  lifter_id INT NOT NULL,
  weight DECIMAL(5,2) NOT NULL,
  reps INT NOT NULL,
  sets INT NOT NULL,
  notes TEXT,
  FOREIGN KEY (workout_id) REFERENCES workouts(workout_id),
  FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id),
  FOREIGN KEY (lifter_id) REFERENCES lifters(lifter_id)
);


CREATE TABLE bodyweight_log (
  bodyweightlog_id INT PRIMARY KEY AUTO_INCREMENT,
  lifter_id INT NOT NULL,
  weight DECIMAL(5,2) NOT NULL,
  date DATE NOT NULL,
  notes TEXT,
  FOREIGN KEY (lifter_id) REFERENCES lifters(lifter_id)
);


CREATE TABLE measurement_log (
  measurementlog_id INT PRIMARY KEY AUTO_INCREMENT,
  lifter_id INT NOT NULL,
  upper_arm DECIMAL(5,2) NOT NULL,
  forearm DECIMAL(5,2) NOT NULL,
  quad DECIMAL(5,2) NOT NULL,
  calf DECIMAL(5,2) NOT NULL,
  neck DECIMAL(5,2) NOT NULL,
  chest DECIMAL(5,2) NOT NULL,
  stomach DECIMAL(5,2) NOT NULL,
  notes TEXT,
  date DATE NOT NULL,
  FOREIGN KEY (lifter_id) REFERENCES lifters(lifter_id)
);



-- CREATE TABLE workout_lifter (
--   workout_id INT NOT NULL,
--   lifter_id INT NOT NULL,
--   PRIMARY KEY (workout_id, lifter_id),
--   FOREIGN KEY (workout_id) REFERENCES workout(workout_id),
--   FOREIGN KEY (lifter_id) REFERENCES lifter(lifter_id)
-- );
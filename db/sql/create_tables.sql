CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, name text, email text UNIQUE, signup_date DATE);
CREATE TABLE IF NOT EXISTS user_experiments (experiment_id int PRIMARY KEY, user_id int, experiment_compounds_ids integer[], experiment_run_time int);
CREATE TABLE IF NOT EXISTS compounds (compound_id int PRIMARY KEY, compound_name text, compound_structure text);
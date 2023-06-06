# Implementation of Take Home Challenge

## Getting Started

### Setting Up

#### Prereqs:

- [Docker](https://www.docker.com/) installed
- `curl` or equivalent (e.g. Postman) available

#### Building the App

- Navigate to the root directory where `app.py` and `DOCKERFILE` are

`$ cd eikon_takehome/`

- Build the docker images

`$ docker compose build`

- Bring up the docker containers (in background)

`$ docker compose up -d`

#### Teardown

- Stopping containers

`$ docker compose down`

### Make API Calls

#### Trigger ETL

```
POST /api/v1/load

Request params: 
- None
```

`$ curl -XPOST http://127.0.0.1:5500/api/v1/load`

#### Total experiments a user ran

```
GET /api/v1/get_total_experiments

Request params: 
- user_id: int
- email: str
```

`$ curl -XPOST http://127.0.0.1:5500/api/v1/get_total_experiments?user_id=1`

#### Average experiments amount per user

```
GET /api/v1/get_total_experiments

Request params: 
- None
```

`$ curl -XGET http://127.0.0.1:5500/api/v1/get_average_experiment_per_user`

#### User's most commonly experimented compound.

```
GET /api/v1/get_most_commonly_used_compound

Request params: 
- user_id: int
- email: str
```

`$ curl -XGET http://127.0.0.1:5500/api/v1/get_most_commonly_used_compound?user_id=2`
 
### Run API Tests

From the root directory, run

`# docker exec -it eikon_app python3 -m unittest test.test_services`

## Design

- I used Docker Compose to build both the Flask app and database as containers. This makes it so that whoever runs this app doesn't need to install PostgreSQL on theit machine and configure it. In real world situation, the DB most likely on a server and not a container. This means the run command for this assignment is not `docker run`.
- I wrote some basic API tests for sanity checking. 


### Caveats / Tech Debt
- Credentials are hard-coded and exposed. The secrets and passwords can be stored using `.env` files. 
- I would also implement several configs for dev and production
- A lot of common methods could be abstracted out to a `common.py` file. But given the scope of the assignment, I left them where they are.
- Likewise, constants could also be abstracted to a `constants.py` file.
- For more official web service handling, could add Nginx to handle connections


# Backend Engineering Take-Home Challenge

### Introduction
In this challenge, you will be tasked with creating a simple ETL pipeline that can be triggered via an API call. You will be provided with a set of CSV files that you will need to process, derive some features from, and then upload into a database table.

### Requirements
- Python 3.7+
- Docker
- PostgreSQL

### Challenge
1.  Create a Dockerized application that can be started with a single `docker run` command.

2. The application should expose an API endpoint that triggers an ETL process.

3. The ETL process should:
- Load CSV files from the given data directory.
 - Process these files to derive some simple features.
 - Upload the processed data into a **postgres** table.

4.  The application should be built using Python and any tooling you like for coordinating the workflow and fronting the api server

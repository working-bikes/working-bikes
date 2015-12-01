# Working Bikes [![Build Status](https://travis-ci.org/working-bikes/working-bikes.svg?branch=master)](https://travis-ci.org/working-bikes/working-bikes)
Working Bikes volunteer tracking website

## Development

### Create the database (MySQL)
```sql
CREATE DATABASE the_database;
CREATE USER the_user IDENTIFIED BY 'the_password';
GRANT ALL PRIVILEGES ON the_database.* to 'the_user'@'%';
```

### Set up the environment
```shell
# Add to .bashrc or .zshrc or another file that gets sourced at login, for ease
export WORKING_BIKES_DATABASE_NAME=the_database
export WORKING_BIKES_DATABASE_USER=the_user
export WORKING_BIKES_DATABASE_PASSWORD=the_password
export WORKING_BIKES_SECRET_KEY=foobarbaz
export WORKING_BIKES_DEBUG=TRUE
```

### Clone this repository
```shell
$ git clone https://github.com/working-bikes/working-bikes.git
```
### Install its dependencies (in a Python virtual environment)
```shell
$ cd working-bikes
$ mkvirtualenv working-bikes
(working-bikes)$ pip install -r requirements.txt
```

### Run the server
```shell
(working-bikes)$ ./manage.py runserver
```

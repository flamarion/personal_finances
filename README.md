Access the root of repository and run the following commands to initialize the database and run the application.

* pip install -r requirements
* export FLASK_APP=pfv2
* export FLASK_DEBUG=1
* flask db init
* flask db migrate -m "Initial migration."
* flask db upgrade
* flask run

I'm going to improve this in the future with instructions for database migrations and whatever more necessary.
# GraphSite
Web Interface for GraphProfile project 

Setup instructions:

Make sure you have python 3 and pip installed (https://www.python.org)

Clone the repo, and open a command line interface in the repo. 

Install the necessary packages by running `pip install -r requirements.txt`

On Linux and Mac OSes, install redis via https://redis.io/download
On Windows based systems, the windows based port is already in this repo (redis-server.exe)

The .env file specifies the environment variables needed. In order to run the server properly, you will need the SECRET_KEY
from me or someone on the team.
Once you have the key, replace the line

`SECRET_KEY=GET_THIS_FROM_BOSHEN`

to

`SECRET_KEY=(the actual secret key)`

The default database is sqlite. If you want to use another database (e.g. postgreSQL), you can add a DATABASE_URL setting to the env file, e.g:

`DATABASE_URL=postgres://username:password@ec-instance.compute-1.amazonaws.com:5432/database-name`

You can also specify another redis server by changing the `REDIS_URL` attribute, e.g:

`REDIS_URL=redis://username:password@ec-instance.compute-1.amazonaws.com:port`

The executable that is used to profile the graphs is located in /media/executables. Update GraphProfile.exe if you want to test out new executables, etc.
Also note that there is GraphProfile-Windows.exe and GraphProfile-Linux.exe, for running on both OSes.
You will have to rename the appropriate one to GraphProfile.exe based on the OS you are using in order for the executable to be runnable
by the server.

Migrate the database with

`python manage.py migrate`

Then, start the server with

`./redis-server.exe & python manage.py runserver & wait`  on Windows or

`redis-server & python manage.py runserver & wait` on Linux/Mac OS

In a seperate command line, start the celery worker with
`celery -A GraphSite worker -l info`
At the moment, the celery worker may be prone to crashing and may need to be restarted, which makes it more convenient to have it running
on a seperate shell than with the redis & django servers

Go to localhost:8000, and GraphSite should be up and running.



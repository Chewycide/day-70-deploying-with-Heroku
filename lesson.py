# Version Control using Git and Github:
# is like a save point where you can rollback to a previous version of
# your code. You can rollback as further as you like.

# NOTE: In Macs Git is already pre-installed

# ------------------------------------ #

#           GIT COMMANDS               #

# ------------------------------------ #

# git init = initialize a repository

# git status = check tracked and untracked files (files in staging area)

# git add <filename> = add a file to the staging area

# git commit -m = commit files that are staged. NOTE: commit message is
# very important as it helps you keep track of what changes have been
# made in that commit. you have to be as explicit as possible about what
# changes were made between the last save point and the current save point.
# NOTE: best practice for git commit messages is having it written in 
# present tense.

# git log - view commits that have been made. the hash uniquely identifies
# the commit

# git diff <optional:filename> = compare the current state of the file vs 
# the previous commit state of the file.

# git checkout <optional:filename> - rollback to the previous state

# git remote add origin <URL> = add a remote repository at the URL specified
# NOTE: origin is the name of the remote, you use other names but origin
# is the convention

# git push -u origin master = push local to remote repository using the -u flag
# -u links local to remote, origin is the name of remote and master is the name
# of the main branch.


# ------------------------------------ #

#             MORE THEORY

# ------------------------------------ #

# The Working Directory - is the folder where the git repository is initialized
# The Staging Area - is where the files are reviewed before getting committed
# The Local Repository - is where the files staged go after commiting
# The Remote Repository - is a repository saved in another computer e.g. GitHub
# The Master Branch - is the main branch of commits, is sequential and is where
# your main progress is committed


# WSGI stands for Web Server Gateway Interface and it's described here: 
# https://www.python.org/dev/peps/pep-3333/

# It standardises the language and protocols between our Python Flask application 
# and the host server.

# Again, but in English: Normal web servers can't run Python applications, so a 
# special type of server was created (WSGI) to run python applications.

# There are many WSGIs to choose from, but we'll use the most popular - gunicorn.

# So Heroku will call gunicorn to run our code and gunicorn will know how to speak 
# to Heroku.

# Next, we need to tell Heroku about our gunicorn server and how to run our Flask 
# app, we do that using a Procfile.
# Create a new file in the project top-level folder called Procfile

# NOTE: make sure you spell the name of the file exactly as you see above, with a 
# capital P and no file extension.

# Type the following into the Procfile:
# web: gunicorn main:app

# This will tell Heroku to create a web worker, one that is able to receive HTTP 
# requests.

# To use gunicorn to serve your web app
# And the Flask app object is the main.py file.
# NOTE: If your app is not inside a file called main.py then you should change
# main to your file name.


# Upgrade SQLite to PostgreSQL
# When we were coding and testing our Flask website, it was nice to use a simple 
# database like SQLite. But SQLite is a file-based database. This is its strength 
# and weakness. It's a strength because while we're coding up our database and 
# debugging, it's really useful to be able to open the SQLite file using DB 
# Viewer and see how our data looks.

# But it's also a weakness because once it's deployed with Heroku the file 
# locations are shifted around every 24 hours or so. This means that your database 
# might just get wiped every day. That will mean some very unhappy users.
# READ MORE: https://devcenter.heroku.com/articles/sqlite3

# So we've got to put on our big-boy/big-girl pants and upgrade our simple 
# SQLite database to PosgreSQL, a database that can handle millions of data 
# entries and reliably delivers data to users.

# Luckily, because we used SQLAlchemy to create our Flask app, there's nothing 
# we need to change in terms of code. We just need to set up the PostgreSQL 
# database and tell Heroku about it.

# SQLite is pre-installed for all Python projects, but if we are going to use 
# Postgres, we'll need to install the psycopg2-binary packages as well. 
# https://pypi.org/project/psycopg2-binary/
# NOTE: you'll also need to add the package name and version to requirements.txt 
# as well as commit and push the updates.


# Important, make sure that you don't include any pipfile or pipfile.lock files 
# in your GitHub repo (you can delete them and commit the changes). Heroku needs
# to know which packages they should install on their side

# Because our main.py SQLAlchemy database is now pointing to an environment 
# variable that is only avilable on Heroku, if you run the app right now locally, 
# you will get some errors.

# Instead, we want to provide SQLite as the alternative when we're developing 
# the app locally.

# Update the app config to use "DATABASE_URL" environment variable if provided, 
# but if it's None (e.g. when running locally) then we can provide 
# sqlite:///blog.db as the alternative.

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///blog.db")


# Finally, if you go to your heroku app, it should now be up and using a Postgres database.
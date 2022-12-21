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
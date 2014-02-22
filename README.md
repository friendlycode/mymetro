MyMetro
==============

A hyperlocal civic notification app. Forget when your trash gets picked up? Have it remind you. Want to know where your polling place is? Forget your precinct and ward? It can remind you of that too.

[Project board](https://waffle.io/FriendlyCode/mymetro)

[![Build Status](https://secure.travis-ci.org/friendlycode/mymetro.png)](http://travis-ci.org/friendlycode/mymetro)

## Prerequisites

- Basic [Python](http://python.org/) knowledge.
- Installed Python and [Virtualenv](http://pypi.python.org/pypi/virtualenv). See [this guide](http://install.python-guide.org/) for guidance.
- A Heroku user account. [Signup is free and instant](https://api.heroku.com/signup/devcenter).
- A Local [PostgreSQL](http://www.postgresql.org/) instance. See [this guide](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup) for guidance.

## Local workstation setup

Install the [Heroku Toolbelt](https://toolbelt.heroku.com/) on your local workstation. This ensures that you have access to the [Heroku command-line client](https://devcenter.heroku.com/categories/command-line), Foreman, and the Git revision control system.

Once installed, you can use the `heroku` command from your command shell. Log in using the email address and password you used when creating your Heroku account:

    $ heroku login
    Enter your Heroku credentials.
    Email: chase@example.com
    Password:
    Could not find an existing public key.
    Would you like to generate one? [Yn]
    Generating new SSH public key.
    Uploading ssh public key /Users/chase/.ssh/id_rsa.pub

Press enter at the prompt to upload your existing `ssh` key or create a new one, used for pushing code later on.

## Getting the app running

Make sure you `cd` to your favorite directory. Then we'll clone the app repo:

    $ git clone git@github.com:friendlycode/mymetro.git

Move into the project:

    $ cd mymetro

Then create a Python virtual environment:

    $ virtualenv venv --distribute

To use our new virtualenv, we need to activate it.
(You must source the virtualenv environment for each terminal session where you wish to run your app.)

    $ source venv/bin/activate

Next, install our application’s local dependencies (that you’ll need to run your site locally) with [pip](http://pypi.python.org/pypi/pip):

    $ pip install -r reqs/dev.txt --use-mirrors

NOTE: If the pip command above fails, it means you’re missing some C libraries that are required for some of the Python libraries to work. The ones you need (on Ubuntu) are:

- libevent-dev
- libpq-dev
- libmemcached-dev
- zlib1g-dev
- libssl-dev
- python-dev
- build-essential

We also recommend you install `postgresql-client`, even though it isn’t required.

### Local .env File

A sample configuration of environment variables can be found in `sample.env`.
Create the real `.env` file based on the sample:

    $ cp sample.env .env

Now replace the examples inside `.env` with your actual values.

Environment Variables:

    DATABASE_URL=engine://username:password@host:port/mymetro
    AWS_ACCESS_KEY_ID=accesskey
    AWS_SECRET_ACCESS_KEY=secretkey
    AWS_STORAGE_BUCKET_NAME=bucket
    DJANGO_SETTINGS_MODULE=mymetro.settings.dev
    SECRET_KEY=xxx
    EMAIL_HOST=host
    EMAIL_HOST_USER=user
    EMAIL_HOST_PASSWORD=password
    EMAIL_PORT=port
    EMAIL_USE_TLS=true

####`DATABASE_URL`

Set this to use your local database engine, name, port, username, and password.

####`AWS_ACCESS_KEY_ID`

(not used in development) Set to Amazon S3 Access Key

####`AWS_SECRET_ACCESS_KEY`

(not used in development) Set to Amazon S3 Secret Key

####`AWS_STORAGE_BUCKET_NAME`

(not used in development) Set to Amazon Storage Bucket used for this app.

####`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS`

MyMetro uses [SendGrid](http://www.sendgrid.com/) for system emails. Ask a senior team member for this info. Or set it to your own email server info for local development.


### Start the app

You can now start the processes in your [Procfile](https://devcenter.heroku.com/articles/procfile)
locally using [Foreman](http://blog.daviddollar.org/2011/05/06/introducing-foreman.html)
(installed as part of the Toolbelt):

    foreman start

[Visit](http://0.0.0.0:5000/) your app in the browser, and you should see Django print out an error
because we still need to set up our database to work with our app. This is covered in the next section.


## Database Setup & Migrations w/South

### Overview

[South](http://south.readthedocs.org/en/latest/) is used to handle the migrations of our Django models and database.

First, make sure you have a PostgreSQL database running as set in the `.env` file.

Create a PostgreSQL database:

    $ psql> CREATE DATABASE mymetro;

Create a PostgreSQL user:

    $ psql> CREATE USER username WITH PASSWORD 'password';

Grant privileges to user for the mymetro database:

    $ psql> GRANT ALL PRIVILEGES ON DATABASE mymetro to username;

You must now sync the database to add our apps' models, including South, to the schema:

    $ foreman run python manage.py syncdb

NOTE: Skip creating a Django super user right now. You can do so [later](#creating-a-superuser).

Once [`syncdb`](https://docs.djangoproject.com/en/1.5/ref/django-admin/#syncdb) is complete,
the `south_migrationhistory` table along with other tables from our apps are created in the database.

If you are working with an empty database, run the `migrate` command:

    $ foreman run python manage.py migrate

If you are working with a database that has existing data, but you have not run South yet,
you must use `--fake` instead:

    $ foreman run python manage.py migrate mymetro --fake

### Creating a superuser

After syncdb and migrate, you can now create a superuser.
Run the following command to create a superuser:

    $ foreman run python manage.py createsuperuser

The command will prompt you for username, email, password.

### Creating and Updating models
When you update a model or create a new model, you must run `schemamigration`.

    $ foreman run python manage.py schemamigration mymetro --auto
    $ foreman run python manage.py migrate mymetro

### Team Workflow
Migration files generated by South must be synced with the git repository. As a team member:

- Make sure to commit your changes to the migrations folder.
- Make sure you run the migrate command after pulling the repo if you see changes to the migrations.

If you run migrate, and there are conflicts with the migration history, you may see a message:

    Inconsistent migration history
    The following options are available:
    --merge: will just attempt the migration ignoring any potential dependency conflicts.

To resolve these conflicts with South, rerun `migrate` with `--merge`:

    $ foreman run python manage.py migrate --merge mymetro

This will normally work if you were working on separate models. If not, you need to create a new empty migration.

    $ foreman run python manage.py schemamigration --empty mymetro merge_models

In any case, make sure you are collaborating with other team members and try not to be working on the same model at the same time during a sprint.

See the [South Docs](http://south.readthedocs.org/en/latest/tutorial/part5.html#team-workflow) for more information about South migration with teams.


## Deploying Test Branch Using Heroku Forks
To deploy your topic branch for others in the team to review, you can fork the mymetro app using heroku and deploying an instance. [Learn More](https://devcenter.heroku.com/articles/fork-app)

**Create a fork:**
```
heroku fork -a mymetro <your-app-name>
```

**Change the environment variables:**

View your heroku config:

    heroku config --app <your-app-name>

Change app environment

    heroku config:set ENV_VAR=new_value --app <your-app-name>

Add remote:
```
git remote add forked git@heroku.com:<your-app-name>.git
```

Push your branch to your fork:
```
git push forked <your-branch-name>:master
```

Heroku will build your app, and the output will contain the url of your branch, which is <your-app-name>.herokuapp.com.


## Running Tests (needs development)

We would like to implement automated testing for our app using coverage and Django's test suite as well as Django REST Framework's helper classes.

The following is not usable until this is developed:

### Django test suite

To run django tests for the mymetro app, you can use foreman:
```
foreman run python manage.py test mymetro
```

To run coverage:
```
foreman run coverage run --omit "venv/*,mymetro/migrations/*" manage.py test mymetro
foreman run coverage report
```

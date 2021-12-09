# CSDS 234: Structured and Unstructured Data:
This final course project was completed by Escanord Le, and Kris Zhao. It is meant to be a search tool centered around CWRU CSDS courses listed on the general bulletin.

## Running the project:

### Local serving:

In order to run the project, it can be run using python with the following steps:

```
pip install requirements.txt
```

Then, you can launch the local server with:

```
python manage.py runserver
```

Then, navigate to `127.0.0.1:8000` if it is not taken, and you should see the home page for the application.

### Remote access:

Alternatively, this site will be published to Heroku, and can be accessed at:

```
https://csds234-final-project.herokuapp.com/
```

## Project structure directory overview:

### _database:

This includes the csv files that were used to load into psql (after cleaning) as well as the SQL to create the tables themselves.

### _docs_regex

This folder includes some sample and reference regex / formulas for data manipulation and cleaning.

### course

This folder includes the bulk of the work for the project. This includes the html, css, python files, ORM specifications, and view generators.

### mysite

The main importance inside the mysite folder is the `urls.py` file which tackles all of the routing to each template.
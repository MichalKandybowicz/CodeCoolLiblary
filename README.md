# CodeColl Library

This web application creates an online catalog for a small local library, where users can browse available books and manage their accounts.

The main features that have currently been implemented are:

* There are models for books, book copies, genre, language and authors.
* Users can view list and detail information for books.
* Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).


## Quick Start

To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
1. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
1. Create a few test objects of each type.
1. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.

### TODO

All task to do in next version
- Register with google acc *
- make list with book (by genre)
- back books system
- Add reset password (email)
- Book history (% loan time )
- Alert to user if he dont back book in time (mail?)

```
Link with tutorial (google acc connect)
https://medium.com/trabe/oauth-authentication-in-django-with-social-auth-c67a002479c1
``` 
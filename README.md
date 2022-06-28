# Online Classroom

Hosted on Heroku: https://capstoneclassroom.herokuapp.com/  
To watch a video showcasing the features of this website, click [here](https://youtu.be/ZoIO-Ewe1AM)

## Features
* 2 types of accounts - Faculty and Student
* Faculties can create and join courses, Students can join courses ( using a 6-digit code )
* Faculties can create assignments and set a due date
* Users can create posts for a particular subject
* Comments on posts
* Faculties can schedule attendance for a particular day
* Users can create notes and mark them as important
* Mobile responsive

## NOTE
An email is send to all students when an assignment is created. So please create an environment variable `EMAIL_USER` for email and `EMAIL_PASS` for email password.
Also please change the variables given in capstone/manage.py based on the email service you use  
Add an environment variable for SECRET_KEY and DROPBOX_OAUTH2_TOKEN

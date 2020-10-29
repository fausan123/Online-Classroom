# Capstone - Online Classroom

This project provides an interface for faculties to conduct their courses online.A user can sign up as either a Faculty or Student. A faculty can create subjects/courses or join courses as faculty using a 6-digit code. A student can join courses. Faculties can create posts, assignment with due date(can be blank),
take attendance for a particular day. Student can also create posts. All signed in users can create notes and mark them as important. They can also delete the notes. Students and faculties can also comment on posts.

## Files

This is created as a django project of name **capstone**. It has an app called **classroom**. The app has:
* views.py : Contains all the views of the classroom app
* urls.py : Contains mapping of all urls and apis of app classroom
* models.py : Contains all the models related to app classroom (8 models in total)
* forms.py : Contains all the forms

### Static Files
* styles.css: Contains all CSS property of the website (Web also uses Bootstrap)
* script.js: Contains JavaScript related to mobile responsiveness and also related to course creation and joining
* subject.js: For each subject page. Contains JavaScript related to visibility of comments, faculties and students, and entering comments.
* note.js: For the note page. Contains JavaScript for marking notes important and also deleting notes.

### Template Files
* layout.html: Contains the general layout of the website
* index.html: Contains the main page ie. the page that lists all the subject enrolled or joined.
* subject.html: View page for each subject
* assignview.html: View page for each assignment
* createassign.html: View page which contains the form for creating an assignment
* note.html: View page for creating notes and displaying them
* todo.html: View page which contains all the assignments that is yet to be done (for Students)
* register.html: Register page
* login.html: Login page

## NOTE
An email is send to all students when an assignment is created. So please create an environment variable `EMAIL_USER` for email and `EMAIL_PASS` for email password. If gmail, go to security and enable security for less secure apps. Also change "EMAIL_HOST", "EMAIL_PORT", "EMAIL_USE_TLS" and "EMAIL_USE_SSL" in settings.py if your account is not gmail. For more info check the setting.py file in capstone folder.

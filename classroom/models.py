from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    account_type = models.CharField(
        max_length=20, choices=[('Student', 'Student'), ('Faculty', 'Faculty')])

    def __str__(self):
        return f'{self.username}'


class Subject(models.Model):
    name = models.CharField(max_length=20)
    info = models.TextField(blank=True)
    code = models.CharField(max_length=6)
    faculties = models.ManyToManyField(User, related_name="subjects")
    students = models.ManyToManyField(User, related_name="courses")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Subject: {self.name}'


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="posts",
                             on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey(
        Subject, related_name="posts", on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username
        }

    def __str__(self):
        return f'Post by {self.user} in {self.subject}'


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        User, related_name="created_assigns", on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, related_name="assignments", on_delete=models.CASCADE)
    submitted_students = models.ManyToManyField(
        User, related_name="submitted")

    def __str__(self):
        return f'Assignment: {self.name} in {self.subject}'


def submission_path(instance, filename):
    return f'{instance.assignment.subject.name}/{instance.assignment.name}/{instance.user}/{filename}'


class Submission(models.Model):
    date = models.DateTimeField(default=timezone.now)
    files = models.FileField(upload_to=submission_path)
    user = models.ForeignKey(
        User, related_name="submissions", on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment, related_name="submissions", on_delete=models.CASCADE)

    def __str__(self):
        return f'Submitted {self.assignment} by {self.user}'


class Attendance(models.Model):
    date = models.DateTimeField(default=timezone.now)
    closing_time = models.DateTimeField()
    subject = models.ForeignKey(
        Subject, related_name="attendances", on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name="attendance")

    def __str__(self):
        return f'Attendence of {self.subject} on {self.date}'


class Note(models.Model):
    title = models.CharField(max_length=15)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    starred = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="notes",
                             on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
            "starred": self.starred
        }

    def __str__(self):
        return f'Note: {self.title} by {self.user}'


class PostComment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, related_name="postcomments", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

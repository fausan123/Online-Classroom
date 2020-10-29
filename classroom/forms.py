from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username',
                  'email', 'password1', 'password2', 'account_type']


class SubjectCreationForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'info']


class PostCreationForm(forms.Form):
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={'rows': 3}))


class AssignmentCreationForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'content', 'due_date']


class SubmissionForm(forms.Form):
    files = forms.FileField(
        label="", widget=forms.ClearableFileInput(attrs={'multiple': True}))


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['closing_time']

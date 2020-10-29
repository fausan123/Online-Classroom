import secrets
import json
import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.mail import send_mail
from .models import *
from .forms import *


@login_required
def index(request):
    if request.user.is_authenticated:
        if request.user.account_type == 'Faculty':
            subjects = Subject.objects.filter(
                faculties=request.user).order_by('-date_created')
        else:
            subjects = Subject.objects.filter(
                students=request.user).order_by('-date_created')
        if request.method == 'POST':
            name = request.POST.get('name')
            info = request.POST.get('info')
            course_code = request.POST.get('code')
            if name is not None and (request.user.account_type == 'Faculty'):
                code = secrets.token_hex(3)
                sub = Subject(name=name, info=info, code=code)
                sub.save()
                sub.faculties.add(request.user)
                return redirect('index')
            if course_code is not None:
                subs = Subject.objects.all()
                for sub in subs:
                    if course_code == sub.code:
                        sub.students.add(request.user)
                        sub.save()
                        return render(request, "classroom/index.html", {
                            'subjects': subjects,
                            'message': {'tag': 'success', 'body': 'Joined course!!'}
                        })
                return render(request, "classroom/index.html", {
                    'subjects': subjects,
                    'message': {'tag': 'danger', 'body': 'Invalid code, please try again.'}
                })
        return render(request, "classroom/index.html", {
            'subjects': subjects
        })
    else:
        return render(request, "classroom/index.html")


@login_required
def subject_view(request, sub_id):
    subject = Subject.objects.get(id=sub_id)
    assignments = Assignment.objects.filter(subject=subject).order_by('-date')
    posts = Post.objects.filter(subject=subject).order_by('-date')

    post_paginator = Paginator(posts, 5)
    post_pagenum = request.GET.get('page1')
    post_pageobj = post_paginator.get_page(post_pagenum)
    if post_paginator.num_pages > 1:
        post_ispage = True
    else:
        post_ispage = False

    assign_paginator = Paginator(assignments, 5)
    assign_pagenum = request.GET.get('page2')
    assign_pageobj = assign_paginator.get_page(assign_pagenum)
    if assign_paginator.num_pages > 1:
        assign_ispage = True
    else:
        assign_ispage = False

    delta30 = datetime.timedelta(0, 0, 0, 0, 30, 0, 0)
    time = timezone.now() + delta30
    time = time.strftime("%m/%d/%Y %H:%M:00")

    atts = Attendance.objects.filter(subject=subject).order_by('-date')

    attendances = []
    if len(atts) > 0:
        for attnd in atts:
            if (attnd.closing_time > timezone.now()):
                attendances.append(attnd)

    context = {
        'subject': subject,
        'p_form': PostCreationForm(),
        'att_form': AttendanceForm({'closing_time': time}),
        'attendances': attendances,
        'post_pageobj': post_pageobj,
        'post_ispage': post_ispage,
        'assign_pageobj': assign_pageobj,
        'assign_ispage': assign_ispage
    }

    if request.method == 'POST':
        pform = PostCreationForm(request.POST)
        attform = AttendanceForm(request.POST)
        if pform.is_valid():
            content = pform.cleaned_data["content"]
            post = Post(content=content, user=request.user, subject=subject)
            post.save()
            return render(request, "classroom/subject.html", context=context)
        elif attform.is_valid():
            closing_time = attform.cleaned_data['closing_time']
            att = Attendance(closing_time=closing_time, subject=subject)
            att.save()
            return render(request, "classroom/subject.html", context=context)
        elif request.POST.get('present'):
            attid = request.POST['attid']
            att = Attendance.objects.get(id=attid)
            if request.POST['present']:
                att.students.add(request.user)
        else:
            return render(request, "classroom/subject.html", {
                'message': {'tag': 'danger', 'body': 'Something happened..Please try again'}
            })

    return render(request, "classroom/subject.html", context=context)


@login_required
def create_assign(request, sub_id):
    subject = Subject.objects.get(id=sub_id)
    if request.method == 'POST':
        form = AssignmentCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            if form.cleaned_data['due_date']:
                due_date = form.cleaned_data['due_date']
            else:
                due_date = None
            assign = Assignment(name=name, content=content,
                                due_date=due_date, subject=subject, user=request.user)
            assign.save()
            recipients = [student.email for student in subject.students.all()]
            sub = f'New Assignment in {subject.name}'
            message = f'{name} created on {assign.date}'
            html_message = f'<div><p> Created on {assign.date}</p><h4> {assign.name} </h4><p> {assign.user}</p><hr><p>{assign.content} </p><hr><p><strong> Due date: {assign.due_date}</strong></p></div>'
            from_mail = os.environ.get('EMAIL_USER')
            send_mail(
                subject=sub,
                message=message,
                from_email=from_mail,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False)
            return HttpResponseRedirect(reverse('subject', kwargs={'sub_id': subject.id}))
        else:
            return render(request, "classroom/createassign.html", {
                'form': AssignmentCreationForm(),
                'message': {'tag': 'danger', 'body': 'Error, please try again.'}
            })
    return render(request, "classroom/createassign.html", {
        'form': AssignmentCreationForm()
    })


@login_required
def assign_view(request, assign_id):
    assignment = Assignment.objects.get(id=assign_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data['files']
            submission = Submission(
                files=files, user=request.user, assignment=assignment)
            submission.save()
            assignment.submitted_students.add(request.user)
            assignment.save()
            return HttpResponseRedirect(reverse('assign', kwargs={'assign_id': assign_id}))
        else:
            return render(request, "classroom/assignview.html", {
                'assignment': assignment, 'form': SubmissionForm(),
                'message': {'tag': 'danger', 'body': 'Error, please try again.'}
            })
    return render(request, "classroom/assignview.html", {
        'assignment': assignment, 'form': SubmissionForm()
    })


@login_required
def noteview(request):
    notes = Note.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            note = Note(title=title, content=content, user=request.user)
            note.save()
    return render(request, "classroom/note.html", {
        'form': NoteForm(), 'notes': notes
    })


@login_required
def todo_view(request):
    if request.user.account_type == 'Student':
        subjects = Subject.objects.filter(
            students=request.user).order_by('-date_created')
        assignments = []
        for sub in subjects:
            for assign in sub.assignments.all():
                if request.user not in assign.submitted_students.all():
                    assignments.append(assign)

        assignments = sorted(assignments, key=lambda k: k.date, reverse=True)
        return render(request, "classroom/todo.html", {
            'assignments': assignments
        })


@csrf_exempt
@login_required
def get_posts(request, sub_id):
    subject = Subject.objects.get(id=sub_id)
    if request.method == 'GET':
        if ((request.user in subject.students.all()) or (request.user in subject.faculties.all())):
            posts = Post.objects.filter(subject=subject).order_by('-date')
            return JsonResponse([post.serialize() for post in posts], safe=False)
        else:
            return JsonResponse({'error': 'Action not authorized', 'status': 401}, status=401)
    else:
        return JsonResponse({'error': 'GET request required', 'status': 400}, status=400)


@csrf_exempt
@login_required
def comment_posts(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data["content"]
        comment = PostComment(content=content, user=request.user, post=post)
        comment.save()
        return JsonResponse({"message": "Commented successfully", "status": 201}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def get_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-date')
    if request.method == 'GET':
        return JsonResponse([note.serialize() for note in notes], safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


@csrf_exempt
@login_required
def delstar_notes(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('star') is not None:
            if data["star"]:
                note.starred = True
                note.save()
            else:
                note.starred = False
                note.save()
            return HttpResponse(status=204)
        if data.get('delete') is not None:
            note.delete()
    else:
        return JsonResponse({
            "error": "PUT request required.",
            "status": 400
        }, status=400)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            return render(request, "classroom/login.html", {
                'message': {'tag': 'success',
                            'body': f'Account for {firstname} {lastname} created!. Please login now.'}
            })
    else:
        form = UserRegistrationForm()
        return render(request, "classroom/register.html", {
            'form': form
        })


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "classroom/login.html")
    else:
        return render(request, "classroom/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

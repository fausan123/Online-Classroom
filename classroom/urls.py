from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name='logout'),
    path('subject/<int:sub_id>', views.subject_view, name="subject"),
    path('subject/<int:sub_id>/createassign',
         views.create_assign, name="createassign"),
    path('assignments/<int:assign_id>', views.assign_view, name="assign"),
    path('notes/', views.noteview, name="note"),
    path('todo/', views.todo_view, name="todo"),

    # Api requests
    path('subject/<int:sub_id>/posts', views.get_posts, name="posts"),
    path('posts/<int:post_id>', views.comment_posts, name="commentpost"),
    path('getnotes/', views.get_notes, name="getnotes"),
    path('notes/<int:note_id>', views.delstar_notes, name="starnotes"),

]

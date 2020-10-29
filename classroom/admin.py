from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Assignment)
admin.site.register(Submission)

from django.contrib import admin
from Courses import models

# Register your models here.
admin.site.register(models.Attendance)
admin.site.register(models.BatchDetails)
admin.site.register(models.Course)
admin.site.register(models.CourseEmployeeList)
admin.site.register(models.Feedback)
admin.site.register(models.Grading)
admin.site.register(models.Files)
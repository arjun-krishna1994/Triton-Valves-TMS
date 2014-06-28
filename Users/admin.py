from django.contrib import admin
from Users import models
from Users.models import EmployeeInfo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(models.CoursesAttended)
admin.site.register(models.CoursesToAttend)
admin.site.register(models.Department)
class UserProfileInline(admin.StackedInline):
    model = EmployeeInfo
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
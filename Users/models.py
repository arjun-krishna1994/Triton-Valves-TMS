from django.db import models
from django.contrib.auth.models import User
from Courses.models import BatchDetails
from Courses.models import Course
# Create your models here.
class Department(models.Model):
    deptID = models.CharField(max_length = 15,unique = True , verbose_name = 'Department ID')
    dept_name = models.CharField(max_length = 30, unique = True, verbose_name = 'Department Name')
    def __unicode__(self):
        return '%s ' % ( self.dept_name )
    
class EmployeeInfo(models.Model):
    userObj = models.OneToOneField(User)
    is_Manager = models.BooleanField(default = False ,verbose_name = 'Manager aka Supervisior aka Unit Incharge')
    is_Admin = models.BooleanField(default = False) 
    is_HOD = models.BooleanField(default = False)
    is_Staff = models.BooleanField(default = False)
    userId = models.CharField(max_length = 15)
    unit = models.CharField(max_length = 35)
    is_Internal = models.BooleanField(default = False)
    phone_Number = models.IntegerField()
    address = models.CharField(max_length = 200)
    working_Status = models.BooleanField(default = False)
    current_shift = models.CharField(max_length = 15)
    department = models.ForeignKey('Users.Department')
    designation = models.CharField(max_length = 25)
    grade = models.CharField(max_length = 20,default = 'NA')
    def __unicode__(self):
        return '%s %s' % (self.userObj.first_name, self.userObj.last_name)
    def authorised_to_handle(self, employee = None , batch = None , course = None):
        handler = self
        all_dept = Department.objects.get(dept_id = 'ALL')
        flag = False
        if handler.is_Admin:
            flag = True
        elif handler.is_HOD:
            if employee is not None:
                if employee.department == handler.department or employee.department.dept_id == 'ALL':
                    flag = True
            if batch is not None:
                if handler.department in batch.course.department.all() or all_dept in batch.course.department.all():
                    flag = True
            if course is not None:
                if  handler.department in course.department.all() or all_dept in course.department.all():
                    flag = True
                
        elif handler.is_Manager:
            if employee is not None:
                if employee.department == handler.department:
                    flag = True        
        
        return flag    
    
    
class CoursesAttended(models.Model):
    course = models.ForeignKey(Course)
    batch = models.ForeignKey(BatchDetails, null = True)
    employee = models.ForeignKey(EmployeeInfo)
    def __unicode__(self):
        return '%s  %s  %s' % (self.course.course_name , self.employee.userObj.first_name , self.employee.userObj.last_name)
    
class CoursesToAttend(models.Model):
    employee = models.ForeignKey(EmployeeInfo)
    course = models.ForeignKey(Course)
    batch = models.ForeignKey(BatchDetails, null = True)
    def __unicode__(self):
        return '%s  %s  %s' % (self.course.course_name , self.employee.userObj.first_name , self.employee.userObj.last_name)
    

 
class Notification(models.Model):
    employee = models.ForeignKey(EmployeeInfo)
    message = models.CharField(max_length = 500)
    dateTime = models.DateTimeField(null = True)
    seen = models.BooleanField(default = False)
  
    
    
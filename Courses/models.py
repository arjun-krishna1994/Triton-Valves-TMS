from django.db import models
from Courses  import variables
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
#model everything with courses not batches

class Course(models.Model):
    course_name = models.CharField(max_length = 30, unique = True)
    course_id = models.CharField(unique = True,max_length = 30)
    duration = models.CharField(max_length = 10)
    objective = models.CharField(max_length = 400)
    misc_Details = models.CharField(max_length = 600)
    department = models.ManyToManyField('Users.Department', blank = True, null = True)
    productivity = models.TextField( null = True)
    quality_improvement = models.TextField( null = True)
    reduction_time = models.TextField( verbose_name = 'Improvement in m/c uptime', null = True)
    reduction_wastage = models.TextField( verbose_name = 'Improvement in m/c uptime', null = True)
    technical = models.TextField( blank = True , null = True)
    final = models.TextField( blank = True , null = True)
    behavioral = models.TextField( blank = True , null = True)
    others = models.TextField(blank = True , null = True)
    
    def __unicode__(self):
        return '%s  ' % (self.course_name )

class BatchDetails(models.Model):
    start_date = models.DateField(blank = True, null = True)
    actual_start_date = models.DateField(blank = True, null = True)
    stop_date = models.DateField(blank = True, null = True)
    finish_date = models.DateField(blank = True, null = True)
    actual_stop_date = models.DateField(blank = True, null = True)
    start_time  = models.TimeField(blank = True, null = True)
    stop_time = models.TimeField(blank = True, null = True)
    course = models.ForeignKey(Course)
    venue = models.CharField(max_length = 50,blank = True)
    course_completed = models.BooleanField(default = False)
    course_ongoing = models.BooleanField(default = False)
    course_finished = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True,null = True)
    files = models.ManyToManyField('Courses.Files', null = True)
    def __unicode__(self):
        stri = '%s  %s  %s' % (self.course.course_name , str(self.start_date) , str(self.stop_date))
        return stri
    
class Attendance(models.Model):
    course = models.ForeignKey(Course)
    batch = models.ForeignKey(BatchDetails,null = True)
    employee = models.ForeignKey('Users.EmployeeInfo')
    shift = models.CharField(max_length = 15)
    date = models.DateField()
    
class CourseEmployeeList(models.Model):
    
    course = models.ForeignKey(Course) 
    batch = models.ForeignKey(BatchDetails, blank = True , null = True)
    employee = models.ForeignKey('Users.EmployeeInfo')

class CoursewiseTrainer(models.Model):
    course = models.ForeignKey(Course)    
    employee = models.ForeignKey('Users.EmployeeInfo')
    def __unicode__(self):
        return unicode(str(self.id) )
    
class BatchwiseTrainer(models.Model):   
    batch = models.ForeignKey(BatchDetails)
    employee = models.ForeignKey('Users.EmployeeInfo')
    def __unicode__(self):
        return unicode(str(self.id) )
    

    
class Grading(models.Model):
    batch = models.ForeignKey(BatchDetails)
    employee = models.ForeignKey('Users.EmployeeInfo')
    pre_training = models.DecimalField(max_digits = 3 , decimal_places = 2 ,blank = True, default = 0)
    post_training = models.DecimalField(max_digits = 3 , decimal_places = 2 ,blank = True , default = 0)
    retraning_needed = models.BooleanField(default = False)
    probable_date_of_retraining = models.DateField(blank = True, null = True)
    misc_data = models.CharField(max_length = 150, default = '' ,blank = True)
    def get_fields(self):
        fieldDetails = []
        for field in Grading._meta.fields:
            if not ( field.verbose_name == 'batch' or field.verbose_name == 'ID' or field.verbose_name == 'employee'):
                fieldDetails.append("" + field.verbose_name + ": " + field.value_to_string(self))
        return fieldDetails

    
class Feedback(models.Model):
    batch = models.ForeignKey(BatchDetails, null = True)
    employee = models.ForeignKey('Users.EmployeeInfo')
    expectations_met = models.DecimalField(max_digits = 3 , decimal_places = 2 ,blank = True, null = True)
    reasons_not_met = models.CharField(max_length = 300, null = True)
    pre_training = models.DecimalField(max_digits = 3 , decimal_places = 2 ,blank = True, null = True)
    post_training = models.DecimalField(max_digits = 3 , decimal_places = 2 ,blank = True, null = True)
    training_methodology = models.IntegerField(blank = True, null = True)
    use_of_AV_techniques = models.IntegerField(blank = True, null = True)
    quality_of_courseMaterial = models.IntegerField(blank = True, null = True)
    aoth = models.IntegerField(verbose_name = 'Arrangement Of Training Hall',blank = True, null = True)
    opinion = models.IntegerField(blank = True, null = True)
    subject_knowledge = models.IntegerField(blank = True , null = True)
    presentation_skills = models.IntegerField(blank = True, null = True)
    communication_skills = models.IntegerField(blank = True, null = True)
    iwp = models.IntegerField(verbose_name = 'Interactions With Participants',blank = True, null = True)
    suggestions = models.TextField(blank = True, null = True)
    def get_fields(self):
        fieldDetails = []
        for field in Feedback._meta.fields:
            if not ( field.verbose_name == 'batch' or field.verbose_name == 'ID' or field.verbose_name == 'employee'):
                fieldDetails.append("" + field.verbose_name + ": " + field.value_to_string(self))
        return fieldDetails
        
def content_file_name(instance, filename):
    return '/'.join(['Files', str(instance.year), instance.name + ".xls"])

class Files(models.Model):  
 
    name = models.CharField(max_length = 100,choices = variables.name_choices)
    
    
    modifiedBy = models.ManyToManyField('Users.EmployeeInfo' , null = True)
    year = models.CharField(max_length = 4 , choices = variables.year_choices)
    created = models.DateTimeField(auto_now_add=True,null = True)
    updated = models.DateTimeField(auto_now=True, null = True)
    details = models.CharField(max_length = 150)
    file = models.FileField(upload_to = content_file_name)
    def __unicode__(self):
        stri = "Name:" + self.name 
        return unicode(stri)
    
@receiver(post_delete, sender=Files)
def file_post_delete_handler(sender, **kwargs):
    filer = kwargs['instance']
    storage, path = filer.file.storage, filer.file.path
    storage.delete(path)
  

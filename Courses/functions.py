from Courses.models import Course
from datetime import datetime
from Courses import models,  formatGenerator
from Users import models as UserModels
from Users import userfunctions
from django.db.backends.sqlite3.base import IntegrityError
from TritonValvesTraining import settings
from Users.userfunctions import get_trainer_list
from django.core.files import File
from shutil import copyfile

def getCourseList(emp):
    return list(Course.objects.all())

def authorise_batch_edit(batch,emp):
    if emp.is_Admin:
        return True
    if emp.is_HOD or emp.is_Manager:
        if emp.department == batch.course.department:
            return True
    return False    
    
def start_batch(batch,emp = None ):
    if not authorise_batch_edit(batch,emp):
        return 
    batch.course_ongoing = True
    batch.actual_start_date = datetime.today()
    records = UserModels.CoursesToAttend.objects.filter(batch = batch)
    for record in records:
        try:
            models.CourseEmployeeList.objects.get(course = record.course , batch = record.batch , employee = record.employee)
        except models.CourseEmployeeList.DoesNotExist:
            models.CourseEmployeeList.objects.create(course = record.course , batch = record.batch , employee = record.employee).save() 
            
    records.delete()
    batch.save()
    
def stop_batch(batch,emp = None):
    if not authorise_batch_edit(batch,emp):
        return 
    batch.course_ongoing = False
    batch.course_completed = True
    batch.actual_stop_date = datetime.today()
    batch.save()
    
def complete_batch(batch,emp = None):
    """
    0 - Operation successfull
    1 - Grading not Done
    2 - Feedback not Done
    3 - Both Grading and Feedback not Done
    4- Batch Start not Done
    5 - Batch Stop not Done
    """
    if not authorise_batch_edit(batch,emp):
        return 
    if batch.course_ongoing == False and  batch.course_completed == False:
        return 4
    if batch.course_ongoing == False and  batch.course_completed == True:
        i = check_for_table_inconsistency(batch)
        print str(i)
        if i == 0:
            try:
                records = models.CourseEmployeeList.objects.filter(batch = batch)
            except models.CourseEmployeeList.DoesNotExist:
                return 4
            
            for record in records:
                UserModels.CoursesAttended.objects.create(course = record.course , batch = record.batch , employee = record.employee)
            print "reached Here"   
            batch.course_finished = True
            batch.save()
            return 0
        else:
            return i
    else:
        return 5
def nemployees_per_batch(batch):
    liste = list(models.CourseEmployeeList.objects.filter(batch = batch))
    return len(liste)

def batches_supposed_to_start(course ,batches,emp = None):
    today = datetime.today()
    try:
        if emp is not None:
            batchesL1 = models.BatchDetails.objects.filter(course = course , start_date__gte = today , course_ongoing = False , course_completed = False , course__department = emp.department)
        else:
            batchesL1 = models.BatchDetails.objects.filter(course = course , start_date__gte = today , course_ongoing = False , course_completed = False)
    except models.BatchDetails.DoesNotExist:
        return -1
    for batch in batchesL1:
        batches.append(batch)
    return 1

def batches_running(course,batches,emp = None):
    today = datetime.today()
    try:
        if emp is not None:
            batchesL1 = models.BatchDetails.objects.filter(course = course , start_date__gte = today , course_ongoing = False , course_completed = False , course__department = emp.department)
        else:
            batchesL1 = models.BatchDetails.objects.filter(course = course , start_date__gte = today , course_ongoing = False , course_completed = False)
    except models.BatchDetails.DoesNotExist:
        return -1
    for batch in batchesL1:
        batches.append(batch)
    return 1  

def batches_to_grade(igbatches,ifbatches , emp = None):
    if emp is not None:
        batches = list(models.BatchDetails.objects.filter(course_completed = True , course__department = emp.department, course_finished = False))
    else:
        batches = list(models.BatchDetails.objects.filter(course_completed = True,course_finished = False))
    for batch in batches:
        nepb = nemployees_per_batch(batch)
        try:
            liste = list(models.Grading.objects.filter(batch = batch))
            if len(liste) <  nepb :
                igbatches.append(batch)
        except models.Grading.DoesNotExist:
            igbatches.append(batch)
            
        try:
            liste = list(models.Feedback.objects.filter(batch = batch))
            if len(liste) <  nepb :
                ifbatches.append(batch)
        except models.Grading.DoesNotExist:
            ifbatches.append(batch)
        

        
        
def check_for_date_inconsistency(batch,errorList):
    #batch has to be started but isnt 
    """
    7 - batch has started early
    8- batch is yet to be stopped
    9 - batch is Supposed to have started but hasnt
    10 - batch has ended before it is supposed to 
    """
    today = datetime.today()
    
    if batch.start_date > today and (batch.course_ongoing or batch.course_completed ):
        errorList.append(7)
    if batch.stop_date < today and (batch.course_ongoing or not batch.course_completed ) :
        errorList.append(8)
    if batch.start_date < today and batch.stop_date > today and  (not batch.course_ongoing ):
        errorList.append(9)
    if batch.start_date < today and batch.stop_date > today and  ( batch.course_completed ):
        errorList.append(10)
    return errorList
    
    
def check_for_table_inconsistency(batch):
    i = 0
    nepb = nemployees_per_batch(batch)
    try: 
        liste = list(models.Grading.objects.filter(batch = batch))
        if len(liste) <  nepb :
            i = i + 1
    except models.Grading.DoesNotExist:
            ++i
            
    try:
        liste = list(models.Feedback.objects.filter(batch = batch))
        if len(liste) <  nepb :
            i += 2
    except models.Feedback.DoesNotExist:
        i += 2 
    return i 

def generateBatchFiles(batch,files,emp):
    """
    Each Batch Has
    1. l4PA3 An Attendance List - Generated Automatically
    2. L4PA5 A Grading Report by HOD - Either From FIle or Using the interface(The basic format is generated by the interface)
    3. L4PA9 A Grading and Feedback Report by Employee- Either from File or Using Interface(The basic format is generated by the interface)
    4.L4PA1 An Employee List - Generated Automatically
    """
    if batch is not None:
        
        filerL4PA3 = generate_L4PA3(batch,emp)
        files.append(filerL4PA3)
        filerL4PA5 = generate_L4PA5(batch,emp)
        files.append(filerL4PA5)
        filerL4PA9 = generate_L4PA9(batch,emp)
        files.append(filerL4PA9)
        filerL4PA1 = generate_L4PA1(batch,emp)
        files.append(filerL4PA1)
        tempfiles = []
        filerOthers = generate_Others(batch,tempfiles,emp)
        files.extend(filerOthers)
        
    setFiles = set(files)
    setFiles.remove(None)
    return setFiles
        
def generate_L4PA3(batch,emp):
    flag = True
    files = batch.files.all()
    for filer in files:
        if filer.name == 'L4PA3':
            flag = False
            return filer
    if(flag):
        file_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' +  '/'.join(['FilesCreated', str(batch.start_date.year), 'L4PA3.xls'])
        name = 'L4PA3'
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + '/'.join(['Files', str(batch.start_date.year), name + ".xls"])
        details = ' '
        employees = employees_of_batch(batch,emp)
        trainers = get_trainer_list(batch = batch)
        formatGenerator.make_l4pa3(batch, employees, trainers, file_location)
        filer = File(open(file_location))
        fileObj = models.Files.objects.create(name = name, details = details , file = filer , year = str(batch.start_date.year))
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + fileObj.file.name
        copyfile(file_location,model_location)
        fileObj.modifiedBy.add(emp)
        fileObj.save()
        batch.files.add(fileObj)
        batch.save()
        return fileObj
        """"""
    #Generate the file using Bavej's code
    # and return it

def generate_L4PA5(batch,emp):
    flag = True
    files = batch.files.all()
    for filer in files:
        if filer.name == 'L4PA5':
            flag = False
            return filer
    if(flag):
        """file_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' +  '/'.join(['FilesCreated', str(batch.start_date.year), 'L4PA5.xls'])
        name = 'L4PA5'
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + '/'.join(['Files', str(batch.start_date.year), name + ".xls"])
        details = ' '
        employeeFeedbacks = models.Feedback.objects.filter(batch= batch)
        trainers = get_trainer_list(batch = batch)
        formatGenerator.make_l4pa5(file_location, batch, trainers, employeeFeedbacks)
        filer = File(open(file_location))
        fileObj = models.Files.objects.create(name = name, details = details , file = filer , year = str(batch.start_date.year))
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + fileObj.file.name
        copyfile(file_location,model_location)
        fileObj.modifiedBy.add(emp)
        fileObj.save()
        batch.files.add(fileObj)
        batch.save()
        return fileObj"""
    #Generate the file using Bavej's code
    # and return it
    
    
def generate_L4PA9(batch,emp):
    flag = True
    files = batch.files.all()
    for filer in files:
        if filer.name == 'L4PA9':
            flag = False
            return filer
    if(flag):
        """"""
    #Generate the file using Bavej's code
    # and return it
    
    
def generate_L4PA1(batch,emp):
    flag = True
    files = batch.files.all()
    for filer in files:
        if filer.name == 'L4PA1':
            flag = False
            return filer
    if(flag):
        file_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' +  '/'.join(['FilesCreated', str(batch.start_date.year), 'L4PA1.xls'])
        name = 'L4PA1'
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + '/'.join(['Files', str(batch.start_date.year), name + ".xls"])
        details = ' '
        employees = employees_of_batch(batch,emp)
        trainers = get_trainer_list(batch = batch)
        formatGenerator.make_l4pa1(batch, employees, trainers, file_location)
        filer = File(open(file_location))
        fileObj = models.Files.objects.create(name = name, details = details , file = filer ,  year = str(batch.start_date.year))
        model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + fileObj.file.name
        copyfile(file_location,model_location)
        fileObj.modifiedBy.add(emp)
        fileObj.save()
        batch.files.add(fileObj)
        batch.save()
        return fileObj
    #Generate the file using Bavej's code
    # and return it


def generate_L4PA2(year ,emp ):
    courses = models.Course.objects.all().order_by('course_name')
    departments = UserModels.Department.objects.all()
    departmentsData = []
    for department in departments:
        departmentsData.append(DepartmentData(department))
    
    file_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' +  '/'.join(['FilesCreated',  'L4PA2.xls'])
    name = 'L4PA2'
    details = ' '

    formatGenerator.make_l4pa2(file_location = file_location, departments = departmentsData, courses = courses)
    filer = File(open(file_location))
    fileObj = models.Files.objects.create(name = name, details = details , file = filer ,  year = str(year))
    model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + fileObj.file.name
    copyfile(file_location,model_location)
    fileObj.modifiedBy.add(emp)
    fileObj.save()

    return fileObj
    
    
def process_calendar(calendar):
    """"""
def generate_calendar(year , emp):
    courses = list(models.Course.objects.all())
    coursedata = []
    for course in courses:
        coursedata.append(CourseData(course))
    file_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' +  '/'.join(['FilesCreated', str(year), 'AnnualCalendar.xls'])
    name = 'AC'
    details = 'Annual Calendar Template'
    formatGenerator.make_calendar(file_location, coursedata, year)
    filer = File(open(file_location))
    fileObj = models.Files.objects.create(name = name, details = details , file = filer ,  year = str(year))
    model_location = settings.MEDIA_ROOT.replace('\\','/')  + '/' + fileObj.file.name
    copyfile(file_location,model_location)
    fileObj.modifiedBy.add(emp)
    fileObj.save()    
    return fileObj
    
def generate_Others(batch ,files,emp):
    files = list(batch.files.all())
    files2 = []
    for filer in files:
        if not(filer.name == 'L4PA1' or filer.name == 'L4PA9' or filer.name == 'L4PA5' or filer.name == 'L4PA3'):
            files2.append(filer)
    
    return files2
            
def free_employees_for_batch(batch,emp):
    liste = []
    list2 = []
    if emp.is_Admin:
        try:
            liste =  list(UserModels.CoursesToAttend.objects.filter(course = batch.course , batch = None ))
        except UserModels.CoursesToAttend.DoesNotExist:
            liste = []
    elif emp.is_HOD:
        try:
            liste =  list(UserModels.CoursesToAttend.objects.filter(course = batch.course, employee__department = emp.department ,batch = None))
        except UserModels.CoursesToAttend.DoesNotExist:
            liste = []
    if liste != [] and len(liste) != 1:
        for item in liste:
            list2.append(item.employee)
        
        liste = list(set(list2))
        return liste
    if len(liste) == 1:
        list2.append(liste[0].employee)
        liste = list2
    for employee in liste:
        if not employee_is_free(batch, employee):
            liste.remove(employee)
        
    return liste

def employees_of_batch(batch,emp):
    liste = []
    list2 = []
    if batch.course_finished :
        if emp.is_Admin:
            try:
                liste =  list(UserModels.CoursesAttended.objects.filter(batch = batch))
            except UserModels.CoursesAttended.DoesNotExist:
                liste = []
        elif emp.is_HOD:
            try:
                liste = list(UserModels.CoursesAttended.objects.filter(batch = batch, employee__department = emp.department))
            except UserModels.CoursesAttended.DoesNotExist:
                liste = []
        
    elif emp.is_Admin:
        try:
            liste =  list(UserModels.CoursesToAttend.objects.filter(batch = batch))
            liste.extend(models.CourseEmployeeList.objects.filter(batch = batch))
        except UserModels.CoursesToAttend.DoesNotExist:
            liste = []
    elif emp.is_HOD:
        try:
            liste =  list(UserModels.CoursesToAttend.objects.filter(batch = batch, employee__department = emp.department))
            liste.extend(models.CourseEmployeeList.objects.filter(batch = batch, employee__department = emp.department))
        except UserModels.CoursesToAttend.DoesNotExist:
            liste = []
    if len(liste) == 1:
        liste[0] = liste[0].employee
    if liste != [] and len(liste) != 1:
        for item in liste:
            list2.append(item.employee)
        liste = set(list2)

    
    
    return list(liste)
def get_batches_for_emp(emp):
    print "here"
    batches = []
    liste = list(UserModels.CoursesToAttend.objects.filter(employee = emp ))
    if type(liste) == UserModels.CoursesToAttend:
        liste = [liste]
    for item in liste:
        if item.batch is not None:
            batches.append(item.batch)
    liste = list(models.CourseEmployeeList.objects.filter(employee = emp ))
    if type(liste) == models.CourseEmployeeList:
        liste = [liste]
    for item in liste:
        if item.batch is not None:
            batches.append(item.batch)
    
    return batches    
 
def have_in_common(q11,q12 , q21 , q22):
    if q11 < q21 and q21 < q12:
        return True
    if q11 > q21 and q11<q22:
        return True
    if q11 < q21 and q12 > q22:
        return True
    if q11 > q21 and q12 < q22:
        return True
    return False   

def employee_is_free(batchi ,emp):
    batches = get_batches_for_emp(emp) 
    for batch in batches:
        if have_in_common(batch.start_date ,batch.stop_date ,batchi.start_date ,batchi.stop_date ) and have_in_common(batch.start_time ,batch.stop_time ,batchi.start_time ,batchi.stop_time ):
            return False
    
    return True
            
def add_employee(batch, empl ,emp):
    if not employee_is_free(batch , empl):
        return False
    if userfunctions.authorised_to_handle(handler = emp,  batch = batch , employee = empl) and not batch.course_ongoing  and not batch.course_completed :
        try:
            record = UserModels.CoursesToAttend.objects.get(employee = empl , course = batch.course)
            record.batch = batch
            record.save()
            return True
        except UserModels.CoursesToAttend.DoesNotExist:
            return False        
    if userfunctions.authorised_to_handle(handler = emp,  batch = batch , employee = empl) and  batch.course_ongoing:
        try:
            record = UserModels.CoursesToAttend.objects.get(employee = empl , course = batch.course)
            record.batch = batch
            
            try:
                models.CourseEmployeeList.objects.get(course = record.course , batch = record.batch , employee = record.employee)
                return False
            except models.CourseEmployeeList.DoesNotExist:
                models.CourseEmployeeList.objects.create(course = record.course , batch = record.batch , employee = record.employee).save()
                if batch.course_ongoing:
                    record.delete()
                return True
            record.delete()
        except UserModels.CoursesToAttend.DoesNotExist:
            return False         

def remove_employee(batch, empl ,emp):
    if userfunctions.authorised_to_handle(handler = emp,  batch = batch , employee = emp) :
        try:
            record = UserModels.CoursesToAttend.objects.get(employee = empl , batch = batch)
            record.batch = None
            record.save()
            return True
        except UserModels.CoursesToAttend.DoesNotExist:
            try:
                record = models.CourseEmployeeList.objects.get(employee = empl, batch = batch)
                UserModels.CoursesToAttend.objects.create(employee = empl , course = batch.course).save()
                record.delete()
                return True 
            except models.CourseEmployeeList.DoesNotExist:
                return False

def get_feedback_query_set(batch,emp):      
    empsInBatch  = employees_of_batch(batch, emp)
    for employee in empsInBatch:
        try:
            models.Feedback.objects.get(batch = batch, employee = employee)
        except models.Feedback.DoesNotExist:
            models.Feedback.objects.create(batch = batch , employee = employee )
        
    return models.Feedback.objects.filter(batch = batch , employee__in = empsInBatch)
def get_grading_query_set(batch,emp):      
    empsInBatch  = employees_of_batch(batch, emp)
    for employee in empsInBatch:
        try:
            models.Grading.objects.get(batch = batch, employee = employee)
        except models.Grading.DoesNotExist:
            models.Grading.objects.create(batch = batch , employee = employee )
        
    return models.Grading.objects.filter(batch = batch , employee__in = empsInBatch)

def add_trainer_to_course(employee,course):
    try:
        models.CoursewiseTrainer.objects.create(course = course , employee = employee)
        batches = get_batches_to_start(course)
        for batch in batches:
            add_trainer_to_batch(employee,batch)
        return "Trainer Added"
    except IntegrityError:
        return "For some reason the trainer isnt added to this course, contact the IT Admin"
    
def remove_trainer_from_course(employee,course):
    try:
        emp = models.CoursewiseTrainer.objects.get(employee = employee)
        emp.delete()
        return "The trainer was successfully deleted."
    except models.CoursewiseTrainer.DoesNotExist:
        return " Not possible."

def add_trainer_to_batch(employee,batch):
    if batch.course_finished :
        return " The batch is done and dusted with."
    empsInBatch = employees_of_batch(batch, employee)
    if employee in empsInBatch:
        return "The trainer is supposed to be attending the course , remove the person from the batch-employee List, then try."
    try:
        models.BatchwiseTrainer.objects.get(batch = batch , employee = employee)
        return " Trainer already exists."
    except models.BatchwiseTrainer.DoesNotExist:
        try:
            models.BatchwiseTrainer.objects.create(batch = batch , employee = employee)
            return "Trainer Added to Batch."
        except IntegrityError:
            return " Trainer wasn't added to the batch."
    
    
def remove_trainer_from_batch(employee,batch):
    empsInBatch = employees_of_batch(batch, employee)
    if batch.course_finished :
        return " The batch is done and dusted with."
    if employee in empsInBatch:
        return "The trainer is supposed to be attending the course , remove the person from the batch-employee List, then thry."
    try:
        trainer = models.BatchwiseTrainer.objects.get(batch = batch , employee = employee)
        trainer.delete()
        return "Trainer Deleted From Batch."
    except models.BatchwiseTrainer.DoesNotExist:
        return " Trainer wasn't added to the batch in the first place."
        
def get_batches_to_start(course = None):
    
    batchesToStart = models.BatchDetails.objects.filter(course_ongoing = False,course_completed = False , course_finished = False)    
    batches = batchesToStart
    if course is not None:
        batches =  batchesToStart.filter(course = course)  
    return batches

def add_deafult_trainers_to_batch(batch):
    trainers = userfunctions.get_trainer_list(course = batch.course)
    for trainer in trainers:
        add_trainer_to_batch(trainer, batch)

class CourseData:
    def __init__(self,course):
        self.course_name = course.course_name
        deptNames = []
        for department in course.department.all():
            deptNames.append(department.dept_name)
        self.departments = ','.join(deptNames)
        wcount = len(list(UserModels.CoursesToAttend.objects.filter(employee__is_Staff = False , employee__is_Admin = False , employee__is_HOD = False ,employee__is_Manager  = False , course = course)))
        scount = len(list(UserModels.CoursesToAttend.objects.filter(employee__is_Staff = True , course = course)))
        self.wscount = str(wcount) + "/" + str(scount)
        trainers = userfunctions.get_trainer_list(course = course)
        self.internal = ''
        self.external = ''
        trainerNames = []
        for trainer in trainers:
            trainerNames.append(trainer.userObj.first_name + " " + trainer.userObj.last_name)
            if trainer.is_Internal:
                self.internal = 'Y'
            else:
                self.external = 'Y'
            
           
        
class DepartmentData():
    def __init__(self, department):
        self.department = department
        self.department_name = department.dept_name
        hods = userfunctions.get_hod_of_department(department)
        hodNames = []
        for hod in hods:
            hodNames.append(hod.userObj.first_name + " " + hod.userObj.last_name)
        self.hod = ','.join(hodNames)
            
    def get_employees(self):
        queryset =  UserModels.EmployeeInfo.objects.filter(department = self.department)
        employees = []
        for employee in queryset:
            employees.append(EmployeeCourseData(employee))
        return employees
            
            
        
class EmployeeCourseData():
    def __init__(self,employee):
        courses = models.Course.objects.all().order_by('course_name')
        self.userId = employee.userId
        self.name = employee.userObj.first_name + employee.userObj.last_name
        i = 1
        self.courses = {}
        for course in courses:
            try:
                UserModels.CoursesToAttend.objects.get(employee = employee , course = course)
                stri = 'Y'
            except UserModels.CoursesToAttend.DoesNotExist:
                stri = ''
            self.courses.update({i:stri})
            i = i+1
    def getcourses(self):
        return self.courses
        
        
        
        
        
        
        
        
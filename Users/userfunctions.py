from Users.models import EmployeeInfo, Department
from Users import models, EmployeeListReader
from Courses import models as Cmodels
from Courses.models import CoursewiseTrainer
from django.contrib.auth.models import User

def getEmployeeList(emp, course = 'None'):
    alldept = models.Department.objects.get(deptID = 'ALL')
    if course ==  'None':
        if emp.is_Admin:
            return list(EmployeeInfo.objects.all())
        if emp.is_HOD or emp.is_Manager:
            dept = emp.department
            try:
                liste = list(EmployeeInfo.objects.filter(department = dept))
            except EmployeeInfo.DoesNotExist:
                liste = []
            return liste
    else:
        if emp.is_Admin:
            if alldept not in course.department.all():
                liste2 = course.department.all()
                return list(EmployeeInfo.objects.filter(department__in = liste2 ))
            return list(EmployeeInfo.objects.all())
        elif emp.is_HOD or emp.is_Manager and (emp.department in course.department.all()):
            dept = emp.department
            try:
                liste = list(EmployeeInfo.objects.filter(department = dept))
            except EmployeeInfo.DoesNotExist:
                liste = []
            return liste
        else:
            return []
        
        
def get_courses_attended(emp):
    try:
        liste = list(models.CoursesAttended.objects.filter(employee = emp))
    except models.CoursesAttended.DoesNotExist:
        liste = []
    return liste

def get_courses_to_attend(emp):
    try:
        liste = list(models.CoursesToAttend.objects.filter(employee = emp))
    except models.CoursesToAttend.DoesNotExist:
        liste = []
    return liste

def get_notifications(emp):
    try:
        liste = list(models.Notification.objects.filter(employee = emp))
    except models.Notification.DoesNotExist:
        liste = []
    return liste    

def authorised_to_handle(handler , employee = None , batch = None , course = None):
    all_dept = Department.objects.get(deptID = 'ALL')
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
        
def get_trainer_list(course = None, batch = None):
    lst = []
    if batch is not None:
        lst2 =  list(Cmodels.BatchwiseTrainer.objects.filter(batch = batch))
    
    if course is not None:
        lst2 = list(CoursewiseTrainer.objects.filter(course = course))
        
    if not lst2 == [] :
        for elem in lst2:
            lst.append(elem.employee)
    return lst    

def get_hod_of_department(department):    
    hods = list(EmployeeInfo.objects.filter(department = department , is_HOD = True))
    return hods

def create_workers_from_list(list_file_location,emp):
    errors = []
    empList = []

    if emp.is_Admin:
        employees = EmployeeListReader.readEmployees(list_file_location)
        
        for employee in employees:
            dept_name = employee.department
            try:
                department = models.Department.objects.get(dept_name = dept_name)
            except models.Department.DoesNotExist:
                department = None
                department = models.Department.objects.create(dept_name = dept_name , deptID = dept_name)
                #errors.append("Employee with ID " + employee.idno + " Wasnt added because the department Name wasn't matching with the ones in the Database. (" + dept_name +")  Create a new Department if it is not created for this name. ")   
            if department is not None:        
                try:
                    user = User.objects.get(username = employee.idno)
                    user.first_name = employee.name.split(' ',1)[0]
                    if len(employee.name.split(' ',1)) > 1:
                        user.last_name = employee.name.split(' ',1)[1]
                    user.save()
                    empl = EmployeeInfo.objects.get(userObj = user)
                    empl.unit = employee.unit
                    if employee.cat == 'TR-ST' or employee.cat == 'STAFF':
                        empl.is_Staff = True
                    empl.designation = employee.cat
                    empl.department = department
                    empl.save()
                    #empList.append(empl)
                except User.DoesNotExist:
                    user = User.objects.create_user(username = employee.idno , password = employee.idno , email = "default@trtionvalves.com")
                    user.first_name = employee.name.split(' ',1)[0]
                    if len(employee.name.split(' ',1)) > 1:
                        user.last_name = employee.name.split(' ',1)[1]
                    user.save()
                    if employee.cat == 'TR-ST' or employee.cat == 'STAFF':
                        empl = EmployeeInfo(userObj = user , is_Staff = True ,userId = employee.idno,  unit = employee.unit , designation = employee.cat , phone_Number = 0 ,address = "NA" , current_shift = "NA" , department = department)
                    else:
                        empl = EmployeeInfo(userObj = user ,userId = employee.idno,  unit = employee.unit , designation = employee.cat , phone_Number = 0 ,address = "NA" , current_shift = "NA" , department = department)
                    empl.save()
                    empList.append(empl)
    wl = WorkerList(errors,empList)
    return wl
    
class WorkerList():
    def __init__(self, errors , empList ):
        self.errors = errors
        self.empList = empList
                
            
            
        

from django.template import  Context
from django.http import HttpResponse
from django.template.loader import get_template
#from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import  render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Users.models import EmployeeInfo,Department , CoursesAttended,\
    CoursesToAttend
from Courses.models import   BatchDetails,  Feedback,Grading,  CourseEmployeeList,\
    Course
from Users import userfunctions
from functools import wraps
from Users.forms import  DepartmentForm, HODForm, ManagerForm, EmployeeEditForm, EmployeeForm, UserForm
from django.contrib.admin.helpers import AdminForm
from django.http.response import HttpResponseForbidden
import Courses
from Courses.forms import YearForm

def emp_auth_needed(view_func):
    @login_required
    def _decorator(request, *args, **kwargs):
        # maybe do something before the view_func call
        if not request.user.is_authenticated():
            return HttpResponseRedirect('../../../login')
        try:
            emp = EmployeeInfo.objects.all().get(user = request.user )
        except EmployeeInfo.DoesNotExist:
            emp = None
        
        if emp is None:
            return HttpResponseForbidden()
        response = view_func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(view_func)(_decorator)
# Create your views here.
@emp_auth_needed
def user_registration(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if request.user.is_authenticated() and emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_Manager ) :
        if request.POST :
            userForm = UserForm(request.POST)
            if userForm.is_valid() :
                userForm.save()
                request.session["count1"] += 1
                request.session["username"] = userForm.cleaned_data['username'] 
                return HttpResponseRedirect('../../../' + request.GET["empType"])
            else:
                c = Context({'emp1':emp ,'form':userForm })
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
            
        else:
            userForm = UserForm()
            
            #t = get_template('employeeRegistration.html')
            c = Context({'emp1':emp ,'form':userForm})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponseRedirect('../../../login')
    
    
@emp_auth_needed  
def  employee_registration(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if (request.session["count2"] - request.session["count1"] == -1) and emp is not None :
        if request.POST :
            user = User.objects.all().get(username = request.session["username"] ) 
            employee = EmployeeInfo(user = user )
            employeeForm = EmployeeForm(request.POST,instance = employee )
            
            if employeeForm.is_valid() :
                empl = employeeForm.save(commit = False)
                if emp.authorised_to_handle(empl):
                    empl.save()
                else:
                    user.delete()
                    return HttpResponseForbidden("Not authorised to do this")
                
                request.session["count2"] += 1
                t = get_template('added.html')
                c = Context({'emp1':emp ,'employee':employeeForm.save() })
                return HttpResponse(t.render(c))
            else :
                #t = get_template('registration.html')
                c = Context({'emp1':emp ,'form': employeeForm})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
            
            
        else:       
            employeeForm =  EmployeeForm()
            
            c = Context({'emp1':emp ,'form': employeeForm })
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponse('We are sorry but some error has occurred try to register again  from the start ')

def booleanize(var): 
    if var == 'true' :
        return True  
    return False

def authorise(var,typer,emp):
    if emp.is_Admin:
        return var
    if emp.is_HOD and (typer != 'admin'):
        return var
    if emp.is_Manager and(typer != 'hod' or typer != 'admin' ):
        return var
    
    return 'false'
    
def determineEmpType(empObj, empl,manager,hod,admin , staff):
    if admin:
        if empObj.is_Admin:
            return True
    if hod:
        if empObj.is_HOD:
            return True
    if manager:
        if empObj.is_Manager:
            return True
    if staff:
        if empObj.is_Staff:
            return True
    if empl:
        if not empObj.is_Admin and not empObj.is_Manager and not empObj.is_HOD and not empObj.is_Staff:
            return True
    if not empl and not hod and not manager and not admin and not staff:
        return True
    return False

def determineAuthType(empObj,empl):
    if empl.is_Admin:
        return True
    if empl.is_HOD and (not empObj.is_Admin):
        return True
    if empl.is_Manager and not ( empObj.is_Admin or empObj.is_HOD):
        return True
    return False
@emp_auth_needed
def search_results(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        set2 = userfunctions.getEmployeeList(emp,working_Status = [True,False])
        if request.GET:
            userID = request.GET['userID'].encode('ascii','ignore')
            username = request.GET['username'].encode('ascii','ignore')
            first_name = request.GET['first_name'].encode('ascii','ignore')
            last_name = request.GET['last_name'].encode('ascii','ignore')
            empl = booleanize(authorise(request.GET['w'].encode('ascii','ignore'),'emp',emp))
            manager = booleanize(authorise(request.GET['m'].encode('ascii','ignore'),'mang',emp))
            hod = booleanize(authorise(request.GET['h'].encode('ascii','ignore'),'hod',emp))
            admin = booleanize(authorise(request.GET['a'].encode('ascii','ignore'),'admin',emp))
            staff = booleanize(authorise(request.GET['s'].encode('ascii','ignore'),'staff',emp))
            tempset = []
            cond =  not(empl or hod or admin or manager or staff)
            if (first_name == '' and  last_name == '' and  userID == '' and  username == '' ) and not cond:
                for elem in set2:
                    if determineEmpType(elem,empl,manager,hod,admin , staff):
                        tempset.append(elem)
            
            elif  not ( first_name == '' and  last_name == '' and  userID == '' and  username == '' and cond ):
                if not first_name == '' :
                    for elem in set2:
                        
                        if (elem.user.first_name.lower()).find(first_name.lower()) >= 0  and determineEmpType(elem,empl,manager,hod,admin, staff):
                            tempset.append(elem)
                if not last_name == '':
                    for elem in set2:
                        if (elem.user.last_name.lower()).find(last_name.lower()) >= 0 and determineEmpType(elem,empl,manager,hod,admin, staff):
                            tempset.append(elem)
                if not userID == '':
                    for elem in set2:
                        if (elem.userId.lower()).find(userID.lower()) >= 0 and determineEmpType(elem,empl,manager,hod,admin, staff) :
                            tempset.append(elem)
                if not username == '':
                    for elem in set2:
                        if (elem.user.username.lower()).find(username.lower()) >= 0 and determineEmpType(elem,empl,manager,hod,admin, staff):
                            tempset.append(elem)
                            
            else:
                for elem in set2:
                    if (determineEmpType(elem,empl,manager,hod,admin, staff)):
                        tempset.append(elem)
            c = Context({'emp1':emp ,'list': tempset})
            t = get_template('employeeList.html')
            return HttpResponse(t.render(c))
        else:
            tempset = []
            for elem in set2:
                if (determineAuthType(elem,emp)):
                    tempset.append(elem)
            c = Context({'emp1':emp ,'list': tempset})
            t = get_template('employeeList.html')
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')

@emp_auth_needed
def search_page(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        m = request.GET.get('m' ,False)
        h = request.GET.get('h' ,False)
        a = request.GET.get('a' ,False)
        w = request.GET.get('w' ,False)
        c = Context({'emp1':emp ,'m':m , 'h':h , 'a': a, 'w': w})
        t = get_template('searchPage.html')
        return HttpResponse(t.render(c))
    
    return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')

@emp_auth_needed
def employee_edit(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        userId = request.GET['userid'].encode('ascii','ignore') 
        empl = EmployeeInfo.objects.get(userId = userId) 
        if not request.POST:

            form  = EmployeeEditForm(instance = empl)
            form.set_exclude(emp)
            c = Context({'emp1':emp ,"form":form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
        else:
            form = EmployeeEditForm( request.POST,instance = empl)
            form.save()
            t = get_template('added.html')
            c = Context({'emp1':emp ,"employee":form.save()})
            
            return HttpResponse(t.render(c))    


@emp_auth_needed
def employee_delete(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_Manager):
        empdelID = request.GET['empId']
        empdel = EmployeeInfo.objects.get(userId = empdelID) 
        user = empdel.user
        username = user.username
        if emp.is_Admin:
            empdel.delete()
            user.delete()
            var = "The employee with id: " + empdelID + "User Login Name: " + username +  "has been deleted from the records."
            return HttpResponse(var)
        if emp.is_HOD and not empdel.is_Admin and not empdel.is_HOD:
            empdel.delete()
            user.delete()
            var = "The employee with id: " + empdelID + "User Login Name: " + username +  "has been deleted from the records."
            return HttpResponse(var)
        if emp.is_Manager and not empdel.is_Admin and not empdel.is_HOD and not empdel.is_Manager:
            empdel.delete()
            user.delete()
            var = "The employee with id: " + empdelID + "User Login Name: " + username +  "has been deleted from the records."
            return HttpResponse(var)
        return HttpResponse("You are not authorised to do this . ")     
    
@emp_auth_needed 
def view_complete_emp(request):
    empid = request.GET.get('empid', '').encode('ascii','ignore')
    emp = get_object_or_404(EmployeeInfo,id = empid) 
    coursesAttended = CoursesAttended.objects.filter(employee = emp)
    coursesToAttend = CoursesToAttend.objects.filter(employee = emp)  
    coursesAttending = CourseEmployeeList.objects.filter(employee = emp)
    t = get_template('empDetails.html')
    emp1 = EmployeeInfo.objects.all().get(user = request.user )
    c = Context({'emp1':emp1 ,'emp':emp,'coursesAttended':coursesAttended,'coursesToAttend':coursesToAttend,'coursesAttending':coursesAttending})
    return HttpResponse(t.render(c))  
@emp_auth_needed 
def view_emp_grades(request):
    empid = request.GET.get('empid', '').encode('ascii','ignore')
    batchid =  request.GET.get('batchid', '').encode('ascii','ignore')
    batch = BatchDetails.objects.get(id = batchid)
    employee  = BatchDetails.objects.get(id = empid)
    Grades = Grading.objects.get(employee = employee , batch = batch)
    Feedback = Courses.models.Feedback.objects.get(employee = employee , batch = batch)
    print Grades
    t = get_template('graded.html')
    emp = EmployeeInfo.objects.all().get(user = request.user )
    c = Context({'emp1':emp ,'list':[Grades,Feedback],'grading':True})
    return HttpResponse(t.render(c))  
    
@emp_auth_needed 
def view_course_employee_details(request): 
    empid = request.GET.get('empid', '').encode('ascii','ignore')
    emp = get_object_or_404(EmployeeInfo,id = empid) 
    batchid = request.GET.get('batchid','').encode('ascii','ignore') 
    batch = BatchDetails.objects.get(id = batchid)  
    grades = get_object_or_404(Grading,batch = batch , employee = emp)   
    feedback = get_object_or_404(Feedback,batch = batch , employee = emp)  
    t = get_template('gradeDetails.html')
    c = Context({'emp1':emp ,'emp':emp, 'batch':batch , 'grades':grades, 'feedback':feedback})
    return HttpResponse(t.render(c))

    
    
    
    
    
@emp_auth_needed 
def  manager_registration(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if (request.session["count2"] - request.session["count1"] == -1) and emp is not None and (emp.is_Admin or emp.is_HOD):
        if request.POST :
            user = User.objects.all().get(username = request.session["username"] ) 
            employee = EmployeeInfo(user = user ,is_Staff = False , is_Manager = True ,is_HOD = False)
            managerForm = ManagerForm(request.POST,instance = employee )
            
            if managerForm.is_valid():
                empl = managerForm.save(commit = False)
                if emp.authorised_to_handle(empl):
                    empl.save()
                else:
                    user.delete()
                    return HttpResponseForbidden("Not authorised to do this")
                request.session["count2"] += 1
                t = get_template('added.html')
                c = Context({'emp1':emp ,'employee':managerForm.save() })
                return HttpResponse(t.render(c))
            else :
                #t = get_template('registration.html')
                c = Context({'emp1':emp ,'form': managerForm})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
            
            
        else:       
            managerForm =  ManagerForm()
            c = Context({'emp1':emp ,'form': managerForm})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponse('We are sorry but some error has occurred try to register again  from the start ')
    
@emp_auth_needed   
def  admin_registration(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if (request.session["count2"] - request.session["count1"] == -1) and emp is not None and emp.is_Admin:
        if request.POST :
            user = User.objects.all().get(username = request.session["username"] ) 
            employee = EmployeeInfo(user = user ,is_Staff = False)
            adminForm = AdminForm(request.POST,instance = employee )
            if adminForm.is_valid():
                adminForm.save()
                request.session["count2"] += 1
                t = get_template('added.html')
                c = Context({'emp1':emp ,'employee':adminForm.save() })
                return HttpResponse(t.render(c))
            else :
                #t = get_template('registration.html')
                c = Context({'emp1':emp ,'form': adminForm})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
            
            
        else:       
            adminForm =  AdminForm()
            c = Context({'emp1':emp ,'form': adminForm})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponse('We are sorry but some error has occurred try to register again  from the start ')
    
    
@emp_auth_needed   
def  hod_registration(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    
    if (request.session["count2"] - request.session["count1"] == -1) and emp is not None and emp.is_Admin:
        if request.POST :
            user = User.objects.all().get(username = request.session["username"] ) 
            hod = EmployeeInfo(user = user , is_Staff = False ,  is_HOD = True )
            hodForm = HODForm(request.POST,instance = hod )
            if hodForm.is_valid() :
                hod = hodForm.save()  
                request.session["count2"] += 1
                t = get_template('added.html')
                c = Context({'emp1':emp ,'employee':hodForm.save() })
                return HttpResponse(t.render(c))
            else :
                #t = get_template('registration.html')
                c = Context({'emp1':emp ,'form': hodForm})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
            
            
        else:       
            hodForm =  HODForm()
            c = Context({'emp1':emp ,'form': hodForm})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponse('We are sorry but some error has occurred try to register again  from the start ')
        
        

@emp_auth_needed
def create_department(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
        
    if emp is not None and emp.is_Admin :
        if request.POST:
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                deptID = form.cleaned_data['deptID']
                dept = Department.objects.get(deptID = deptID)
                t = get_template('deptAdded.html')
                c = Context({'emp1':emp ,'dept':dept})
                return HttpResponse(t.render(c))
        else:
            form = DepartmentForm()
            c = Context({'emp1':emp ,'form': form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
@emp_auth_needed       
def search_department(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
        
    if emp is not None and emp.is_Admin:
        depts = list(Department.objects.all())
        t = get_template("indeptsSearch.html")
        c = Context({'emp1':emp ,'depts':depts})
        return HttpResponse(t.render(c))
@emp_auth_needed
def edit_department(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and emp.is_Admin:
        deptID = request.GET['deptID']
        dept = Department.objects.get(deptID = deptID)
        if request.POST:
            form = DepartmentForm(request.POST,instance = dept)
            form.save()
            t = get_template('deptAdded.html')
            c = Context({'emp1':emp ,'dept':dept})
            return HttpResponse(t.render(c))
        else:
            form = DepartmentForm(instance = dept)
            c = Context({'emp1':emp ,'form':form}) 
            return render_to_response('registration.html', context_instance=RequestContext(request,c))

@emp_auth_needed       
def delete_department(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and emp.is_Admin:
        deptID = request.GET['deptID']
        dept = Department.objects.get(deptID = deptID)
        deptname = dept.dept_name
        dept.delete()
        vari = " The department " + deptname + " with ID" + deptID +' has been deleted.'
        return HttpResponse(vari) 
@emp_auth_needed 
def generate_schedule(request): 
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin ):
        if request.POST:
            form = YearForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                liste = []
                message = "Here is the schedule ."
                t = get_template('documentList.html')
                liste = [userfunctions.generate_schedule(int(year), emp)]    
                c = Context({'emp1':emp ,'documents': liste})
                c = RequestContext(request,c)
                return HttpResponse(t.render(c))
            else:
                c = Context({'emp1':emp ,'form':form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
        else:
            form = YearForm()
            c = Context({'emp1':emp ,'form':form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))   
    else:
        return HttpResponse("You are not authorised to view this.")  
@emp_auth_needed 
def down_employee_list_template(request): 
    emp = EmployeeInfo.objects.all().get(user = request.user )
    if emp.is_Admin:
        filer  = userfunctions.generate_employee_list_template()
        t = get_template('documentList.html')
        c = Context({'emp1':emp ,'documents': [filer]})
        return HttpResponse(t.render(c))
    return HttpResponseRedirect("../../loggedin")
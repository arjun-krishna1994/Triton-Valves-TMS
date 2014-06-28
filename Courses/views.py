
from django.template import  Context
from django.http import HttpResponse
from django.template.loader import get_template
#from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import  render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from Users.models import EmployeeInfo, CoursesToAttend
from Courses.models import  Course, BatchDetails, Files, Feedback,Grading
from django import forms
import Users
import Courses
from Courses import functions
from Users import userfunctions
from django.views.decorators.csrf import csrf_exempt 
from TritonValvesTraining import settings
from datetime import datetime
from django.forms.models import modelformset_factory
from functools import wraps
from django.http.response import HttpResponseForbidden
from Users.userfunctions import get_trainer_list
from Courses.functions import add_trainer_to_course, remove_trainer_from_course
from Courses.forms import FileForm, YearForm, GradingForm, FeedbackForm,\
    BatchForm, CourseAssignmentData, CourseForm
from Users.forms import EmployeeCourseData, CourseData
from Users.views import determineAuthType, booleanize
# Create your views here.

def emp_auth_needed(view_func):
    @login_required
    def _decorator(request, *args, **kwargs):
        # maybe do something before the view_func call
        if not request.user.is_authenticated():
            return HttpResponseRedirect('../../../login')
        try:
            emp = EmployeeInfo.objects.all().get(userObj = request.user )
        except EmployeeInfo.DoesNotExist:
            emp = None
        
        if emp is None:
            return HttpResponseForbidden()
        response = view_func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(view_func)(_decorator)
@emp_auth_needed
def create_course(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
        
    if emp is not None and (emp.is_Admin or emp.is_HOD) :
        if request.POST:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.do_clean_department(emp)
                form.save()
                course = form.save()
                t = get_template('courseAdded.html')
                c = Context({'course':course})
                return HttpResponse(t.render(c))
            else:
                c = Context({'form': form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))                
        else:
            form = CourseForm()
            c = Context({'form': form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
        
        
@emp_auth_needed       
def search_course(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD):
        courses = functions.getCourseList(emp)
        t = get_template("coursesSearch.html")
        c = Context({'courses':courses})
        return HttpResponse(t.render(c))
    else:
        return HttpResponseRedirect("../../../loggedin")
    
@emp_auth_needed
def edit_course(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD):
        course_id = request.GET['course_id']
        course = Course.objects.get(course_id = course_id)
        if request.POST:
            form = CourseForm(request.POST,instance = course)
            if form.is_valid():
                form.do_clean_department(emp)
                form.save()
                t = get_template('courseAdded.html')
                c = Context({'course':course})
                return HttpResponse(t.render(c))
            else:
                c = Context({'form':form}) 
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
                
        else:
            form = CourseForm(instance = course)
            c = Context({'form':form}) 
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        return HttpResponseRedirect("../../../loggedin")
        
@emp_auth_needed       
def delete_course(request):

    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD):
        course_id = request.GET['course_id']
        course = Course.objects.get(course_id = course_id)
        coursename = course.course_name
        course.delete()
        vari = " The course with name " + coursename + " with ID" + course_id +' has been deleted.'
        return HttpResponse(vari)    
    
     




@emp_auth_needed 
def add_ttc_main(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        t = get_template('ttcMain.html')
        courses = functions.getCourseList(emp)
        c = Context({'courses':courses}) 
        return HttpResponse(t.render(c))
            
    else: 
        return HttpResponseRedirect("../../logout")

@emp_auth_needed    
def ttc_emp_list(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        
        if request.GET:
            
            userID = request.GET['userID'].encode('ascii','ignore')
            username = request.GET['username'].encode('ascii','ignore')
            first_name = request.GET['first_name'].encode('ascii','ignore')
            last_name = request.GET['last_name'].encode('ascii','ignore')
            courseid = request.GET['courseid'].encode('ascii','ignore')
            tempset = []
            try:
                course = Course.objects.get(course_id = courseid)
            except Course.DoesNotExist:
                course = None
            if course is not None:
                set3  = []
                set2 = userfunctions.getEmployeeList(emp)
                trainers = userfunctions.get_trainer_list(course)
                for item in set2:
                    if not (item in trainers):
                        set3.append(item)
                set2 = set3                   
            else:
                set2 = []
            if(first_name == '' and  last_name == '' and  userID == '' and  username == '' and course is not None ):
                c = Context({'list': set2})
                t = get_template('addList.html')
                return HttpResponse(t.render(c))
                
            if  not ( first_name == '' and  last_name == '' and  userID == '' and  username == '' and course is not None  and set2  == []):
                if not first_name == '' :
                    for elem in set2:
                        if (elem.first_name.lower()).find(first_name.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not last_name == '':
                    for elem in set2:
                        if (elem.last_name.lower()).find(last_name.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                if not userID == '':
                    for elem in set2:
                        if (elem.userId.lower()).find(userID.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not username == '':
                    for elem in set2:
                        if (elem.userObj.username.lower()).find(username.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                
            else:
                tempset = []
            c = Context({'list': tempset})
            t = get_template('addList.html')
            return HttpResponse(t.render(c))
        else:
            tempset = []
            c = Context({'list': tempset})
            t = get_template('addList.html')
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')

@emp_auth_needed 
def ttc_trainer_list(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        if request.GET:
            courseid = request.GET['courseid'].encode('ascii','ignore')
            try:
                course = Course.objects.get(course_id = courseid)
            except Course.DoesNotExist:
                course = None
            if course is not None:
                set2 = get_trainer_list(course = course)
            else:
                set2 = []
            
            t = get_template('addedList.html')
            c = Context({'list': set2})
            return HttpResponse(t.render(c))
        else:
            t = get_template('addedList.html')
            c = Context({'list': []})
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')    

@emp_auth_needed
def add_ttc(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        idt = request.GET['id'].encode('ascii','ignore')
        courseid = request.GET['course'].encode('ascii','ignore') 
        course = Course.objects.get(course_id = courseid)
        empl = EmployeeInfo.objects.get(id = idt)
        res  = add_trainer_to_course(employee = empl, course = course)
        return HttpResponse(res)
    else: 
        return HttpResponseRedirect("../../logout")

@emp_auth_needed    
def del_ttc(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        #nothing
        empid = request.GET['empid'].encode('ascii','ignore')
        courseid = request.GET['course'].encode('ascii','ignore') 
        course = Course.objects.get(course_id = courseid)
        empl = EmployeeInfo.objects.get(id = empid)
        res = remove_trainer_from_course(course = course , employee = empl)
        return HttpResponse(res)
    else: 
        return HttpResponseRedirect("../../logout")
    
def ajax_trial(request):
    t = get_template("ajaxTrial.html")
    c = Context({})
    return HttpResponse(t.render(c))
        
def trial_post(request):
    name = request.POST["name"]
    return HttpResponse(name)

@emp_auth_needed 
def add_ttb_main(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        batchid = request.GET.get('batchid',None).encode('ascii','ignore')
        batch = BatchDetails.objects.get(id = batchid)
        t = get_template('ttbMain.html')
        c = Context({'batch':batch}) 
        return HttpResponse(t.render(c))
            
    else: 
        return HttpResponseRedirect("../../logout")

@emp_auth_needed    
def ttb_emp_list(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        
        if request.GET:
            
            userID = request.GET.get('userID','').encode('ascii','ignore')
            username = request.GET.get('username','').encode('ascii','ignore')
            first_name = request.GET.get('first_name','').encode('ascii','ignore')
            last_name = request.GET.get('last_name','').encode('ascii','ignore')
            batchid = request.GET.get('batchid','').encode('ascii','ignore')
            tempset = []
            try:
                batch = BatchDetails.objects.get(id = batchid)
            except BatchDetails.DoesNotExist:
                batch = None
            if batch is not None:
                set3  = []
                set2 = userfunctions.getEmployeeList(emp)
                trainers = userfunctions.get_trainer_list(batch = batch)
                for item in set2:
                    if not (item in trainers):
                        set3.append(item)
                set2 = set3                   
            else:
                set2 = []
            if(first_name == '' and  last_name == '' and  userID == '' and  username == '' and batch is not None ):
                c = Context({'list': set2, 'batch':batch})
                t = get_template('addList2.html')
                return HttpResponse(t.render(c))
                
            if  not ( first_name == '' and  last_name == '' and  userID == '' and  username == '' and batch is not None  and set2  == []):
                if not first_name == '' :
                    for elem in set2:
                        if (elem.first_name.lower()).find(first_name.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not last_name == '':
                    for elem in set2:
                        if (elem.last_name.lower()).find(last_name.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                if not userID == '':
                    for elem in set2:
                        if (elem.userId.lower()).find(userID.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not username == '':
                    for elem in set2:
                        if (elem.userObj.username.lower()).find(username.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                
            else:
                tempset = []
            c = Context({'list': tempset, 'batch':batch})
            t = get_template('addList2.html')
            return HttpResponse(t.render(c))
        else:
            tempset = []
            c = Context({'list': tempset})
            t = get_template('addList2.html')
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')

@emp_auth_needed 
def ttb_trainer_list(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        if request.GET:
            batchid = request.GET['batchid'].encode('ascii','ignore')
            try:
                batch = BatchDetails.objects.get(id = batchid)
            except BatchDetails.DoesNotExist:
                batch = None
            if batch is not None:
                set2 = get_trainer_list(batch = batch)
            else:
                set2 = []
            
            t = get_template('addedList2.html')
            c = Context({'list': set2 , 'batch':batch})
            return HttpResponse(t.render(c))
        else:
            t = get_template('addedList2.html')
            c = Context({'list': []})
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')    

@emp_auth_needed
def add_ttb(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        empid = request.GET['empid'].encode('ascii','ignore')
        batchid = request.GET['batchid'].encode('ascii','ignore') 
        batch = BatchDetails.objects.get(id = batchid)
        empl = EmployeeInfo.objects.get(id = empid)
        res  = functions.add_trainer_to_batch(employee = empl, batch = batch)
        return HttpResponse(res)
    else: 
        return HttpResponseRedirect("../../logout")

@emp_auth_needed    
def del_ttb(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    if emp is not None and (emp.is_Admin or emp.is_HOD or emp.is_manager):
        #nothing
        empid = request.GET['empid'].encode('ascii','ignore')
        batchid = request.GET['batchid'].encode('ascii','ignore') 
        batch = BatchDetails.objects.get(id = batchid)
        empl = EmployeeInfo.objects.get(id = empid)
        res  = functions.remove_trainer_from_batch(employee = empl, batch = batch)
        return HttpResponse(res)
    else: 
        return HttpResponseRedirect("../../logout")
    
""" ----------------------------------------------------------------------------------------------------------------------------------------""" 
def empIsToAttend(employee,course):
    try: 
        Users.models.CoursesToAttend.objects.get(employee = employee , course = course)
        return True
    except Users.models.CoursesToAttend.DoesNotExist:
        return False

       
@emp_auth_needed
@csrf_exempt
def course_emp_assignment(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        cond = 'n'
        courses = functions.getCourseList(emp)
        empList = userfunctions.getEmployeeList(emp)
        if request.POST:
            cond = 'y'
            for emplee in empList:
                for course in courses:
                    elem = request.POST.get(emplee.userId + course.course_id,'F').encode('ascii','ignore')
                    if(not empIsToAttend(emplee,course) and  elem == "true"):
                        rec = Users.models.CoursesToAttend(employee = emplee , course = course)
                        rec.save()
                    if(empIsToAttend(emplee,course) and  elem == 'F'):
                        rec = Users.models.CoursesToAttend.objects.get(employee = emplee , course = course)
                        rec.delete() 

        liste = []
        for empx in empList:
            empl = EmployeeCourseData(empx)
            coursedata = []
            for course in courses:
                 
                if(empIsToAttend(empx,course)):
                    coursedata.append(CourseData(course.course_id,empx.userId,'checked'))
                else:
                    coursedata.append(CourseData(course.course_id,empx.userId,''))
            empl.coursedata = coursedata
            liste.append(empl)          
    return render_to_response('courseEmployeeAssignment.html', {'list':liste , 'courses':courses ,'cond':cond})

@emp_auth_needed
def main_course_emp_assignment(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        t = get_template('maincourseEmployeeAssignment.html')
        c = Context({})
        return HttpResponse(t.render(c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def course_emp_assignemnt_details(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        courseid = request.GET['id'].encode('ascii','ignore')
        course = Course.objects.get(id = courseid )
        employeesl = list(Users.models.CoursesToAttend.objects.filter(course = course ))
        trainers = get_trainer_list(course = course)
        employees = []
        for employee in employeesl:
            employees.append(employee.employee)
        c = Context({'employees':employees,'trainers':trainers})
        t = get_template('cead.html')
        return HttpResponse(t.render(c))
    
    return HttpResponseRedirect('../../loggedin')



@emp_auth_needed 
def main_course_emp_assignemnt_details(request):
    courses = list(Course.objects.all()) 
    liste = []
    for course in courses:
        np = len(list(Users.models.CoursesToAttend.objects.filter(course = course)))
        nt = len(get_trainer_list(course = course))
        cad = CourseAssignmentData(course,np,nt)
        liste.append(cad)
    t = get_template('mcead.html')
    c = Context({'list':liste })
    return HttpResponse(t.render(c))


"""-----------------------------------------------------------------------------------------------------------------------------"""
@emp_auth_needed 
def view_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None 
    batchid = request.GET.get('batchid','').encode('ascii','ignore')
    batch = get_object_or_404(BatchDetails,id = batchid)
    if emp is not None and (userfunctions.authorised_to_handle(handler = emp , batch = batch )):

        t = get_template('batchDetails.html')
        c = Context({'item':batch})
        return HttpResponse(t.render(c))
    else:
        return HttpResponseForbidden("Get Lost.")


@emp_auth_needed 
def assign_batches(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        if request.POST:
            form = BatchForm(request.POST)
            if form.is_valid():
                batch = form.save()
                functions.add_deafult_trainers_to_batch(batch)
                t = get_template('batchAdded.html')
                c = Context({'batch':batch})
                return HttpResponse(t.render(c))
            else:
                c = Context({'form':form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
        else:
            form = BatchForm()
            c = Context({'form':form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def main_edit_batches(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        courses = functions.getCourseList(emp)
        t = get_template('mainEditBatch.html')
        now = datetime.now()
        years = range(2014, int(now.year) + 10)
        c = Context({'courses': courses,'years':years})
        return HttpResponse(t.render(c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed 
def list_edit_batches(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        courses = functions.getCourseList(emp)
        if request.GET:   
            course = Course.objects.get(id = request.GET['course'].encode('ascii','ignore'))
            year = request.GET.get('year','none').encode('ascii','ignore')
            alli = booleanize(request.GET.get('all','false').encode('ascii','ignore'))
            if not alli:
                batches = BatchDetails.objects.filter(course = course  ,course_finished = False)
            else:
                batches = BatchDetails.objects.filter(course__in =  courses )
            if year != 'none':
                batches = batches.filter(start_date__year = year )
            print batches
            t = get_template('batchList.html')
            c = Context({'list':batches})
            return HttpResponse(t.render(c))
        else:
            batches = BatchDetails.objects.filter( course_finished = False)
            t = get_template('batchList.html')
            print batches
            c = Context({'list':batches})
            return HttpResponse(t.render(c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def edit_batches(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        idt = request.GET.get('id','None').encode('ascii','ignore')
        if not idt == 'None':
            batch = BatchDetails.objects.get(id = idt)
            if not functions.authorise_batch_edit(batch,emp):
                return   HttpResponseForbidden() 
            if request.POST:
                form = BatchForm(request.POST,instance = batch)
                if  form.is_valid() and form.clean_with_emp(emp) :
                    batch = form.save()
                    t = get_template('batchAdded.html')
                    c = Context({'batch':batch})
                    return HttpResponse(t.render(c))
                else:
                    c = Context({'form':form})
                    return render_to_response('registration.html', context_instance=RequestContext(request,c))                
            else:
                form = BatchForm(instance = batch)
                c = Context({'form':form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def main_assign_employee_batch(request):
    batchid = request.GET['batchid'].encode('ascii','ignore')
    batch = BatchDetails.objects.get(id = batchid)
    t = get_template('assEmpToBatch.html')
    c = Context({'batch':batch})
    return HttpResponse(t.render(c)) 
    
@emp_auth_needed
def free_employees_for_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        
        if request.GET:
            
            userID = request.GET.get('userID','').encode('ascii','ignore')
            username = request.GET.get('username','').encode('ascii','ignore')
            first_name = request.GET.get('first_name','').encode('ascii','ignore')
            last_name = request.GET.get('last_name','').encode('ascii','ignore')
            batchid = request.GET.get('batchid','').encode('ascii','ignore')
            tempset = []
            try:
                batch = BatchDetails.objects.get(id = batchid)
            except Course.DoesNotExist:
                batch = None
            if batch is not None:
                set2 = functions.free_employees_for_batch(batch, emp)
            else:
                set2 = []
            print set2
            if(first_name == '' and  last_name == '' and  userID == '' and  username == '' and batch is not None ):
                c = Context({'list': set2,'batch':batch})
                t = get_template('addListBatch.html')
                return HttpResponse(t.render(c))
                
            if  not ( first_name == '' and  last_name == '' and  userID == '' and  username == '' and batch is not None  and set2  == []):
                if not first_name == '' :
                    for elem in set2:
                        if (elem.first_name.lower()).find(first_name.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not last_name == '':
                    for elem in set2:
                        if (elem.last_name.lower()).find(last_name.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                if not userID == '':
                    for elem in set2:
                        if (elem.userId.lower()).find(userID.lower()) >= 0 and determineAuthType(elem,emp)  :
                            tempset.append(elem)
                            set2.remove(elem)
                if not username == '':
                    for elem in set2:
                        if (elem.userObj.username.lower()).find(username.lower()) >= 0 and determineAuthType(elem,emp):
                            tempset.append(elem)
                            set2.remove(elem)
                
            else:
                tempset = []
            c = Context({'list': tempset ,'batch':batch})
            t = get_template('addListBatch.html')
            return HttpResponse(t.render(c))
        else:
            tempset = []
            c = Context({'list': tempset,'batch':batch})
            t = get_template('addListBatch.html')
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')

@emp_auth_needed    
def employees_of_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None   
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD): 
        if request.GET:
            batchid = request.GET['batchid'].encode('ascii','ignore')
            try:
                batch = BatchDetails.objects.get(id = batchid)
            except BatchDetails.DoesNotExist:
                batch = None
            if batch is not None:
                set2 = functions.employees_of_batch(batch, emp)
            else:
                set2 = []
            
            t = get_template('addedListBatch.html')
            c = Context({'list': set2 ,'batch':batch})
            return HttpResponse(t.render(c))
        else:
            t = get_template('addedListBatch.html')
            c = Context({'list': [] })
            return HttpResponse(t.render(c))
    else:
        return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')   
    
@emp_auth_needed
def add_employee_to_batch(request):
    emp = EmployeeInfo.objects.all().get(userObj = request.user )
    empl = EmployeeInfo.objects.get(id = request.GET['empid'].encode('ascii','ignore') )
    batch = BatchDetails.objects.get(id = request.GET['batchid'].encode('ascii','ignore') )
    if functions.add_employee(batch, empl, emp):
        return HttpResponse("The Employee was sucesfully added")
    else:
        return HttpResponse("We regret to inform you that the employee hasnt been added to the batch , contact the IT Admin")
    
@emp_auth_needed
def remove_employee_from_batch(request):
    emp = EmployeeInfo.objects.all().get(userObj = request.user )
    empl = EmployeeInfo.objects.get(id = request.GET['empid'].encode('ascii','ignore') )
    batch = BatchDetails.objects.get(id = request.GET['batchid'].encode('ascii','ignore') )
    if functions.remove_employee(batch, empl, emp):
        return HttpResponse("The Employee was sucesfully removed.")
    else:
        return HttpResponse("We regret to inform you that the employee hasnt been removed from the batch , contact the IT Admin.")
"""-------------------------------------------------------------------------------------------------------------------------------------"""
@emp_auth_needed
def start_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        batchid = request.GET['id'].encode('ascii','ignore')
        batch = BatchDetails.objects.get(id = batchid) 
        if not batch.course_ongoing and not batch.course_completed:
            functions.start_batch(batch, emp)  
            return HttpResponse("Batch Succesfully Started")
        else:
            return HttpResponse("The batch is done and dusted with, in case of a mistake contact the IT Administrator")  
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def stop_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        batchid = request.GET['id'].encode('ascii','ignore')
        batch = BatchDetails.objects.get(id = batchid) 
        if batch.course_ongoing and not batch.course_completed and not batch.course_finished:
            functions.stop_batch(batch, emp)  
            return HttpResponse("Batch sucesfully stopped")
        elif not batch.course_started:
            return HttpResponse("The batch has not yet started. Start the batch first , in case this is a mistake contact the IT Administrator")
        elif batch.course_finished:
            return HttpResponse("The batch is done and dusted with, in case of a mistake contact the IT Administrator")  
        else:
            return HttpResponse("Some error has occured , contact the IT Administrator") 
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def do_feedback(request):
    emp = EmployeeInfo.objects.all().get(userObj = request.user )
    batchid = request.GET.get('batchid','').encode('ascii','ignore')
    try:
        batch = BatchDetails.objects.get(id = batchid)
    except EmployeeInfo.DoesNotExist:
        batch = None
    empsInBatch = functions.employees_of_batch(batch, emp)
    formset = modelformset_factory(Feedback, form = FeedbackForm,max_num=len(empsInBatch), extra=1)
    if request.POST:
        forms = formset(request.POST)
        if forms.is_valid():
            list1 = forms.save()
            t = get_template('graded.html')
            c = Context({'list':list1 ,'grading': True})
            return HttpResponse(t.render(c))
        else:
            c = Context({'forms':forms})
            render_to_response('grading.html', context_instance=RequestContext(request,c))
    forms = formset(queryset = functions.get_feedback_query_set(batch, emp))
    c = Context({'forms':forms})
    return render_to_response('grading.html', context_instance=RequestContext(request,c))
@emp_auth_needed
def do_grading(request):
    emp = EmployeeInfo.objects.all().get(userObj = request.user )
    batchid = request.GET.get('batchid','').encode('ascii','ignore')
    try:
        batch = BatchDetails.objects.get(id = batchid)
    except EmployeeInfo.DoesNotExist:
        batch = None
    empsInBatch = functions.employees_of_batch(batch, emp)
    formset = modelformset_factory(Grading, form = GradingForm,max_num=len(empsInBatch), extra=1 )
    if request.POST:
        forms = formset(request.POST)
        if forms.is_valid():
            list1 = forms.save()
            print list1
            for form  in forms:
                print "Here"
                if form.cleaned_data['retraning_needed']:
                    CoursesToAttend.objects.create(course = form.cleaned_data['batch'].course , employee = form.cleaned_data['employee'])
            t = get_template('graded.html')
            c = Context({'list':list1})
            return HttpResponse(t.render(c))
        else:
            c = Context({'forms':forms})
            return render_to_response('grading.html', context_instance=RequestContext(request,c))
    forms = formset(queryset = functions.get_grading_query_set(batch, emp))
    c = Context({'forms':forms})
    return render_to_response('grading.html', context_instance=RequestContext(request,c))    
    
            
        

    
@emp_auth_needed
def complete_batch(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        batchid = request.GET['id'].encode('ascii','ignore')
        batch = BatchDetails.objects.get(id = batchid) 
        err = functions.complete_batch(batch, emp)
        print err
        if err == 0:
            return HttpResponse("The batch is finished.")
        elif err == 1:
            return HttpResponse("Grading is not for this batch")
        elif err ==2 :
            return HttpResponse("Feedback is not done for this batch")
        elif err == 3:
            return HttpResponse("Both Grading and feedback are not done for this batch")
        elif err == 4:
            return HttpResponse("Batch start not done")
        elif err == 5:
            return HttpResponse("Batch stop not done")
    return HttpResponseRedirect('../../loggedin')

    
    
@emp_auth_needed
def search_all_documents(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin ):
        documents = Files.objects.all().order_by('-created')
        message = "All The Documents"
        t = get_template('documentList.html')
        c = Context({'documents':documents,'message': message})
        return HttpResponse(t.render(c))
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def annual_training_calendars(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin ):
        """"""
        calendars = Files.objects.filter(name = "AC").order_by('-year')
        message = "All The Annual Calendars"
        t = get_template('documentList.html')
        c = Context({'documents':calendars,'message': message})
        return HttpResponse(t.render(c))
        
        
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def annual_training_calendar_template(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin ):
        if request.POST:
            form = YearForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                filee = functions.generate_calendar(year, emp)
                message = " Here is your template."
                doclist = [filee]
                t = get_template('documentList.html')
                c = Context({'documents':doclist,'message': message})
                return HttpResponse(t.render(c))
            else:
                c = Context({'form':form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
        else:
            form = YearForm()
            c = Context({'form':form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))           
        
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed
def indent_for_year(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin ):
        if request.POST:
            form = YearForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                filee = functions.generate_L4PA2(year, emp)
                message = " Here is your Indent."
                doclist = [filee]
                t = get_template('documentList.html')
                c = Context({'documents':doclist,'message': message})
                return HttpResponse(t.render(c))
            else:
                c = Context({'form':form})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
        else:
            form = YearForm()
            c = Context({'form':form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))           
        
    return HttpResponseRedirect('../../loggedin')
@emp_auth_needed 
def download_batch_documents(request):
    """
    L4PA1 - After Batches are assigned. Employee List for the Course , Batch Wise
    L4PA2 - In this Employees and HOD's apply for courses, Generation Of Annual Calendar
    l4PA3 - Attendance List,Batch Wise.
    L4PA5 - Programme Evaluation and Faculty Evaluation , Batch Wise.
    L4PA7 - Indivisual Training Record.
    L4PA9 - Grade the employees deaprtment wise per batch.
    Anuual Training Calendar - Create batches.
    """
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        idt = request.GET.get('id','none').encode('ascii','ignore')
        
        if idt != 'none':
            batch = BatchDetails.objects.get(id = idt )
            tempfiles = []
            files = functions.generateBatchFiles(batch,tempfiles,emp)
            t = get_template('documentList.html')
            message = "Download the batch documents."
            c = Context({'documents':files ,'message':message})
            return HttpResponse(t.render(c))
            
    return HttpResponseRedirect('../../loggedin')    

@emp_auth_needed
def upload_batch_documents(request):
    """
    L4PA1 - After Batches are assigned. Employee List for the Course , Batch Wise
    L4PA2 - In this Employees and HOD's apply for courses, Generation Of Annual Calendar
    l4PA3 - Attendance List,Batch Wise.
    L4PA5 - Programme Evaluation and Faculty Evaluation , Batch Wise.
    L4PA7 - Indivisual Training Record.
    L4PA9 - Grade the employees deaprtment wise per batch.
    Anuual Training Calendar - Create batches.
    """
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        FileFormSet = modelformset_factory(Courses.models.Files, form = FileForm )
        batchid = request.GET.get('id','none').encode('ascii','ignore')
        batch = BatchDetails.objects.get(id = batchid)
        formset = FileFormSet(queryset = batch.files.all() )

        if request.POST:
            
            formset = FileFormSet(request.POST,request.FILES)
            files = batch.files.all()
            if formset.is_valid():
                for form in formset:
                    filer = form.save(commit=False)
                    if filer.file:

                        try:
                            filer2 = files.get(id = filer.id)
                            
                            filer.save()
                            for entry in filer2.modifiedBy.all():
                                filer.modifiedBy.add(entry)
                            filer2.delete()
                            batch.files.add(filer)
                            batch.save()    
                        except Files.DoesNotExist:
                            filer.save()
                            batch.files.add(filer)
                            batch.save()
                        
                        filer.modifiedBy.add(emp)
                        filer.save()

                        
                message = "All the Files for the Batch("+  batch.course.course_name + "  , " + str(batch.start_date) + " now are"
                t = get_template('documentList.html')
                c = Context({'documents':batch.files.all(),'message': message})
                return HttpResponse(t.render(c))
            else:
                c = Context({'formset':formset})
                return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
        else:
            c = Context({'formset':formset})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
            
                
    return HttpResponseRedirect('../../loggedin')

@emp_auth_needed     
def upload_document(request,):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin or emp.is_Manager or emp.is_HOD):
        """"""
        if request.POST:
            form = FileForm(request.POST,request.FILES)
            if form.is_valid():
                record = form.save()
                record.modifiedBy.add(emp)
                record.save()
                url = record.file.url
                return HttpResponse("File Added Sucessfully Download it <a href = " + url + "> Here </a>" )
            else:
                c = Context({'form':form})
                return render_to_response('fileUploads.html', context_instance=RequestContext(request,c)) 
        else:
            form =  FileForm()
            c = Context({'form':form})
            return render_to_response('fileUploads.html', context_instance=RequestContext(request,c)) 
                
    return HttpResponseRedirect('../../loggedin')   

@emp_auth_needed
def edit_document(request):
    idt = request.GET['fileID'].encode('ascii','ignore')
    filer = get_object_or_404(Files, id=idt)
    if request.POST:
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            document = form.save()
            
            message = "The Edited Document."
            t = get_template('documentList.html')
            c= Context({'documents':[document],'message': message})  
            return HttpResponse(t.render(c))
        else:
            c = Context({'form':form})
            return render_to_response('registration.html', context_instance=RequestContext(request,c))
    else:
        form = FileForm(instance = filer)
        c = Context({'form':form})
        return render_to_response('registration.html', context_instance=RequestContext(request,c))

@emp_auth_needed    
def delete_document(request):
    idt = request.GET['fileID'].encode('ascii','ignore')
    filer = get_object_or_404(Files, id=idt)
    filer.delete()
    return HttpResponse("File Was Sucessfully Deleted")
    
"""-------------------------------------------------------------------------------------------------------------------------------------"""
# Grading and Feedback views
@emp_auth_needed   
def employee_list_reader(request):
    try:
        emp = EmployeeInfo.objects.all().get(userObj = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None  
    if emp is not None and (emp.is_Admin):
        """"""
        if request.POST:
            form = FileForm(request.POST,request.FILES)
            if form.is_valid():
                record = form.save()
                record.modifiedBy.add(emp)
                record.save()
                file_location = settings.MEDIA_ROOT.replace('\\','/') + "/" + record.file.name
                wl = userfunctions.create_workers_from_list(file_location, emp)
                t = get_template('employeesAdded.html')
                c = Context({'errors':wl.errors, 'employees':wl.empList})
                return HttpResponse(t.render(c) )
            else:
                c = Context({'form':form})
                return render_to_response('fileUploads.html', context_instance=RequestContext(request,c)) 
        else:
            form =  FileForm()
            c = Context({'form':form})
            return render_to_response('fileUploads.html', context_instance=RequestContext(request,c)) 
                
    return HttpResponseRedirect('../../loggedin')   
    
    
"""--------------------------------------------------------------------------------------------------------------------------------------"""
      


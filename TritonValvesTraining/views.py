'''
Created on May 27, 2014

@author: Arjun
'''
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponse
from Users.models import EmployeeInfo, Schedule
from django.utils.unittest.compatibility import wraps
from django.template.loader import get_template
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template.context import RequestContext, Context
import datetime



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

def main_page(request):
    t = get_template('mainPage.html')
    c = Context({})
    return HttpResponse(t.render(c))
   
def login(request):
    if not request.user.is_authenticated() :
        errors = ""
        if request.POST:
            userid = request.POST.get('userid','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=userid, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if request.GET:
                    return HttpResponseRedirect( request.GET['next'])
                return HttpResponseRedirect("../loggedin/")
            else:
                errors = "Invalid Username or Password"
                return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors}))
        else:
            return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors}))
        
    else:  
        return HttpResponseRedirect("../loggedin/")
 
@emp_auth_needed
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('../../../../login')


@emp_auth_needed 
def logged_in_page(request):
    try:
        emp = EmployeeInfo.objects.all().get(user = request.user )
    except EmployeeInfo.DoesNotExist:
        emp = None
    print request.user.get_profile().is_Admin
    request.session["username"] = request.user.username
    request.session["count1"] = 0
    request.session["count2"] = 0
    try:
        day_notifications = Schedule.objects.get(date = datetime.datetime.today())
        day_notifications = list(day_notifications.message.all())
        notifications = []
        for notification in day_notifications:
            notifications.append(notification.message)
    except Schedule.DoesNotExist:
        notifications = ["No Notifications Today."]
    if  emp is not None :
        t = get_template('adminPage.html')
        if emp.is_Admin:
            
            c = Context({'emp1':emp ,'Admin': True , 'first_name': emp.user.first_name , 'last_name': emp.user.last_name , 'notifications':notifications})
            c = RequestContext(request,c)
            return HttpResponse(t.render(c))
            
            
        elif emp.is_HOD:
            c = Context({'emp1':emp ,'HOD': True, 'first_name': emp.user.first_name , 'last_name': emp.user.last_name , 'notifications':notifications})
            c = RequestContext(request,c)
            return HttpResponse(t.render(c))
            
            
        elif emp.is_Manager:
            c = Context({'emp1':emp ,'Manager': True, 'first_name': emp.user.first_name , 'last_name': emp.user.last_name , 'notifications':notifications})
            c = RequestContext(request,c)
            return HttpResponse(t.render(c))
            
            
        else:    
            c = Context({'emp1':emp ,'Employee': True,'user':request.user})
            c = RequestContext(request,c)
            return HttpResponse(t.render(c))
            
            
    return HttpResponse('Employee Not Registered or Invalid <br> <a href = "../../logout" > Logout </a>')


""" ----------------------------------------------------------------------------------------------------------------------------------------""" 


        
        
        

                

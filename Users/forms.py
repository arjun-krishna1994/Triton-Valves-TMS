'''
Created on Jun 26, 2014

@author: Arjun
'''
from Users.models import EmployeeInfo, Department
from django import forms
from django.contrib.auth.models import User
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
"""
class DepartmentEmployeeForm(forms.ModelForm):
    class Meta:
        model = DepartmentEmployeeList
        exclude = ['employee']
 """       
class UserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(required = False)
    username = forms.CharField(help_text = "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.")
    password1 = forms.CharField(widget = forms.PasswordInput(),label = 'Password')
    password2 = forms.CharField(widget = forms.PasswordInput(),label = 'Password(Again for conformation)')
    email=forms.EmailField(help_text = "enter default@tritionvalaves.com if you dont have one")
    
    def clean_username(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise forms.ValidationError("This user exist already choose anpther username")
    
    
    
    def clean(self): # check if password 1 and password2 match each other
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
            if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
                raise forms.ValidationError("Passwords don't match each other")

        return self.cleaned_data
    def save(self): # create new user
        new_user = User.objects.create_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'],email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        return new_user

class EmployeeForm(forms.ModelForm ):
    class Meta:
        model = EmployeeInfo
        exclude = ['email','userObj','first_name','last_name','is_Admin' ,'is_HOD','is_Manager']
        
class ManagerForm(forms.ModelForm ):
    class Meta:
        model = EmployeeInfo
        exclude = ['email','userObj','first_name','last_name','is_Admin' ,'is_HOD','is_Manager','is_Staff']
        
class AdminForm(forms.ModelForm ):
    class Meta:
        model = EmployeeInfo
        exclude = ['email','userObj','first_name','last_name','is_Staff']
    
    
class HODForm(forms.ModelForm ):
    class Meta:
        model = EmployeeInfo
        exclude = ['email','userObj','first_name','last_name','is_Admin' ,'is_HOD','is_Staff']

class EmployeeEditForm(forms.ModelForm):
    def set_exclude(self,emp):
        if emp.is_Admin :
            self.fields['userObj'].widget = forms.widgets.HiddenInput()
        elif emp.is_HOD:
            self.fields['userObj'].widget = forms.widgets.HiddenInput()
            self.fields['is_HOD'].widget = forms.widgets.HiddenInput()
            self.fields['is_Admin'].widget = forms.widgets.HiddenInput()
        elif emp.is_Manager:
            self.fields['userObj'].widget = forms.widgets.HiddenInput()
            self.fields['is_HOD'].widget = forms.widgets.HiddenInput()
            self.fields['is_Admin'].widget = forms.widgets.HiddenInput()
            self.fields['is_Manager'].widget = forms.widgets.HiddenInput()
        else:
            self.fields['userObj'].widget = forms.widgets.HiddenInput()
            self.fields['email'].widget = forms.widgets.HiddenInput()
            self.fields['first_name'].widget = forms.widgets.HiddenInput()
            self.fields['last_name'].widget = forms.widgets.HiddenInput()
            self.fields['is_HOD'].widget = forms.widgets.HiddenInput()
            self.fields['is_Admin'].widget = forms.widgets.HiddenInput()
            self.fields['is_Manager'].widget = forms.widgets.HiddenInput()
        
    class Meta:
        model = EmployeeInfo   


class CourseData:
    def __init__(self,course_id,userID,checked):
        self.course_id = course_id
        self.userID = userID
        self.checked = checked

class EmployeeCourseData:
    def __init__(self,employee):
        self.emp = employee
        self.coursedata = None
        
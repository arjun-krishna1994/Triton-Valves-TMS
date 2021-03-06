'''
Created on Jun 26, 2014

@author: Arjun
'''
from django import forms
from Courses.models import Grading, Feedback, BatchDetails, Course, Files
from django.forms.extras.widgets import SelectDateWidget 
from Courses import variables
from Users import userfunctions
class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs) 
        instance = getattr(self, 'instance', None)
        if instance :
            self.fields['employee'].required = False
    class Meta:
        model = Feedback
        exclude = ['course','batch']    
        widgets = {'employee':forms.Select(attrs={'disabled':'disabled'})} 
    def clean_employee(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.employee
        else:
            return self.cleaned_data['employee']       

class GradingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GradingForm, self).__init__(*args, **kwargs) 
        instance = getattr(self, 'instance', None)
        if instance :
            self.fields['employee'].required = False  
            self.fields['batch'].required = False 
    class Meta:
        model = Grading
        widgets = {'probable_date_of_retraining':SelectDateWidget()  , 'employee':forms.Select(attrs={'disabled':'disabled'}) , 'batch':forms.Select(attrs={'disabled':'disabled'}) }
    def clean_employee(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.employee
        else:
            return self.cleaned_data['employee']  
    def clean_batch(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            print "here"
            return instance.batch
        else:
            return self.cleaned_data['batch']       
    def clean(self):
        cleaned_data = super(GradingForm, self).clean()
        if not cleaned_data['probable_date_of_retraining']:
            cleaned_data['probable_date_of_retraining'] = None
        return cleaned_data 
    

        
class YearForm(forms.Form):    
    year = forms.ChoiceField(widget = forms.Select, choices = variables.year_choices ,help_text= " Enter the year you want to see the document for.")

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        exclude = ['modifiedBy' , 'created' ,'updated' ]
        """
    def clean_file(self):
        filer = self.cleaned_data['file']
        name = filer.name
        if not (name[len(name)-3: len(name)] == 'xls' or name[len(name)-4: len(name)] == 'xlsx'):
            raise forms.ValidationError("Provide a valid excel File")
            return self.cleaned_data['file']"""
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        widgets = {'department':forms.CheckboxSelectMultiple()}
    def do_clean_department(self ,emp):
        if not emp.is_Admin:
            cleaned_data = super(CourseForm, self).clean()
            cleaned_data['department'] = [emp.department]
            
            


        
        
class CourseAssignmentData:
    def __init__(self,course,NoPeople,NoTrainers , batches = None):
        self.course = course
        self.np = NoPeople
        self.nt = NoTrainers  
        self.batches = batches
        
import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe

__all__ = ('SelectTimeWidget', 'SplitSelectDateTimeWidget')

# Attempt to match many time formats:
# Example: "12:34:56 P.M."  matches:
# ('12', '34', ':56', '56', 'P.M.', 'P', '.', 'M', '.')
# ('12', '34', ':56', '56', 'P.M.')
# Note that the colon ":" before seconds is optional, but only if seconds are omitted
time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'

RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4

class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second' 
    meridiem_field = '%s_meridiem'
    twelve_hr = False # Default to 24hr.
    
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        """
        self.attrs = attrs or {}
        
        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)
        
        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step) 
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24) 

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES]) 
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])
                    
                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None
                    

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
            
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)

        second_choices = [("%.2d"%i, "%.2d"%i) for i in self.seconds]
        local_attrs['id'] = self.second_field % id_
        select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
        output.append(select_html)
    
        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem gets selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute 
        s = data.get(self.second_field % name, 0) # second

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem is None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24 
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0
        
        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)
    
class BatchForm(forms.ModelForm):
    class Meta:
        model = BatchDetails
        widgets = {'start_date':SelectDateWidget() , 'stop_date': SelectDateWidget()  , 'start_time': SelectTimeWidget() , 'stop_time' : SelectTimeWidget() }
        fields = ['start_date','stop_date','course','venue' ,'start_time','stop_time']
    def clean_with_emp(self,emp):
        cleaned_data = super(BatchForm, self).clean()
        course = cleaned_data.get('course')
        if not course.department == emp.department and not course.department.deptID == 'ALL' :
            return False
        return True
    def save(self,*args,**kwargs):
        batch = super(BatchForm,self).save(*args,**kwargs)
        userfunctions.generate_notification(username = "Auto:", message = "Start The Batch for module " + batch.course.course_name +" on:" + str(batch.start_date), date = batch.start_date, accessLevel = 1 , code= "BST" + batch.id)
        userfunctions.generate_notification(username = "Auto:", message = "Stop The Batch for module " + batch.course.course_name +" on:" + str(batch.stop_date), date = batch.stop_date, accessLevel = 1)
        return batch
class CourseBatchForm(forms.ModelForm):

    class Meta:
        model = BatchDetails
        widgets = {'start_date':SelectDateWidget() , 'stop_date': SelectDateWidget()  , 'start_time': SelectTimeWidget() , 'stop_time' : SelectTimeWidget() }
        fields = ['start_date','stop_date','course','venue' ,'start_time','stop_time']
    def clean_with_emp(self,emp):
        cleaned_data = super(BatchForm, self).clean()
        course = cleaned_data.get('course')
        if not course.department == emp.department and not course.department.deptID == 'ALL' :
            return False
        return True
    def save(self,*args,**kwargs):
        batch = super(CourseBatchForm,self).save(*args,**kwargs)
        userfunctions.generate_notification(username = "Auto:", message = "Start The Batch for module " + batch.course.course_name +" on:" + str(batch.start_date), date = batch.start_date, accessLevel = 1)
        userfunctions.generate_notification(username = "Auto:", message = "Stop The Batch for module " + batch.course.course_name +" on:" + str(batch.stop_date), date = batch.stop_date, accessLevel = 1)
        return batch
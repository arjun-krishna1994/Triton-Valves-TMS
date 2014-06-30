from django.conf.urls import patterns, include, url
from TritonValvesTraining.views import login
from TritonValvesTraining import  settings
from Courses import views as cviews
from Users import views as uviews
from TritonValvesTraining.views import main_page
from TritonValvesTraining.views import logged_in_page
from TritonValvesTraining.views import logout
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TritonValvesTraining.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main_page),
    
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^loggedin/$', logged_in_page),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^registerUser/$', uviews.user_registration),
    url(r'^registerEmployee/$', uviews.employee_registration),
    url(r'^registerHOD/$', uviews.hod_registration),
    url(r'^registerManager/$', uviews.manager_registration),
    url(r'^registerAdmin/$', uviews.admin_registration),
    url(r'^createDepartment/$', uviews.create_department),
    url(r'^search/$', uviews.search_results),
    url(r'^searchPage/$', uviews.search_page),
    url(r'^editEmployee/$', uviews.employee_edit),
    url(r'^delEmployee/$', uviews.employee_delete),
    url(r'^searchDept/$', uviews.search_department),
    url(r'^editDept/$', uviews.edit_department),
    url(r'^delDept/$', uviews.delete_department),
    url(r'^createCourse/$', cviews.create_course),
    url(r'^searchCourse/$', cviews.search_course),
    url(r'^createBatches/$', cviews.create_batches_for_course),
    url(r'^editCourse/$', cviews.edit_course),
    url(r'^delCourse/$', cviews.delete_course),
  
    url(r'^ttcMain/$', cviews.add_ttc_main),
    url(r'^ttcEmpList/$', cviews.ttc_emp_list),
    url(r'^ttcTrainerList/$', cviews.ttc_trainer_list),
    url(r'^assttc/$', cviews.add_ttc),
    url(r'^delttc/$', cviews.del_ttc),
    url(r'^ttbMain/$', cviews.add_ttb_main),
    url(r'^ttbEmpList/$', cviews.ttb_emp_list),
    url(r'^ttbTrainerList/$', cviews.ttb_trainer_list),
    url(r'^assttb/$', cviews.add_ttb),
    url(r'^delttb/$', cviews.del_ttb),
    url(r'^maincea/$', cviews.main_course_emp_assignment),
    url(r'^cea/$', cviews.course_emp_assignment),
    url(r'^mcead/$', cviews.main_course_emp_assignemnt_details),
    url(r'^cead/$', cviews.course_emp_assignemnt_details),
    url(r'^assb/$', cviews.assign_batches),
    url(r'^essb/$', cviews.main_edit_batches),
    url(r'^searchEB/$', cviews.list_edit_batches),
    url(r'^editEB/$', cviews.edit_batches),
    url(r'^uploadFile/$', cviews.upload_document),
    url(r'^employeeListReader/$', cviews.employee_list_reader),
    url(r'^uploadBatchFiles/$', cviews.upload_batch_documents),
    url(r'^downBatchFiles/$', cviews.download_batch_documents),
    url(r'^searchFiles/$',cviews.search_all_documents),
    url(r'^editFile/$', cviews.edit_document),
    url(r'^delFile/$', cviews.delete_document),
    url(r'^viewCalendar/$', cviews.view_calendar),
    url(r'^batchFreeEmpList/$', cviews.free_employees_for_batch),
    url(r'^batchEmpList/$', cviews.employees_of_batch),
    url(r'^mainBatchEmpAssignment/$', cviews.main_assign_employee_batch),
    url(r'^assetb/$', cviews.add_employee_to_batch),
    url(r'^delefb/$', cviews.remove_employee_from_batch),
    url(r'^startBatch/$', cviews.start_batch),
    url(r'^stopBatch/$', cviews.stop_batch),
    url(r'^completeBatch/$', cviews.complete_batch),
    url(r'^doGrading/$', cviews.do_grading),
    url(r'^doFeedback/$', cviews.do_feedback),
    url(r'^viewBatch/$', cviews.view_batch),
    url(r'^viewEmployee/$', uviews.view_complete_emp),
    url(r'^getCalendarTemplate/$', cviews.annual_training_calendar_template),
    url(r'^indentGenerator/$', cviews.indent_for_year),
    url(r'^viewGF/$', uviews.view_emp_grades),
    url(r'^viewSchedule/$', uviews.generate_schedule),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

urlpatterns2 = patterns('',
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
    # ...
)
urlpatterns += urlpatterns2

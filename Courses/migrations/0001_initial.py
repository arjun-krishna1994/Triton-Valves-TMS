# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'Courses_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('course_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('objective', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('misc_Details', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('productivity', self.gf('django.db.models.fields.TextField')(null=True)),
            ('quality_improvement', self.gf('django.db.models.fields.TextField')(null=True)),
            ('reduction_time', self.gf('django.db.models.fields.TextField')(null=True)),
            ('others', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'Courses', ['Course'])

        # Adding M2M table for field department on 'Course'
        m2m_table_name = db.shorten_name(u'Courses_course_department')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'Courses.course'], null=False)),
            ('department', models.ForeignKey(orm[u'Users.department'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'department_id'])

        # Adding model 'BatchDetails'
        db.create_table(u'Courses_batchdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('actual_start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('stop_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('actual_stop_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('batch_timings', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.Course'])),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('course_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('course_ongoing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('course_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Courses', ['BatchDetails'])

        # Adding M2M table for field files on 'BatchDetails'
        m2m_table_name = db.shorten_name(u'Courses_batchdetails_files')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('batchdetails', models.ForeignKey(orm[u'Courses.batchdetails'], null=False)),
            ('files', models.ForeignKey(orm[u'Courses.files'], null=False))
        ))
        db.create_unique(m2m_table_name, ['batchdetails_id', 'files_id'])

        # Adding model 'Attendance'
        db.create_table(u'Courses_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.Course'])),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.BatchDetails'], null=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Users.EmployeeInfo'])),
            ('shift', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'Courses', ['Attendance'])

        # Adding model 'CourseEmployeeList'
        db.create_table(u'Courses_courseemployeelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.Course'])),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.BatchDetails'], null=True, blank=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Users.EmployeeInfo'])),
        ))
        db.send_create_signal(u'Courses', ['CourseEmployeeList'])

        # Adding model 'TrainerList'
        db.create_table(u'Courses_trainerlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.Course'])),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.BatchDetails'], null=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Users.EmployeeInfo'])),
        ))
        db.send_create_signal(u'Courses', ['TrainerList'])

        # Adding model 'Grading'
        db.create_table(u'Courses_grading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.BatchDetails'])),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Users.EmployeeInfo'])),
            ('pre_training', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=2, blank=True)),
            ('post_training', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=2, blank=True)),
            ('retraning_needed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('probable_date_of_retarining', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('misc_data', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'Courses', ['Grading'])

        # Adding model 'Feedback'
        db.create_table(u'Courses_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Courses.BatchDetails'], null=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Users.EmployeeInfo'])),
            ('expectations_met', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('reasons_not_met', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
            ('pre_training', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('post_training', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('training_methodology', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('use_of_AV_techniques', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('quality_of_courseMaterial', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('aoth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('opinion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subject_knowledge', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('presentation_skills', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('communication_skills', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('iwp', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('suggestions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Courses', ['Feedback'])

        # Adding model 'Files'
        db.create_table(u'Courses_files', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'Courses', ['Files'])

        # Adding M2M table for field modifiedBy on 'Files'
        m2m_table_name = db.shorten_name(u'Courses_files_modifiedBy')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('files', models.ForeignKey(orm[u'Courses.files'], null=False)),
            ('employeeinfo', models.ForeignKey(orm[u'Users.employeeinfo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['files_id', 'employeeinfo_id'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'Courses_course')

        # Removing M2M table for field department on 'Course'
        db.delete_table(db.shorten_name(u'Courses_course_department'))

        # Deleting model 'BatchDetails'
        db.delete_table(u'Courses_batchdetails')

        # Removing M2M table for field files on 'BatchDetails'
        db.delete_table(db.shorten_name(u'Courses_batchdetails_files'))

        # Deleting model 'Attendance'
        db.delete_table(u'Courses_attendance')

        # Deleting model 'CourseEmployeeList'
        db.delete_table(u'Courses_courseemployeelist')

        # Deleting model 'TrainerList'
        db.delete_table(u'Courses_trainerlist')

        # Deleting model 'Grading'
        db.delete_table(u'Courses_grading')

        # Deleting model 'Feedback'
        db.delete_table(u'Courses_feedback')

        # Deleting model 'Files'
        db.delete_table(u'Courses_files')

        # Removing M2M table for field modifiedBy on 'Files'
        db.delete_table(db.shorten_name(u'Courses_files_modifiedBy'))


    models = {
        u'Courses.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']", 'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shift': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'Courses.batchdetails': {
            'Meta': {'object_name': 'BatchDetails'},
            'actual_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'actual_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'batch_timings': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.Course']"}),
            'course_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course_ongoing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Courses.Files']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'Courses.course': {
            'Meta': {'object_name': 'Course'},
            'course_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'course_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'department': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Users.Department']", 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misc_Details': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'objective': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'others': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'productivity': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'quality_improvement': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reduction_time': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'Courses.courseemployeelist': {
            'Meta': {'object_name': 'CourseEmployeeList'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.Course']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Courses.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'aoth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']", 'null': 'True'}),
            'communication_skills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            'expectations_met': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iwp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'opinion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_training': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'pre_training': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'presentation_skills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quality_of_courseMaterial': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reasons_not_met': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'subject_knowledge': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'suggestions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'training_methodology': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'use_of_AV_techniques': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Courses.files': {
            'Meta': {'object_name': 'Files'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedBy': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Users.EmployeeInfo']", 'null': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'Courses.grading': {
            'Meta': {'object_name': 'Grading'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misc_data': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'post_training': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'pre_training': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'probable_date_of_retarining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retraning_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Courses.trainerlist': {
            'Meta': {'object_name': 'TrainerList'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']", 'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.Course']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Users.department': {
            'Meta': {'object_name': 'Department'},
            'deptID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'dept_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Users.employeeinfo': {
            'Meta': {'object_name': 'EmployeeInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'current_shift': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.Department']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'grade': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_Admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_HOD': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_Internal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_Manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'phone_Number': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'userId': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'userObj': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'working_Status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Courses']
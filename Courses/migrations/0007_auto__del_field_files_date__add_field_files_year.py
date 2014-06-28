# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Files.date'
        db.delete_column(u'Courses_files', 'date')

        # Adding field 'Files.year'
        db.add_column(u'Courses_files', 'year',
                      self.gf('django.db.models.fields.CharField')(default='2014', max_length=4),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Files.date'
        db.add_column(u'Courses_files', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 25, 0, 0)),
                      keep_default=False)

        # Deleting field 'Files.year'
        db.delete_column(u'Courses_files', 'year')


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
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Courses.Files']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'Courses.batchwisetrainer': {
            'Meta': {'object_name': 'BatchwiseTrainer'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'Courses.coursewisetrainer': {
            'Meta': {'object_name': 'CoursewiseTrainer'},
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
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'Courses.grading': {
            'Meta': {'object_name': 'Grading'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Courses.BatchDetails']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Users.EmployeeInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misc_data': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'post_training': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'pre_training': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'probable_date_of_retraining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retraning_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'grade': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_Admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_HOD': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_Internal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_Manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_Staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.surveygizmo_survey_id'
        db.add_column(u'monitor_project', 'surveygizmo_survey_id',
                      self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.surveygizmo_survey_id'
        db.delete_column(u'monitor_project', 'surveygizmo_survey_id')


    models = {
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
        },
        u'monitor.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'monitor.buzzartupdate': {
            'Meta': {'object_name': 'BuzzartUpdate'},
            'fa_class': ('django.db.models.fields.TextField', [], {'default': "'fa-check'", 'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'update': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'monitor.interestproject': {
            'Meta': {'object_name': 'InterestProject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interestAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nikiInterest.InterestAccount']"}),
            'nikiProjectId': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"})
        },
        u'monitor.project': {
            'Meta': {'object_name': 'Project'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fanpage_id': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'fanpage_token': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailchimp_api_token': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'mailchimp_list_id': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'nikiProject': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'surveygizmo_survey_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'monitor.summary': {
            'Meta': {'object_name': 'Summary'},
            'availability_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'conversion_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dateEnd': ('django.db.models.fields.DateField', [], {}),
            'dateStart': ('django.db.models.fields.DateField', [], {}),
            'facebook_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mail_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mailchimp_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'traffic_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'nikiInterest.interestaccount': {
            'Meta': {'object_name': 'InterestAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdate': ('django.db.models.fields.DateTimeField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['monitor']
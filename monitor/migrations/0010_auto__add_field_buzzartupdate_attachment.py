# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BuzzartUpdate.attachment'
        db.add_column(u'monitor_buzzartupdate', 'attachment',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BuzzartUpdate.attachment'
        db.delete_column(u'monitor_buzzartupdate', 'attachment')


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
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'accounts'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'monitor.buzzartupdate': {
            'Meta': {'object_name': 'BuzzartUpdate'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fa_class': ('django.db.models.fields.TextField', [], {'default': "u'fa-check'", 'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'update': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'monitor.buzzcache': {
            'Meta': {'object_name': 'BuzzCache'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
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
            'fanpage_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'fanpage_token': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailchimp_api_token': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'mailchimp_list_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'nikiProject': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'surveygizmo_survey_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'template': ('relativefilepathfield.fields.RelativeFilePathField', [], {'default': "u''", 'path': "u'/home/hz/projects/buzzart/dashboard/templates'", 'max_length': '100', 'recursive': 'True'}),
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
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SurveyGizmoAccount'
        db.create_table(u'surveygizmo_surveygizmoaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('password', self.gf('django.db.models.fields.TextField')(max_length=300)),
        ))
        db.send_create_signal(u'surveygizmo', ['SurveyGizmoAccount'])


    def backwards(self, orm):
        # Deleting model 'SurveyGizmoAccount'
        db.delete_table(u'surveygizmo_surveygizmoaccount')


    models = {
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
        u'surveygizmo.surveygizmoaccount': {
            'Meta': {'object_name': 'SurveyGizmoAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['surveygizmo']
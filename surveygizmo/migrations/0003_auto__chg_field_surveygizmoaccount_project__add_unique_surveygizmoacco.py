# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SurveyGizmoAccount.project'
        db.alter_column(u'surveygizmo_surveygizmoaccount', 'project_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['monitor.Project'], unique=True))
        # Adding unique constraint on 'SurveyGizmoAccount', fields ['project']
        db.create_unique(u'surveygizmo_surveygizmoaccount', ['project_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SurveyGizmoAccount', fields ['project']
        db.delete_unique(u'surveygizmo_surveygizmoaccount', ['project_id'])


        # Changing field 'SurveyGizmoAccount.project'
        db.alter_column(u'surveygizmo_surveygizmoaccount', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project']))

    models = {
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
            'template': ('relativefilepathfield.fields.RelativeFilePathField', [], {'default': "''", 'path': "'/home/hz/projects/buzzart/dashboard/templates'", 'max_length': '100', 'recursive': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'surveygizmo.surveygizmoaccount': {
            'Meta': {'object_name': 'SurveyGizmoAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monitor.Project']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['surveygizmo']
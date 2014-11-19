# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AnalyticsSettings'
        db.create_table(u'googleAnalytics_analyticssettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project'])),
            ('sessions_target', self.gf('django.db.models.fields.IntegerField')()),
            ('pageviews_target', self.gf('django.db.models.fields.IntegerField')()),
            ('ga_view', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('goal_to_track', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'googleAnalytics', ['AnalyticsSettings'])


    def backwards(self, orm):
        # Deleting model 'AnalyticsSettings'
        db.delete_table(u'googleAnalytics_analyticssettings')


    models = {
        u'googleAnalytics.analyticssettings': {
            'Meta': {'object_name': 'AnalyticsSettings'},
            'ga_view': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'goal_to_track': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pageviews_target': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'sessions_target': ('django.db.models.fields.IntegerField', [], {})
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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['googleAnalytics']
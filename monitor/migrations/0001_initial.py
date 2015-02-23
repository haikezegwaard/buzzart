# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'monitor_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('nikiProject', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('mailchimp_list_id', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('mailchimp_api_token', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('fanpage_id', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('fanpage_token', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'monitor', ['Project'])

        # Adding model 'InterestProject'
        db.create_table(u'monitor_interestproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project'])),
            ('nikiProjectId', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('interestAccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nikiInterest.InterestAccount'])),
        ))
        db.send_create_signal(u'monitor', ['InterestProject'])

        # Adding model 'Summary'
        db.create_table(u'monitor_summary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project'])),
            ('introduction', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('traffic_advice', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('availability_advice', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('facebook_advice', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mailchimp_advice', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conversion_advice', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('dateStart', self.gf('django.db.models.fields.DateField')()),
            ('dateEnd', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'monitor', ['Summary'])

        # Adding model 'BuzzartUpdate'
        db.create_table(u'monitor_buzzartupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.Project'])),
            ('update', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fa_class', self.gf('django.db.models.fields.TextField')(default='fa-check', max_length=1000)),
        ))
        db.send_create_signal(u'monitor', ['BuzzartUpdate'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'monitor_project')

        # Deleting model 'InterestProject'
        db.delete_table(u'monitor_interestproject')

        # Deleting model 'Summary'
        db.delete_table(u'monitor_summary')

        # Deleting model 'BuzzartUpdate'
        db.delete_table(u'monitor_buzzartupdate')


    models = {
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
            'mailchimp_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.Project']"}),
            'traffic_advice': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
       # u'nikiInterest.interestaccount': {
       #     'Meta': {'object_name': 'InterestAccount'},
       #     u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
       #     'lastUpdate': ('django.db.models.fields.DateTimeField', [], {}),
       #     'password': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
       #     'username': ('django.db.models.fields.CharField', [], {'max_length': '400'})
       # }
    }

    complete_apps = ['monitor']
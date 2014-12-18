# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Summary.mail_sent'
        db.add_column(u'monitor_summary', 'mail_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Summary.mail_sent'
        db.delete_column(u'monitor_summary', 'mail_sent')


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
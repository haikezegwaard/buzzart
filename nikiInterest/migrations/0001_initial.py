# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InterestAccount'
        db.create_table(u'nikiInterest_interestaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('lastUpdate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'nikiInterest', ['InterestAccount'])


    def backwards(self, orm):
        # Deleting model 'InterestAccount'
        db.delete_table(u'nikiInterest_interestaccount')


    models = {
        u'nikiInterest.interestaccount': {
            'Meta': {'object_name': 'InterestAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdate': ('django.db.models.fields.DateTimeField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['nikiInterest']
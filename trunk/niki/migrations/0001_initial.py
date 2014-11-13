# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'niki_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'niki', ['Account'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'niki_account')


    models = {
        u'niki.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['niki']
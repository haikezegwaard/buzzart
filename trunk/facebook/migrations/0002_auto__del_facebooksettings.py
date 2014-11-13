# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FacebookSettings'
        db.delete_table(u'facebook_facebooksettings')


    def backwards(self, orm):
        # Adding model 'FacebookSettings'
        db.create_table(u'facebook_facebooksettings', (
            ('app_secret', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=400)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'facebook', ['FacebookSettings'])


    models = {
        
    }

    complete_apps = ['facebook']
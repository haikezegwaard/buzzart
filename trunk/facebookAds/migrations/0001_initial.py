# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacebookAdsSettings'
        db.create_table(u'facebookAds_facebookadssettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'facebookAds', ['FacebookAdsSettings'])


    def backwards(self, orm):
        # Deleting model 'FacebookAdsSettings'
        db.delete_table(u'facebookAds_facebookadssettings')


    models = {
        u'facebookAds.facebookadssettings': {
            'Meta': {'object_name': 'FacebookAdsSettings'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['facebookAds']
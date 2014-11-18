# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FacebookAdsSettings.expires'
        db.add_column(u'facebookAds_facebookadssettings', 'expires',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 18, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FacebookAdsSettings.expires'
        db.delete_column(u'facebookAds_facebookadssettings', 'expires')


    models = {
        u'facebookAds.facebookadssettings': {
            'Meta': {'object_name': 'FacebookAdsSettings'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['facebookAds']
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IPNRecord'
        db.create_table('paypal_ipnrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('created_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('paypal', ['IPNRecord'])


    def backwards(self, orm):
        
        # Deleting model 'IPNRecord'
        db.delete_table('paypal_ipnrecord')


    models = {
        'paypal.ipnrecord': {
            'Meta': {'object_name': 'IPNRecord'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['paypal']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Message.sent_ts'
        db.add_column('mail_message', 'sent_ts', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Message.sent_ts'
        db.delete_column('mail_message', 'sent_ts')


    models = {
        'mail.message': {
            'Meta': {'object_name': 'Message'},
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'failed_send_attempts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'max_send_attempts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'scheduled_delivery': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sent_ts': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'to_email': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['mail']

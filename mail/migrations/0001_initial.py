# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Message'
        db.create_table('mail_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('from_email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('body_text', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('scheduled_delivery', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('failed_send_attempts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('max_send_attempts', self.gf('django.db.models.fields.PositiveIntegerField')(default=3)),
            ('created_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('logs', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mail', ['Message'])


    def backwards(self, orm):
        
        # Deleting model 'Message'
        db.delete_table('mail_message')


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
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'to_email': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['mail']

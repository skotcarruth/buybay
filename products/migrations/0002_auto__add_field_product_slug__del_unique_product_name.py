# encoding: utf-8
import datetime
import uuid
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Product.slug'
        db.add_column('products_product', 'slug', self.gf('django.db.models.fields.SlugField')(default=lambda: uuid.uuid4().hex, unique=True, max_length=100, db_index=True), keep_default=False)

        # Removing unique constraint on 'Product', fields ['name']
        db.delete_unique('products_product', ['name'])


    def backwards(self, orm):
        
        # Deleting field 'Product.slug'
        db.delete_column('products_product', 'slug')

        # Adding unique constraint on 'Product', fields ['name']
        db.create_unique('products_product', ['name'])


    models = {
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'offer_end': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['products']

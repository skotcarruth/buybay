# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Order.user_shiptostreet2'
        db.add_column('orders_order', 'user_shiptostreet2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Order.user_shiptostreet2'
        db.delete_column('orders_order', 'user_shiptostreet2')


    models = {
        'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'galleries.gallerymedia': {
            'Meta': {'object_name': 'GalleryMedia'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paypal_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'paypal_details_dump': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paypal_feeamt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'paypal_ordertime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paypal_payment_dump': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paypal_paymentstatus': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'paypal_paymenttype': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'paypal_settleamt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'paypal_taxamt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'paypal_transactionid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Product']", 'through': "orm['orders.ProductInOrder']", 'symmetrical': 'False'}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user_firstname': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'user_lastname': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'user_middlename': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'user_salutation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user_shiptocity': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'user_shiptocountrycode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'user_shiptoname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user_shiptophonenum': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user_shiptostate': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'user_shiptostreet': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_shiptostreet2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_shiptozip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user_suffix': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'})
        },
        'orders.productinorder': {
            'Meta': {'unique_together': "(('order', 'product'),)", 'object_name': 'ProductInOrder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False'}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'offer_end': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']

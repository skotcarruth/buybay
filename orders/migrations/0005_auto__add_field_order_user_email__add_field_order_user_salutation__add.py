# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Order.user_email'
        db.add_column('orders_order', 'user_email', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Order.user_salutation'
        db.add_column('orders_order', 'user_salutation', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Order.user_firstname'
        db.add_column('orders_order', 'user_firstname', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Adding field 'Order.user_middlename'
        db.add_column('orders_order', 'user_middlename', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Adding field 'Order.user_lastname'
        db.add_column('orders_order', 'user_lastname', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Adding field 'Order.user_suffix'
        db.add_column('orders_order', 'user_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptoname'
        db.add_column('orders_order', 'user_shiptoname', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptostreet'
        db.add_column('orders_order', 'user_shiptostreet', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptocity'
        db.add_column('orders_order', 'user_shiptocity', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptostate'
        db.add_column('orders_order', 'user_shiptostate', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptozip'
        db.add_column('orders_order', 'user_shiptozip', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptocountrycode'
        db.add_column('orders_order', 'user_shiptocountrycode', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True), keep_default=False)

        # Adding field 'Order.user_shiptophonenum'
        db.add_column('orders_order', 'user_shiptophonenum', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Order.paypal_transactionid'
        db.add_column('orders_order', 'paypal_transactionid', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Adding field 'Order.paypal_paymenttype'
        db.add_column('orders_order', 'paypal_paymenttype', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True), keep_default=False)

        # Adding field 'Order.paypal_ordertime'
        db.add_column('orders_order', 'paypal_ordertime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Order.paypal_amt'
        db.add_column('orders_order', 'paypal_amt', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Order.paypal_feeamt'
        db.add_column('orders_order', 'paypal_feeamt', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Order.paypal_settleamt'
        db.add_column('orders_order', 'paypal_settleamt', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Order.paypal_taxamt'
        db.add_column('orders_order', 'paypal_taxamt', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Order.paypal_paymentstatus'
        db.add_column('orders_order', 'paypal_paymentstatus', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Adding field 'Order.paypal_details_dump'
        db.add_column('orders_order', 'paypal_details_dump', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Order.paypal_payment_dump'
        db.add_column('orders_order', 'paypal_payment_dump', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Order.user_email'
        db.delete_column('orders_order', 'user_email')

        # Deleting field 'Order.user_salutation'
        db.delete_column('orders_order', 'user_salutation')

        # Deleting field 'Order.user_firstname'
        db.delete_column('orders_order', 'user_firstname')

        # Deleting field 'Order.user_middlename'
        db.delete_column('orders_order', 'user_middlename')

        # Deleting field 'Order.user_lastname'
        db.delete_column('orders_order', 'user_lastname')

        # Deleting field 'Order.user_suffix'
        db.delete_column('orders_order', 'user_suffix')

        # Deleting field 'Order.user_shiptoname'
        db.delete_column('orders_order', 'user_shiptoname')

        # Deleting field 'Order.user_shiptostreet'
        db.delete_column('orders_order', 'user_shiptostreet')

        # Deleting field 'Order.user_shiptocity'
        db.delete_column('orders_order', 'user_shiptocity')

        # Deleting field 'Order.user_shiptostate'
        db.delete_column('orders_order', 'user_shiptostate')

        # Deleting field 'Order.user_shiptozip'
        db.delete_column('orders_order', 'user_shiptozip')

        # Deleting field 'Order.user_shiptocountrycode'
        db.delete_column('orders_order', 'user_shiptocountrycode')

        # Deleting field 'Order.user_shiptophonenum'
        db.delete_column('orders_order', 'user_shiptophonenum')

        # Deleting field 'Order.paypal_transactionid'
        db.delete_column('orders_order', 'paypal_transactionid')

        # Deleting field 'Order.paypal_paymenttype'
        db.delete_column('orders_order', 'paypal_paymenttype')

        # Deleting field 'Order.paypal_ordertime'
        db.delete_column('orders_order', 'paypal_ordertime')

        # Deleting field 'Order.paypal_amt'
        db.delete_column('orders_order', 'paypal_amt')

        # Deleting field 'Order.paypal_feeamt'
        db.delete_column('orders_order', 'paypal_feeamt')

        # Deleting field 'Order.paypal_settleamt'
        db.delete_column('orders_order', 'paypal_settleamt')

        # Deleting field 'Order.paypal_taxamt'
        db.delete_column('orders_order', 'paypal_taxamt')

        # Deleting field 'Order.paypal_paymentstatus'
        db.delete_column('orders_order', 'paypal_paymentstatus')

        # Deleting field 'Order.paypal_details_dump'
        db.delete_column('orders_order', 'paypal_details_dump')

        # Deleting field 'Order.paypal_payment_dump'
        db.delete_column('orders_order', 'paypal_payment_dump')


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

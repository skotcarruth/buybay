# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('products_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('created_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('products', ['Tag'])

        # Deleting field 'Product.offer_end'
        db.delete_column('products_product', 'offer_end')

        # Deleting field 'Product.is_active'
        db.delete_column('products_product', 'is_active')

        # Adding field 'Product.design'
        db.add_column('products_product', 'design', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Product.related_info_1'
        db.add_column('products_product', 'related_info_1', self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True), keep_default=False)

        # Adding field 'Product.related_info_2'
        db.add_column('products_product', 'related_info_2', self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True), keep_default=False)

        # Adding field 'Product.related_info_3'
        db.add_column('products_product', 'related_info_3', self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True), keep_default=False)

        # Adding field 'Product.min_quantity'
        db.add_column('products_product', 'min_quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)

        # Adding field 'Product.max_quantity'
        db.add_column('products_product', 'max_quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=10), keep_default=False)

        # Adding field 'Product.current_quantity'
        db.add_column('products_product', 'current_quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Product.main_image_1'
        db.add_column('products_product', 'main_image_1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Product.main_image_2'
        db.add_column('products_product', 'main_image_2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Product.status'
        db.add_column('products_product', 'status', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding M2M table for field tags on 'Product'
        db.create_table('products_product_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['products.product'], null=False)),
            ('tag', models.ForeignKey(orm['products.tag'], null=False))
        ))
        db.create_unique('products_product_tags', ['product_id', 'tag_id'])

        # Changing field 'Product.description'
        db.alter_column('products_product', 'description', self.gf('django.db.models.fields.TextField')(blank=True))


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('products_tag')

        # Adding field 'Product.offer_end'
        db.add_column('products_product', 'offer_end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 8, 8, 9, 35, 27, 890541)), keep_default=False)

        # Adding field 'Product.is_active'
        db.add_column('products_product', 'is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Deleting field 'Product.design'
        db.delete_column('products_product', 'design')

        # Deleting field 'Product.related_info_1'
        db.delete_column('products_product', 'related_info_1')

        # Deleting field 'Product.related_info_2'
        db.delete_column('products_product', 'related_info_2')

        # Deleting field 'Product.related_info_3'
        db.delete_column('products_product', 'related_info_3')

        # Deleting field 'Product.min_quantity'
        db.delete_column('products_product', 'min_quantity')

        # Deleting field 'Product.max_quantity'
        db.delete_column('products_product', 'max_quantity')

        # Deleting field 'Product.current_quantity'
        db.delete_column('products_product', 'current_quantity')

        # Deleting field 'Product.main_image_1'
        db.delete_column('products_product', 'main_image_1')

        # Deleting field 'Product.main_image_2'
        db.delete_column('products_product', 'main_image_2')

        # Deleting field 'Product.status'
        db.delete_column('products_product', 'status')

        # Removing M2M table for field tags on 'Product'
        db.delete_table('products_product_tags')

        # Changing field 'Product.description'
        db.alter_column('products_product', 'description', self.gf('django.db.models.fields.TextField')())


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
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False'}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'design': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image_1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_image_2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'min_quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'related_info_1': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'related_info_2': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'related_info_3': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['products']

# Generated by Django 3.2.3 on 2021-07-11 06:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='title',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]

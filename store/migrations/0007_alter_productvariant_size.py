# Generated by Django 3.2.3 on 2021-07-12 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210711_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='size',
            field=models.ForeignKey(blank=True, default='One Size', null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.size'),
        ),
    ]

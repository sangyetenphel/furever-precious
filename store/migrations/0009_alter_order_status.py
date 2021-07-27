# Generated by Django 3.2.3 on 2021-07-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210715_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Awaiting Payment', 'Awaiting Payment'), ('Paid', 'Paid'), ('On Shipping', 'On Shipping'), ('Completed', 'Completed'), ('Payment Failed', 'Payment Failed'), ('Cancelled', 'Cancelled')], max_length=20),
        ),
    ]

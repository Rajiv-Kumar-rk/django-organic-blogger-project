# Generated by Django 3.2.5 on 2022-11-15 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0002_auto_20221113_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='upadte_date',
            new_name='update_date',
        ),
    ]

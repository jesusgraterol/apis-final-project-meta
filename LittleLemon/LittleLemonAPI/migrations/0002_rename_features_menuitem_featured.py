# Generated by Django 5.0.2 on 2024-02-22 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='features',
            new_name='featured',
        ),
    ]

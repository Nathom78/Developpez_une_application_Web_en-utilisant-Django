# Generated by Django 4.1.7 on 2023-03-14 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_myuser_groups_myuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'permissions': [('see_all', 'Can see all tickets and reviews')]},
        ),
    ]
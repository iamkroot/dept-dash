# Generated by Django 3.0b1 on 2019-11-03 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_department_faculty_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'default_related_name': 'faculties', 'verbose_name': 'faculty', 'verbose_name_plural': 'faculties'},
        ),
        migrations.RemoveField(
            model_name='student',
            name='dept',
        ),
    ]
# Generated by Django 3.1.6 on 2021-02-05 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_question_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Answer',
        ),
    ]

# Generated by Django 4.0 on 2021-12-15 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0007_meetings_thesis_viva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viva',
            name='cv_status',
            field=models.CharField(max_length=20),
        ),
    ]

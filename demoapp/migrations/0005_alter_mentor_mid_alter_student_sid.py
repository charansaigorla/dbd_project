# Generated by Django 4.0 on 2021-12-12 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0004_alter_mentor_mid_alter_student_sid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='mid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='sid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]

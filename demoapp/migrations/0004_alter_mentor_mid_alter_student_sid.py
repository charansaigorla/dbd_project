# Generated by Django 4.0 on 2021-12-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0003_remove_mentor_id_alter_mentor_mid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='mid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='sid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
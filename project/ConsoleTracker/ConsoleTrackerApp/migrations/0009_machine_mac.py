# Generated by Django 3.2.8 on 2022-03-02 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConsoleTrackerApp', '0008_alter_machine_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='mac',
            field=models.CharField(default='00:00:00:00:00:00', max_length=17, unique=True),
        ),
    ]

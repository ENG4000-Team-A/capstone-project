# Generated by Django 4.0.2 on 2022-02-04 05:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ConsoleTrackerApp', '0007_machine_machine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

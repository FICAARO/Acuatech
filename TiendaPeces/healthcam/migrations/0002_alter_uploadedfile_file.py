# Generated by Django 5.0.3 on 2024-03-18 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='fishdiases'),
        ),
    ]
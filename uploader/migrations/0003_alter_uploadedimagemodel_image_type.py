# Generated by Django 5.1.6 on 2025-02-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_alter_uploadedimagemodel_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimagemodel',
            name='image_type',
            field=models.CharField(choices=[], default='portrait', max_length=10),
        ),
    ]

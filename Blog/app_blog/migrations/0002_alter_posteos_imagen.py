# Generated by Django 4.0.4 on 2022-07-03 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posteos',
            name='imagen',
            field=models.ImageField(upload_to='media/', verbose_name='Imagen'),
        ),
    ]

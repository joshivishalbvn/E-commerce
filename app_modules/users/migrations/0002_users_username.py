# Generated by Django 5.1.1 on 2024-10-04 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(blank=True, null=True),
        ),
    ]

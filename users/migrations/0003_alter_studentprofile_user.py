# Generated by Django 3.2 on 2021-04-30 02:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_studentprofile_student_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
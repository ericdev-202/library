# Generated by Django 3.2 on 2022-09-29 19:17

from django.db import migrations, models
import lmsApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_publisher',
            new_name='is_member',
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expiry_date',
            field=models.DateField(default=lmsApp.models.expiry),
        ),
    ]
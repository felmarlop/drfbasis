# Generated by Django 4.1.1 on 2022-11-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_alt_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='alt_name',
            field=models.CharField(default='master', help_text='Alternative name', max_length=25, unique=True),
        ),
    ]
# Generated by Django 4.1.1 on 2022-11-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_alter_entity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='id',
            field=models.UUIDField(default='f98077a3c00648129c6812d554fd506e', editable=False, primary_key=True, serialize=False),
        ),
    ]
# Generated by Django 4.1.1 on 2022-11-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0012_alter_entity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='id',
            field=models.UUIDField(default='be0572e03fbf488c8e233f83be87f50d', editable=False, primary_key=True, serialize=False),
        ),
    ]

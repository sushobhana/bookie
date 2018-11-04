# Generated by Django 2.1.2 on 2018-11-03 18:27

import book.models
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_usersbook_pending_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('NON-EDUCATIONAL', 'NON-EDUCATIONAL'), ('EDUCATIONAL', 'EDUCATIONAL')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(blank=True, choices=[('NON-EDUCATIONAL', 'NON-EDUCATIONAL'), ('EDUCATIONAL', 'EDUCATIONAL')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersbook',
            name='pending_request',
            field=book.models.IntegerRangeField(default=0),
        ),
    ]

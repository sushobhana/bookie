# Generated by Django 2.1.2 on 2018-11-03 18:31

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20181103_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('EDUCATIONAL', 'EDUCATIONAL'), ('NON-EDUCATIONAL', 'NON-EDUCATIONAL')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(blank=True, choices=[('DRAMA', 'DRAMA'), ('NON-EDUCATIONAL', 'NON-EDUCATIONAL'), ('COMEDY', 'COMEDY'), ('FICTION', 'FICTION'), ('EDUCATIONAL', 'EDUCATIONAL'), ('THRILLER', 'THRILLER')], max_length=100, null=True),
        ),
    ]
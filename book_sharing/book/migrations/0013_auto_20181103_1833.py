# Generated by Django 2.1.2 on 2018-11-03 18:33

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_auto_20181103_1832'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tags',
        ),
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('NON-EDUCATIONAL', 'NON-EDUCATIONAL'), ('DRAMA', 'DRAMA'), ('EDUCATIONAL', 'EDUCATIONAL'), ('FICTION', 'FICTION'), ('COMEDY', 'COMEDY'), ('THRILLER', 'THRILLER')], max_length=50, null=True),
        ),
    ]

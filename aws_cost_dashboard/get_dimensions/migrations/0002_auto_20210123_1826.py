# Generated by Django 3.0.5 on 2021-01-23 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_dimensions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='value',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
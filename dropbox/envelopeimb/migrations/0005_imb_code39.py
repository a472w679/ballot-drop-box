# Generated by Django 5.1.6 on 2025-02-11 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envelopeimb', '0004_imb_dropboxid'),
    ]

    operations = [
        migrations.AddField(
            model_name='imb',
            name='code39',
            field=models.CharField(default='012345678', max_length=44),
            preserve_default=False,
        ),
    ]

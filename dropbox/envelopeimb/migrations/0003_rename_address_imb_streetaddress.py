# Generated by Django 5.1.6 on 2025-02-10 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('envelopeimb', '0002_rename_member_imb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imb',
            old_name='address',
            new_name='streetaddress',
        ),
    ]

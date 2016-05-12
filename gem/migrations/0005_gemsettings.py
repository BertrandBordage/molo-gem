# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('gem', '0003_remove_gemuserprofile_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='GemSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banned_keywords_and_patterns', models.TextField(help_text=b'Banned keywords and patterns for comments, separated by a line a break.', null=True, verbose_name=b'Banned Keywords and Patterns', blank=True)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

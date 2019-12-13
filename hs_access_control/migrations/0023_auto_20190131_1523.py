# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 15:23


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hs_access_control', '0022_resourceaccess_require_download_agreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('purpose', models.TextField(blank=True, null=True)),
                ('auto_approve', models.BooleanField(default=False, editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=b'community')),
            ],
        ),
        migrations.CreateModel(
            name='GroupCommunityPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.IntegerField(choices=[(1, b'Owner'), (2, b'Change'), (3, b'View')], default=3, editable=False)),
                ('start', models.DateTimeField(auto_now=True)),
                ('allow_view', models.BooleanField(default=True, editable=False, help_text=b"whether to allow view for group's resources")),
                ('community', models.ForeignKey(editable=False, help_text=b'community to be granted privilege', on_delete=django.db.models.deletion.CASCADE, related_name='c2gcp', to='hs_access_control.Community')),
                ('grantor', models.ForeignKey(editable=False, help_text=b'grantor of privilege', on_delete=django.db.models.deletion.CASCADE, related_name='x2swp', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(editable=False, help_text=b'group providing privilege', on_delete=django.db.models.deletion.CASCADE, related_name='g2gcp', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupCommunityProvenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.IntegerField(choices=[(1, b'Owner'), (2, b'Change'), (3, b'View')], default=3, editable=False)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('undone', models.BooleanField(default=False, editable=False)),
                ('community', models.ForeignKey(editable=False, help_text=b'group to be granted privilege', on_delete=django.db.models.deletion.CASCADE, related_name='c2gcq', to='hs_access_control.Community')),
                ('grantor', models.ForeignKey(editable=False, help_text=b'grantor of privilege', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='x2gcq', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(editable=False, help_text=b'group to which privilege applies', on_delete=django.db.models.deletion.CASCADE, related_name='g2gcq', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='UserCommunityPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.IntegerField(choices=[(1, b'Owner'), (2, b'Change'), (3, b'View')], default=3, editable=False)),
                ('start', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, help_text=b'community to be granted privilege', on_delete=django.db.models.deletion.CASCADE, related_name='c2ucp', to='hs_access_control.Community')),
                ('grantor', models.ForeignKey(editable=False, help_text=b'grantor of privilege', on_delete=django.db.models.deletion.CASCADE, related_name='x2ucp', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, help_text=b'group providing privilege', on_delete=django.db.models.deletion.CASCADE, related_name='u2ucp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCommunityProvenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.IntegerField(choices=[(1, b'Owner'), (2, b'Change'), (3, b'View')], default=3, editable=False)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('undone', models.BooleanField(default=False, editable=False)),
                ('community', models.ForeignKey(editable=False, help_text=b'community to be granted privilege', on_delete=django.db.models.deletion.CASCADE, related_name='c2ucq', to='hs_access_control.Community')),
                ('grantor', models.ForeignKey(editable=False, help_text=b'grantor of privilege', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='x2ucq', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, help_text=b'user to which privilege applies', on_delete=django.db.models.deletion.CASCADE, related_name='u2ucq', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usercommunityprovenance',
            unique_together=set([('community', 'user', 'start')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercommunityprivilege',
            unique_together=set([('community', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupcommunityprovenance',
            unique_together=set([('community', 'group', 'start')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupcommunityprivilege',
            unique_together=set([('community', 'group')]),
        ),
    ]

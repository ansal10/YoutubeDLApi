# Generated by Django 2.0.7 on 2018-07-19 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('video_site', models.CharField(db_index=True, max_length=255)),
                ('video_config', models.TextField(default='{}')),
                ('video_url', models.TextField(default='{}')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

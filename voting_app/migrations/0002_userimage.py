# Generated by Django 3.0.1 on 2020-01-25 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=120)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]

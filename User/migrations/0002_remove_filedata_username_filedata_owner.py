# Generated by Django 4.2.11 on 2024-04-04 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedata',
            name='username',
        ),
        migrations.AddField(
            model_name='filedata',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='User.profile'),
        ),
    ]

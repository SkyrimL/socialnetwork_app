# Generated by Django 3.2.7 on 2021-10-17 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_alter_comment_comment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_is_under_post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='socialnetwork.post'),
        ),
    ]
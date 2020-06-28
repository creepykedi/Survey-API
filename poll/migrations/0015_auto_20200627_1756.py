# Generated by Django 3.0.7 on 2020-06-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0014_person_completed_surveys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='givenanswer',
            name='chosen_answer',
        ),
        migrations.AddField(
            model_name='givenanswer',
            name='chosen_answer',
            field=models.ManyToManyField(blank=True, null=True, to='poll.AnswerOption'),
        ),
    ]

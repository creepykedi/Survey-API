# Generated by Django 3.0.7 on 2020-06-27 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0011_auto_20200627_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='givenanswer',
            name='chosen_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poll.AnswerOption'),
        ),
    ]

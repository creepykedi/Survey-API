# Generated by Django 3.0.7 on 2020-06-24 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20200624_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyquestion',
            name='QuestionId',
        ),
        migrations.RemoveField(
            model_name='surveyquestion',
            name='SurveyId',
        ),
        migrations.RemoveField(
            model_name='surveyquestionanswer',
            name='OfferedAnswerId',
        ),
        migrations.RemoveField(
            model_name='surveyquestionanswer',
            name='QuestionId',
        ),
        migrations.RemoveField(
            model_name='surveyquestionanswer',
            name='SurveyId',
        ),
        migrations.AddField(
            model_name='person',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poll.OfferedAnswer'),
        ),
        migrations.AddField(
            model_name='person',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poll.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poll.Survey'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='SurveyQuestion',
        ),
        migrations.DeleteModel(
            name='SurveyQuestionAnswer',
        ),
    ]

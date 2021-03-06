# Generated by Django 3.0.7 on 2020-06-24 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('finishD', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OfferedAnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.OfferedAnswer')),
                ('QuestionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
                ('SurveyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuestionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
                ('SurveyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OfferedAnswerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.OfferedAnswer')),
                ('PersonId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Person')),
                ('QuestionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
                ('SurveyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Survey')),
            ],
        ),
    ]

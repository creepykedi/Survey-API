from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)
    start_date = models.DateTimeField(null=True, blank=True, )
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id, self.name}"


class AnswerOption(models.Model):
    option = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.id, self.option}"


class Question(models.Model):
    choices = [
        ('1', 'One Choice'),
        ('2', 'Multi Choice'),
        ('3', 'Text')
    ]
    question_text = models.CharField(max_length=256)
    type = models.CharField(choices=choices, max_length=128, default='3')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)
    answer_options = models.ManyToManyField(AnswerOption, blank=True)

    def show_options(self):
        if self.type != 3:
            return ', '.join([a.option for a in self.answer_options.all()])

    def __str__(self):
        return f"{self.id, self.question_text, self.type, [self.show_options()]}"


class Person(models.Model):
    completed_surveys = models.ManyToManyField(Survey, blank=True)
    session_id = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.session_id}"


class GivenAnswer(models.Model):
    given_answer = models.CharField(max_length=256, blank=True, null=True)
    chosen_answer = models.ManyToManyField(AnswerOption, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.given_answer:
            return f"{self.given_answer}"
        else:
            return ', '.join([a.option for a in self.chosen_answer.all()])




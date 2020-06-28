from rest_framework import serializers
from .models import *


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['name', 'description', 'start_date', 'end_date']


class AnswerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['option']


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionsSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'type', 'answer_options']


class PersonSerializer(serializers.ModelSerializer):
    completed_surveys = serializers.ReadOnlyField(source="Person.name")

    class Meta:
        model = Person
        fields = ['hash', 'completed_surveys']


class GivenAnswersSerializer(serializers.ModelSerializer):
    chosen_answer = AnswerOptionsSerializer(read_only=True, many=True)
    question = QuestionSerializer(read_only=True)
    person = PersonSerializer(read_only=True)

    class Meta:
        model = GivenAnswer
        fields = ['given_answer', 'chosen_answer', 'question', 'person']


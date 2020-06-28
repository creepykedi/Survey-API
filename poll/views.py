from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import *
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .serializers import *
import datetime


current_time = timezone.now()
current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_person_hash(request):
    p = Person()
    h = Person.generate_hash(p)
    p.hash = h
    p.save()
    serializer = PersonSerializer(p)
    return JsonResponse(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def delete_survey(request, survey_name):
    s = Survey.objects.get(name=survey_name)
    s.delete()
    return Response({'message': 'Survey has been deleted.'})


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def create_survey(request, survey_name, description):
    if request.method == "POST":
        survey_name = survey_name.strip()
        description = description.strip()
        new_survey = Survey.objects.create(name=survey_name, description=description)
        new_survey.save()
        serializer = SurveySerializer(new_survey)
        return JsonResponse(serializer.data)


@api_view(["PUT"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def update_survey(request, survey_name, new_name, new_desc):
    if request.method == "PUT":
        survey = Survey.objects.get(name=survey_name)
        if survey and not survey.start_date:
            survey.name = new_name
            survey.description = new_desc
        elif survey.start_date:
            raise PermissionDenied
        survey.save()
        serializer = SurveySerializer(survey)
        return JsonResponse(serializer.data)


@api_view(["PUT"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def set_survey_date(request, survey_name, start, end):
    if request.method == "PUT":
        survey = Survey.objects.get(name=survey_name)
        if start == "now":
            survey.start_date = current_time_str
        else:
            survey.start_date = start
        if end == "now":
            survey.end_date = current_time_str
        else:
            survey.end_date = end
        # format YYYY-MM-DD
        survey.save()
        serializer = SurveySerializer(survey)
        return JsonResponse(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def add_question(request, survey_name, question_text, type):
    survey = Survey.objects.get(name=survey_name)
    question = Question.objects.create(question_text=question_text, survey=survey)
    question.type = type
    question.save()
    serializer = QuestionSerializer(question)
    return JsonResponse(serializer.data)


def get_active_surveys(request):
    surveys = Survey.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    active = surveys.values()
    serializer = SurveySerializer(active, many=True)
    return JsonResponse(serializer.data, safe=False)


def start_survey(request, survey_name, person_hash):
    survey = Survey.objects.get(name=survey_name)
    questions = Question.objects.filter(survey=survey)
    s_serializer = SurveySerializer(survey)
    q_serializer = QuestionSerializer(questions, many=True)
    return JsonResponse([s_serializer.data, q_serializer.data], safe=False)


def get_answers(request, person_hash, survey_name):
    survey = Survey.objects.get(name=survey_name)
    person = Person.objects.get(hash=person_hash)
    answers = GivenAnswer.objects.filter(person=person, question__survey=survey)
    serializer = GivenAnswersSerializer(answers, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_completed_surveys(request, person_hash):
    p = Person.objects.get(hash=person_hash)
    completed = p.completed_surveys.values()
    serializer = SurveySerializer(completed, many=True)
    return JsonResponse(serializer.data, safe=False)


def complete_survey(request, person_hash, survey_name):
    survey = Survey.objects.get(name=survey_name)
    person = Person.objects.get(hash=person_hash)
    person.completed_surveys.add(survey)
    person.save()

@csrf_exempt
def write_answer(request, person_hash, question_id, answer):
    if request.method == "POST":
        person = Person.objects.get(hash=person_hash)
        question = Question.objects.get(pk=question_id)
        if question.type == str(1):
            ans = AnswerOption.objects.get(pk=answer)
            a = GivenAnswer.objects.create(person=person, question=question)
            a.chosen_answer.add(ans)
            a.save()
            id = a.id
        elif question.type == str(2):
            a = GivenAnswer.objects.create(person=person, question=question)
            answers = str(answer).split("&")
            for ans in answers:
                ans = AnswerOption.objects.get(pk=ans)
                a.chosen_answer.add(ans)
                a.save()
                id = a.id
        elif question.type == str(3):
            a = GivenAnswer.objects.create(person=person, question=question, given_answer=answer)
            a.save()
            id = a.id
    return JsonResponse({'id': id})

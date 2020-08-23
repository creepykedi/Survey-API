from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import *
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .serializers import *
import datetime
from rest_framework.authtoken.models import Token

current_time = timezone.now()
current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



@api_view(["DELETE"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def delete_survey(request):
    survey_name = request.data['survey']
    s = Survey.objects.get(name=survey_name)
    s.delete()
    return Response({'message': 'Survey has been deleted.'})


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def create_survey(request):
    survey_name = request.data['survey']
    survey_name = survey_name.strip()
    description = request.data['description']
    description = description.strip()
    new_survey = Survey.objects.create(name=survey_name, description=description)
    new_survey.save()
    serializer = SurveySerializer(new_survey)
    return JsonResponse(serializer.data)


@api_view(["PUT"])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([authentication.TokenAuthentication])
def update_survey(request):
    survey_name = request.data['survey name']
    new_name = request.data['new name']
    new_desc = request.data['description']
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
def set_survey_date(request):
    survey_name = request.data['survey name']
    survey = Survey.objects.get(name=survey_name)
    start = request.data['start']
    end = request.data['end']
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
def add_question(request):
    if request.method == "POST":
        question_text = request.data['question text']
        survey_name = request.data['survey name']
        type_ = request.data['type']

        survey = Survey.objects.get(name=survey_name)
        question = Question.objects.create(question_text=question_text, survey=survey)
        question.type = type_
        question.save()
        serializer = QuestionSerializer(data=request.POST) #we can also access through request.data
        return JsonResponse(serializer.data)


def get_active_surveys(request):
    surveys = Survey.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    active = surveys.values()
    serializer = SurveySerializer(active, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def start_survey(request, survey_name):
    survey = Survey.objects.get(name=survey_name)
    questions = Question.objects.filter(survey=survey)
    s_serializer = SurveySerializer(survey)
    q_serializer = QuestionSerializer(questions, many=True)

    if not Person.objects.filter(session_id=request.session.session_key):
        #p = Person.objects.create()
        # token = Token.objects.create(user=p)
        # print(token.key)
        request.session.set_expiry(2628003)
        request.session.save()
        Person(session_id=request.session.session_key).save()

    return JsonResponse([s_serializer.data, q_serializer.data], safe=False)


def get_answers(request, survey_name):
    survey = Survey.objects.get(name=survey_name)
    print(request.session.session_key)
    person = Person.objects.get(session_id=request.session.session_key)
    answers = GivenAnswer.objects.filter(person=person, question__survey=survey)
    serializer = GivenAnswersSerializer(answers, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_completed_surveys(request):
    p = Person.objects.get(session_id__contains=request.session.session_key)
    completed = p.completed_surveys.values()
    serializer = SurveySerializer(completed, many=True)
    return JsonResponse(serializer.data, safe=False)


def complete_survey(request, survey_name):
    survey = Survey.objects.get(name=survey_name)

    person = Person.objects.get(session_id=request.session.session_key)

    person.completed_surveys.add(survey)
    person.save()

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.BasePermission])
def write_answer(request):
    if request.method == "POST":
        answer = request.data['answer']
        question_id = request.data['question id']
        person = Person.objects.get(session_id=request.session.session_key)
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
   # JsonResponse["Access-Control-Allow-Origin"] = True
    return JsonResponse({'id': id})

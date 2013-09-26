from questionnaire_server.models import Question, QuestionAnswers
from django.core import serializers
from django.http import HttpResponse


def questions(request):
    questions= Question.objects.all()
    question_answers = QuestionAnswers.objects.all()
    return HttpResponse(HttpResponseserializers.serialize('json', questions), content_type="application/json")

from questionnaire_server.models import MultipleChoiceAnswer, Question

from tastypie import fields
from tastypie.resources import ModelResource


class MultipleChoiceAnswerResource(ModelResource):

    class Meta:
        resource_name = 'MultipleChoiceAnswer'
        queryset = MultipleChoiceAnswer.objects.all()
        include_resource_uri = False

class QuestionResource(ModelResource):
    answers = fields.ToManyField(MultipleChoiceAnswerResource, 'question', full=True, blank=True)

    class Meta:
        resource_name = 'Questions'
        queryset = Question.objects.all()
        #allowed_methods = ['get']
        include_resource_uri = False

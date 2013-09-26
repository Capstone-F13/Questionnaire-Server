from questionnaire_server.models import MultipleChoiceAnswer, Question

from tastypie import fields
from tastypie.resources import ModelResource


class MultipleChoiceAnswerResource(ModelResource):

    class Meta:
        resource_name = 'MultipleChoiceAnswer'
        queryset = MultipleChoiceAnswer.objects.all()
        allowed_methods = ['get']
        include_resource_uri = False

class QuestionResource(ModelResource):
    answers = fields.ToManyField(MultipleChoiceAnswerResource, 
                                 'multiple_choice_answer', 
                                 full=True, 
                                 blank=True)

    class Meta:
        resource_name = 'Questions'
        queryset = Question.objects.all()
        allowed_methods = ['get']
        include_resource_uri = False

# TODO: setup UserAnswerResource for posting answers from user.

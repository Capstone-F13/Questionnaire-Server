from django.contrib import admin
from questionnaire_server.models import MultipleChoiceAnswer, Question, UserAnswer

admin.site.register(MultipleChoiceAnswer)
admin.site.register(Question)
admin.site.register(UserAnswer)

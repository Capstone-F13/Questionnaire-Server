from questionnaire_server.models import MultipleChoiceAnswer, Question, Patient, Study, Survey, UserAnswer

from django.contrib import admin

admin.site.register(MultipleChoiceAnswer)
admin.site.register(Question)
admin.site.register(Patient)
admin.site.register(Study)
admin.site.register(Survey)
admin.site.register(UserAnswer)


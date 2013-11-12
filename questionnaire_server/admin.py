from questionnaire_server.models import MultipleChoiceAnswer, Question, Patient, Survey, UserAnswer, SurveyResponse

from django.contrib import admin
from django.contrib.sites.models import Site

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('patient', 'question', 'answer')

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'timestamp' , 'score', 'did_listen')

admin.site.register(MultipleChoiceAnswer)
admin.site.register(Question)
admin.site.register(Patient)
admin.site.register(Survey)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)

admin.site.unregister(Site)

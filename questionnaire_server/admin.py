from questionnaire_server.models import MultipleChoiceAnswer, Question, Patient, Survey, UserAnswer

from django.contrib import admin

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('patient', 'question', 'answer')

admin.site.register(MultipleChoiceAnswer)
admin.site.register(Question)
admin.site.register(Patient)
admin.site.register(Survey)
admin.site.register(UserAnswer, UserAnswerAdmin)


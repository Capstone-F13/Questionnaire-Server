from questionnaire_server.api.resources import MultipleChoiceAnswerResource, QuestionResource

from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MultipleChoiceAnswerResource())
v1_api.register(QuestionResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^answer/', 'questionnaire_server.views.submit_answer'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^patient/login', 'questionnaire_server.views.login_patient'),
    url(r'^patient/logout', 'questionnaire_server.views.logout_patient'),
    url(r'^patients/(?P<token>.+)', 'questionnaire_server.views.get_patients'),
)

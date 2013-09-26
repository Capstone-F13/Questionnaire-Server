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
)

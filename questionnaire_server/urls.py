from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^answer/', 'questionnaire_server.views.submit_answer'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^patient/login', 'questionnaire_server.views.login_patient'),
    url(r'^patient/create', 'questionnaire_server.views.create_patient'),
    url(r'^patient/logout', 'questionnaire_server.views.logout_patient'),
    url(r'^patients/(?P<token>.+)', 'questionnaire_server.views.get_patients'),
    url(r'^questions/(?P<access_token>.+)/(?P<patient_id>.+)', 'questionnaire_server.views.get_questions'),
    url(r'^report_builder/', include('report_builder.urls')),
)

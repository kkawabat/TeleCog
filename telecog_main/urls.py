from django.urls import path

from telecog_main.views import greetings, analyze_object_naming, assessment1

urlpatterns = [
    path('greetings', greetings),
    path('assessment1', assessment1),
    path('assessment2', assessment1),
    path('analyze_object_naming', analyze_object_naming),
]

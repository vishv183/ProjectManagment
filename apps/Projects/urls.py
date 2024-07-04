from django.urls import path

from apps.Projects.views import index

urlpatterns=[
    path('', index, name='index')

]
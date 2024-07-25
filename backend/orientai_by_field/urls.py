from django.urls import path
from . import views

app_name = 'orientai_by_field'

urlpatterns = [
    path('', views.index, name='index'),
]

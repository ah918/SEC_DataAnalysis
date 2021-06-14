from django.urls import path

from . import views

app_name = 'SEC_App'
urlpatterns = [
    path('', views.search, name='search'),
]
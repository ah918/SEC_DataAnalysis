from django.urls import path

from . import views

app_name = 'SEC_App'
urlpatterns = [
    path('', views.search, name='search'),
    path('analysis/', views.analysis, name='analysis')
]
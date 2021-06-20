from django.urls import path

from . import views

app_name = 'SEC_App'
urlpatterns = [
    path('', views.searchView, name='search'),
    path('analysis/', views.analysis, name='analysis')
]
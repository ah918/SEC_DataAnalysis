from django.urls import path

from . import views

app_name = 'SEC_App'
urlpatterns = [
    path('', views.searchView, name='search'),
    path('analysis/', views.analysis, name='analysis'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register')
]
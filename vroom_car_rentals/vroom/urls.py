from django.urls import path
from . import views

app_name = 'vroom'

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('log-in/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]

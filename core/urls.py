from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('help/', views.help_home, name='help'),
    path('support/', views.support, name='support'),
    path('settings/', views.general_settings, name='settings'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
]

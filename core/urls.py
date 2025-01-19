from django.urls import path
from .views import SpecialtyListView

app_name = 'core'

urlpatterns = [
    path('', SpecialtyListView.as_view(), name='home'),
]

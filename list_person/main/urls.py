from django.urls import path
from .views import MainList

urlpatterns = [
    path('', MainList.as_view(), name='home')
]
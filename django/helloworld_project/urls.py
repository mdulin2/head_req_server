from django.contrib import admin
from django.urls import path, include # new

from .views import firstView,index
urlpatterns = [
    path('first', firstView.as_view()),
    path('', index, name='index')
]

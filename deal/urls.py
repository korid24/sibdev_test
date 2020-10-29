from django.urls import path
from . import views

urlpatterns = [
    path('', views.DealView.as_view())
]

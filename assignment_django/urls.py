from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.create_customer, name='create_customer'),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="support_index"),
    path("success/", views.support_success, name="support_success"),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
]

from django.urls import path
from .views import RegisterView, UserDetail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserDetail.as_view(), name='user-detail'),
]

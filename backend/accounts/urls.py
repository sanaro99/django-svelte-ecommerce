from django.urls import path
from .views import RegisterView, UserDetail, public_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    # User authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Public GET logout to allow full-page logout
    path('logout/', public_logout, name='logout'),
    # Registration and current user
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserDetail.as_view(), name='user-detail'),
]
from django.shortcuts import render

# backend/accounts/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.shortcuts import redirect

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        try:
            validate_password(password)
        except DjangoValidationError as e:
            # Return password field errors to frontend
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"success": True, "user_id": user.id}, status=201)

# New endpoint to fetch current user info
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'username': user.username, 'email': user.email})

def public_logout(request):
    """
    Logs out via GET and redirects to 'next' parameter or LOGIN_REDIRECT_URL.
    """
    django_logout(request)
    next_url = request.GET.get('next') or settings.LOGIN_REDIRECT_URL
    return redirect(next_url)

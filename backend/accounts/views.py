# backend/accounts/views.py: endpoints for user registration, profile, and logout

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
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from catalog.views import MethodScopedTokenHasScope

class RegisterView(APIView):
    """
    API view for user registration (Signup). Open to all.
    Create a new user account by providing username, password, and optional email.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get("username")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
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

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        return Response({"success": True, "user_id": user.id}, status=201)

class UserDetail(APIView):
    """
    Retrieve the current authenticated user's username and email.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {'GET': ['read:customers'], 'PUT': ['write:customers']}
    
    def get(self, request):
        user = request.user
        # Include user and customer profile details
        profile = getattr(user, 'customer', None)
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': profile.phone if profile else '',
            'street_address': profile.street_address if profile else '',
            'city': profile.city if profile else '',
            'state': profile.state if profile else '',
            'postal_code': profile.postal_code if profile else '',
            'country': profile.country if profile else '',
        })

    def put(self, request):
        user = request.user
        # Update basic user info
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        # Update related customer profile
        profile = getattr(user, 'customer', None)
        if profile:
            profile.phone = request.data.get('phone', profile.phone)
            profile.street_address = request.data.get('street_address', profile.street_address)
            profile.city = request.data.get('city', profile.city)
            profile.state = request.data.get('state', profile.state)
            profile.postal_code = request.data.get('postal_code', profile.postal_code)
            profile.country = request.data.get('country', profile.country)
            profile.save()
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': profile.phone if profile else '',
            'street_address': profile.street_address if profile else '',
            'city': profile.city if profile else '',
            'state': profile.state if profile else '',
            'postal_code': profile.postal_code if profile else '',
            'country': profile.country if profile else '',
        })

def public_logout(request):
    """
    Logs out via GET and redirects to 'next' parameter or LOGIN_REDIRECT_URL.
    """
    django_logout(request)
    next_url = request.GET.get('next') or settings.LOGIN_REDIRECT_URL
    return redirect(next_url)

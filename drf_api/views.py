from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)

@api_view(['GET'])
def root_route(request):
    """
    Root route for API, useful for testing connectivity
    """
    return Response({
        'status': 'ok',
        'message': 'Welcome to BookHub API',
        'csrf': request.META.get('CSRF_COOKIE', None) is not None,
        'session': request.META.get('HTTP_COOKIE', '').find('sessionid') > -1,
        'auth': request.user.is_authenticated,
    })

@api_view(['POST'])
def logout_route(request):
    """
    Custom logout route to make sure both Django session and JWT are cleared
    """
    response = Response({'detail': 'Successfully logged out.'})
    response.delete_cookie(JWT_AUTH_COOKIE)
    response.delete_cookie(JWT_AUTH_REFRESH_COOKIE)
    
    logout(request)
    return response

# CSRF token view already in urls.py, but updated here for reference
class GetCSRFTokenView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "CSRF token set"})

@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status(request):
    """
    Debug view to check authentication status and cookies
    """
    cookies = {k: v for k, v in request.COOKIES.items()}
    
    # For security, mask the actual values
    for key in cookies:
        if key not in ['csrftoken']:
            cookies[key] = f"****{cookies[key][-4:] if len(cookies[key]) > 4 else '****'}"
    
    return Response({
        'authenticated': request.user.is_authenticated,
        'user': str(request.user),
        'cookies_present': cookies,
        'headers': {
            'csrf': request.META.get('HTTP_X_CSRFTOKEN', None) is not None,
            'has_session': 'sessionid' in request.COOKIES,
            'has_jwt': JWT_AUTH_COOKIE in request.COOKIES,
            'has_refresh': JWT_AUTH_REFRESH_COOKIE in request.COOKIES,
        }
    })
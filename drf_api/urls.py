from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route, GetCSRFTokenView, auth_status
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('get-csrf-token/', GetCSRFTokenView.as_view()),
    path('api/auth-status/', auth_status, name='auth_status'),
    
    # App-specific routes
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('comments.urls')),
    path('', include('likes.urls')),
    path('', include('followers.urls')),
]
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import RegisterView, ProfilePostView

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('registration/', RegisterView.as_view(), name='registration_view'),
   path('post/profile/<int:user_id>', ProfilePostView.as_view(), name='profile_post_view'),
   path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers
from . import views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'registration', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
   path('', include(router.urls)),
]

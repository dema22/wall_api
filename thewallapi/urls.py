from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ProfilePostView, UserListView, ListCreatePostView

# The API URLs are now determined automatically by the router.
urlpatterns = [
   path('posts/', ListCreatePostView.as_view(), name='list_create_post_view'),
   path('users/', UserListView.as_view(), name='user_list_view'),
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('registration/', RegisterView.as_view(), name='registration_view'),
   path('post/profile/<int:user_id>', ProfilePostView.as_view(), name='profile_post_view'),
]

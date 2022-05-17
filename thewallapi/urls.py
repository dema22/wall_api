from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ProfilePostView, UserListView, ListCreatePostView, LogoutView


urlpatterns = [
   path('posts/', ListCreatePostView.as_view(), name='list_create_post_view'),
   path('users/', UserListView.as_view(), name='user_list_view'),
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('logout/', LogoutView.as_view(), name="logout_view"),
   path('registration/', RegisterView.as_view(), name='registration_view'),
   path('post/profile/<int:user_id>', ProfilePostView.as_view(), name='profile_post_view'),
]

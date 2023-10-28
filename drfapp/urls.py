from django.urls import path, include
from drfapp import views
from rest_framework import routers

app_name = "drfapp"

router = routers.DefaultRouter()
router.register(r'tags', views.TagApiView, basename="tags")

urlpatterns = [
    path("", include(router.urls)),
    path('posts/', views.PostAPIView.as_view(), name='posts'), # For Get and Post request of post
    path('posts/<int:pk>/', views.PostAPIView.as_view(), name='get_update_post'), # to get the specific post details
    # path('posts/<int:pk>/', views, name='update_post'), # to update the specific post
    # path('posts/delete/<int:pk>/', views, name='delete_post'), # to delete a specific post
    # path('get-blocked-user/', views, name='get_blocked_user'), # to get the blocked user details
    path('block-user/', views.BlockUserAPIView.as_view(), name='block_user'), # to block a user
    # path('unblock-user/', views, name='unblock_user'), # to unblock user
]

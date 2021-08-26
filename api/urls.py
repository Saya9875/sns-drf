from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users',views.UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path("<uuid:id>/follow/", view=views.FollowUsers.as_view(), name="follow_users"),
    path("<uuid:id>/unfollow/", view=views.UnfollowUsers.as_view(), name="unfollow_users"),
    path("<username>/followees", view=views.UserFollwees.as_view(), name="user_followee"),
    path("<username>/following", view=views.UserFollowing.as_view(), name="user_following"),
]

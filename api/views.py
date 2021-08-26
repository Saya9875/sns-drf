from api import serializers, models
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class FollowUsers(APIView):
    """フォローする"""
    def post(self, request, id):
        user = request.user
        user_to_follow = models.User.objects.get(id=id)
        user.following.add(user_to_follow)
        user_to_follow.followees.add(user)
        return Response(status=status.HTTP_200_OK)


class UnfollowUsers(APIView):
    """フォロー解除する"""
    def post(self, request, id):
        user = request.user
        user_to_follow = models.User.objects.get(id=id)
        user.following.remove(user_to_follow)
        user_to_follow.followees.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollwees(APIView):
    """フォロワー一覧"""
    def get(self, request, username):
        found_user = models.User.objects.get(username=username)
        follow_user = found_user.followees.all()
        serializer = serializers.ListUserSerializer(follow_user, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):
    """フォロー一覧"""
    def get(self, request, username):
        found_user = models.User.objects.get(username=username)
        following_user = found_user.following.all()
        serializer = serializers.ListUserSerializer(following_user, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)



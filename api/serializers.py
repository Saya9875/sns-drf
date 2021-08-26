from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id', 
            'username', 
            'email', 
            'password', 
            'user_img'
            )
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user


class ListUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            'id',
            'username',
            'following',
            'followees',
        )

    def get_following(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False

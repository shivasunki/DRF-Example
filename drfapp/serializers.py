from rest_framework import serializers
from drfapp.models import Post, Tag, BlockedUser
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

class PostSerializer(serializers.ModelSerializer):
    # author_id = serializers.SerializerMethodField()

    # def get_author_id(self, obj):        
    #     return self.context["author_id"]

    class Meta:
        model = Post
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BlockUserSerializer(serializers.ModelSerializer):
    blocked_user = UserSerializer()
    blocked_by = UserSerializer()

    class Meta:
        model = BlockedUser
        fields = "__all__"
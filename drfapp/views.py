import json

from django.shortcuts import render, get_object_or_404
# from drfapp.models import Post
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from drfapp.models import Post, Tag, BlockedUser
from drfapp.serializers import PostSerializer, TagSerializer, UserSerializer, BlockUserSerializer
from rest_framework import viewsets
# from rest_framework.authentication import BaseAuthentication

def is_admin(user_id):
    if User.objects.get(id=user_id).is_superuser:
        return True
    return False

@receiver(post_save, sender=Post)
def send_email(sender, instance, **kwargs):
    pass


class PostAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            post = Post.objects.filter(id=pk, is_active=True).first()
            if not post:
                return Response({"message": "Post doesn't exist!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PostSerializer(post)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            print("get all posts")
            posts = Post.objects.filter(is_active=True)
            serializer = PostSerializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        print(json.loads(request.body))
        if pk:
            print("Post with pk")
        else:
            data = json.loads(request.body)
            user_id = data.get("author")
            if user_id and is_admin(user_id):
                
                serialzer = PostSerializer(request.data)
                return Response({"message": "Post created successfully!"}, status=status.HTTP_201_CREATED)
            
            elif user_id and not is_admin(user_id):
                return Response({"message": "You are not authorized to create posts for other user!"}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                data=request.data
                data["author"] = request.user.id
                print(data)
                serialzer = PostSerializer(data=data)
                
                if serialzer.is_valid():
                   serialzer.save()
                   print(serialzer.data)
                   return Response(data, status=status.HTTP_201_CREATED) 

                return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print("Received Put")
        post = Post.objects.get(id=pk)
        
        data = request.data
        data["author"] = post.author.id

        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        print("Received delete")
        data = request.data.copy()
        data["is_active"] = False
        print(data)
        post.is_active = False
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class BlockUserAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            blocked_user = BlockedUser.objects.get(blocked_user_id=pk)
            serializer = BlockUserSerializer(blocked_user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            print("get all")
            blocked_users = BlockedUser.objects.all()
            serializer = BlockUserSerializer(blocked_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            blocked_user = BlockedUser.objects.get(blocked_user_id=id, blocked_by=request.user)
            data = request.data.copy()
            data["blocked_by"] = request.user.id
            serializer = BlockUserSerializer(blocked_user, data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data.copy()
        data["blocked_by"] = request.user.id
        serializer = BlockUserSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            blocked_user = BlockedUser.objects.get(blocked_user_id=id, blocked_by=request.user)
            blocked_user.is_blocked = False
            blocked_user.save()
            serializer = BlockUserSerializer(blocked_user) 
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class TagApiView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


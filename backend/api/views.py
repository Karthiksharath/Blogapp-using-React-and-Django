from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum

from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

import json
import random

from api import serializer as api_serializers
from api import models as api_models


class TokenObtainView(TokenObtainPairView):

  serializer_class = api_serializers.UserToken


class RegisterView(generics.CreateAPIView):

  queryset = api_models.User.objects.all()
  serializer_class = api_serializers.RegisterSeializer
  permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):

  serializer_class = api_serializers.ProfileSerializer
  permission_classes = [AllowAny]


  def get_object(self):
      user_id = self.kwargs['user_id']
      try:
          user = api_models.User.objects.get(id=user_id)
          profile = api_models.Profile.objects.get(user=user)

      except api_models.User.DoesNotExist:
          raise NotFound("User not found.")
      
      except api_models.Profile.DoesNotExist:
          raise NotFound("Profile not found.")
      
      return profile


class CategoryListAPIView(generics.ListAPIView):
    
    serializer_class = api_serializers.CategorySerializer
    permission_classes = [AllowAny]
    queryset = api_models.Category.objects.all()


class PostCategoryListAPIView(generics.ListAPIView):
    
    serializer_class = api_serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        
        category_slug = self.kwargs['category_slug'] 
        category = api_models.Category.objects.get(slug=category_slug)
        filtered = api_models.Post.objects.filter(category=category, status="Active")

        return filtered


class PostListApiView(generics.ListAPIView):
   
   serializer_class = api_serializers.PostSerializer
   permission_classes = [AllowAny]

   def get_queryset(self):
      
      return api_models.Post.objects.all()


class PostDetailApiView(generics.RetrieveAPIView):
   
    serializer_class = api_serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
       
       slug = self.kwargs['slug']
       post = api_models.Post.objects.get(slug=slug, status='Active')
       post.view += 1
       post.save()

       return post
    


class PostLikeApiView(generics.CreateAPIView):

    serializer_class = api_serializers.NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Notification.objects.all()
    

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            post_id = kwargs.get('post_id')

            post = api_models.Post.objects.get(id=post_id)
            user = api_models.User.objects.get(id=user_id)

            if user in post.likes.all():
                post.likes.remove(user)
                return Response({"message": "Post Unliked"}, status=status.HTTP_200_OK)

            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type="Like",
            )
            return Response({"message": "Post Liked"}, status=status.HTTP_201_CREATED)

        except api_models.Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except api_models.User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostCommentAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'comment': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    def post(self, request):

        try:
            post_id = request.data['post_id']
            name = request.data['name']
            email = request.data['email']
            comment = request.data['comment']

            post  = api_models.Post.objects.get(id=post_id)

            api_models.Comment.objects.create(
                post=post,
                name=name,
                email=email,
                comment=comment,
            )

            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type=comment
            )

            return Response({"message": "Comment sent"}, status=status.HTTP_201_CREATED)
        
        except api_models.Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BookMarkPostApiView(APIView):

    # decorator provided by drf-yasg, a  django library for generating Swagger documentation
    @swagger_auto_schema(
        # openapi.Schema is used to define the structure of the JSON data that the client should send.
        request_body=openapi.Schema(
            # TYPE_OBJECT Specifies that the body of the request should be a JSON object.
            type=openapi.TYPE_OBJECT,
            #  properties of the object that the request body will contain
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    def post(self,request):
        try:

            user_id = request.tdata['user_id']
            post_id = request.tdata['post_id']

            if not user_id or post_id:
                return Response({"error": "user_id and post_id are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = api_models.User.objects.get(id=user_id)
            post = api_models.Post.objects.get(id=post_id)

            bookmark = api_models.Bookmark.objects.filter(post=post, user=user)

            if bookmark:

                bookmark.delete()
                return Response({"message": "Post Un-Bookmarked"}, status=status.HTTP_200_OK)
            
            api_models.Bookmark.objects.create(

                    user=user,
                    post=post,
                    type=bookmark
            )

        except api_models.User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except api_models.Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DashboardStats(generics.ListAPIView):
    
    serializer_class = api_serializers.AuthorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)

        views = api_models.Post.objects.filter(user=user).aggregate(view=Sum("view"))['view']
        posts = api_models.Post.objects.filter(user=user).count()
        likes = api_models.Post.objects.filter(user=user).aggregate(total_likes=Sum("likes"))['total_likes']
        bookmarks = api_models.Bookmark.objects.all().count()

        return [{
            "views": views,
            "posts": posts,
            "likes": likes,
            "bookmarks": bookmarks,
        }]

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DashboardPostLists(generics.ListAPIView):

    serializer_class = api_serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)

        return api_models.Post.objects.filter(user=user).order_by("-id")



class DashboardCommentLists(generics.ListAPIView):

    serializer_class = api_serializers.CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Comment.objects.all()




class DashboardNotificationLists(generics.ListAPIView):

    serializer_class = api_serializers.NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)

        return api_models.Notification.objects.filter(seen=False, user=user)



class DashboardMarkNotificationSeenAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'noti_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    
    def post(self, request):
        noti_id = request.data['noti_id']
        noti = api_models.Notification.objects.get(id=noti_id)

        noti.seen = True
        noti.save()

        return Response({"message": "Noti Marked As Seen"}, status=status.HTTP_200_OK)



class DashboardPostCommentAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'reply': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    def post(self, request):

        comment_id = request.data['comment_id']
        reply = request.data['reply']

        print("comment_id =======", comment_id)
        print("reply ===========", reply)

        comment = api_models.Comment.objects.get(id=comment_id)
        comment.reply = reply
        comment.save()

        return Response({"message": "Comment Response Sent"}, status=status.HTTP_201_CREATED)



class DashboardPostCreateAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.PostSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')

        print(user_id)
        print(title)
        print(image)
        print(description)
        print(tags)
        print(category_id)
        print(post_status)

        user = api_models.User.objects.get(id=user_id)
        category = api_models.Category.objects.get(id=category_id)

        post = api_models.Post.objects.create(
            user=user,
            title=title,
            image=image,
            description=description,
            tags=tags,
            category=category,
            status=post_status
        )

        return Response({"message": "Post Created Successfully"}, status=status.HTTP_201_CREATED)




class DashboardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = api_serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.get(user=user, id=post_id)

    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()

        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')

        print(title)
        print(image)
        print(description)
        print(tags)
        print(category_id)
        print(post_status)

        category = api_models.Category.objects.get(id=category_id)

        post_instance.title = title
        if image != "undefined":
            post_instance.image = image
        post_instance.description = description
        post_instance.tags = tags
        post_instance.category = category
        post_instance.status = post_status
        post_instance.save()

        return Response({"message": "Post Updated Successfully"}, status=status.HTTP_200_OK)







         
      
      

   


  

    


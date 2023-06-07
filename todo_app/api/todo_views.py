from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from todo_app.api.serializers import AuthSerializer,AddNewsSerializer,UserAuthApi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from todo_app.models import DailyNews
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q




class RegisterUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = AuthSerializer

    def post(self, request):
        # Validate the serializer data
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Get the username and password from the validated data
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'})
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            token = Token.objects.create(user=user)
            return Response({'message': 'Registration successful'})
        else:
            return Response(serializer.errors)





class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate the serializer data
        serializer = UserAuthApi(data=request.data)
        if serializer.is_valid():
            # Get the username and password from the validated data
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Get the token for the authenticated user
                token = Token.objects.get(user=user)
                return Response({'message': token.key})
            else:
                return Response({'error': 'Invalid credentials'})
        else:
            return Response({'error': 'Please enter username and password'})
        return Response(serializer.errors)





class AddNews(APIView):
    permission_classes = [IsAuthenticated]
    serializer = AddNewsSerializer

    def post(self, request):
        # Validate the serializer data
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            # Get the title from the validated data
            title = serializer.validated_data.get('title')
            # Check if the news with the same title already exists
            if DailyNews.objects.filter(title=title).exists():
                return Response({"message": "already exists"})
            else:
                # Save the news
                news_save = serializer.save()
                return Response({"message": "successfully added News"})
        else:
            return Response(serializer.errors)





class UpdateNews(APIView):
    permission_classes = [IsAuthenticated]
    serializer = AddNewsSerializer

    def post(self, request, id):
        # Get the news instance with the provided ID
        instance = get_object_or_404(DailyNews, id=id)
        # Validate the serializer data with the instance
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            # Save the updated news
            serializer.save()
            return Response({"message": "successfully updated"})
        else:
            return Response({"message": "not updated"})





class DeleteNews(APIView):
    permission_classes = [IsAuthenticated]
    serializer = AddNewsSerializer

    def post(self, request, id):
        # Get the news to delete
        delete_id = DailyNews.objects.get(id=id)
        if delete_id:
            # Delete the news
            delete_id.delete()
            return Response({"message": "successfully deleted"})
        else:
            return Response({"message": "not deleted"})




class ListAll(APIView):
    permission_classes = [IsAuthenticated]
    serializer = AddNewsSerializer

    def get(self, request):
        # Get the search query parameter
        search = request.GET.get("search")
        # Get all the news and order by ID
        lists = DailyNews.objects.all().order_by("-id")
        if lists and search:
            # Filter the news by title containing the search query
            lists = lists.filter(Q(title__icontains=search))
        paginator = PageNumberPagination()
        paginator.page_size = 3
        # Paginate the news queryset
        result_page = paginator.paginate_queryset(lists, request)
        serializer = AddNewsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)











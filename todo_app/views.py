from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.views.generic.base import TemplateView
from .models import DailyNews
from django.template.loader import render_to_string
from django.http import JsonResponse



class TemplateList(TemplateView):
    def get(self, request, *args, **kwargs):
        lists = DailyNews.objects.all().order_by("-id")
        search_text = request.GET.get('search','')
        if search_text:
        	lists=lists.filter(Q(title__icontains=search_text))
        paginator = Paginator(lists, 5) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = render_to_string('news_list_pagination.html', context)
            return JsonResponse(response, safe=False)        
        return render(request, "list_news.html", context)





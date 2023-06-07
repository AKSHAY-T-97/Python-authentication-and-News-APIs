from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth.views import LoginView
from todo_app import views



urlpatterns =[	
	path('template_list',views.TemplateList.as_view())															
]

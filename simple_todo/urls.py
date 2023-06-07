"""simple_todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from todo_app.api import todo_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lists/', include("todo_app.urls")),
    path('api/todo/register',todo_views.RegisterUser.as_view()),
	path('api/todo/login',todo_views.LoginUser.as_view()),
	path('api/todo/add',todo_views.AddNews.as_view()),
	path('api/todo/update/<int:id>/',todo_views.UpdateNews.as_view()),
	path('api/todo/delete/<int:id>/',todo_views.DeleteNews.as_view()),
	path('api/todo/list',todo_views.ListAll.as_view()),
	
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from rest_framework import serializers
from django.contrib.auth.models import User
from todo_app.models import DailyNews


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserAuthApi(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()
	class Meta:
		fields = ["username","password"]		
        

class AddNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyNews
        fields = [
            'title',
            'description',
            'publication_date',
            'author',
            'image',
            'created_at',
            'updated_at'
        ]
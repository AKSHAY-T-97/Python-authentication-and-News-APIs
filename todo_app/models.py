from django.db import models


class DailyNews(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	publication_date = models.DateField()
	author = models.CharField(max_length=50)
	image = models.ImageField(upload_to='news_images/')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)    
	class Meta:
		db_table = 'daily_news'
from django.urls import path
from .views import scrape, news_list

app_name = 'news'
urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('', news_list, name="home"),
]
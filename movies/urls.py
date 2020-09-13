from django.urls import path

from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.search_movies, name='search_movies'),
    
]
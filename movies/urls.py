from django.urls import path

from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.search_movies, name='search_movies'),
    path(
        'watchlist/add/<str:movie_id>/', views.toggle_movie_to_watchlist, 
        name='toggle_movie_to_watchlist'
        ),

]
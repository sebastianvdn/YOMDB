from django.shortcuts import render

def search_movies(request):
    return render(request, 'movies/search.html')
from django.shortcuts import render
from django.conf import settings
import requests

from .forms import SearchMoviesForm



def search_movies(request):
    form = SearchMoviesForm(request.GET or None)
    context = {
        'form': form
    }
    if request.method == "GET":
        if form.is_valid():
            movies = requests.get(
                f"http://www.omdbapi.com/?s={form.cleaned_data['title']}&apikey={settings.OMDB_API_KEY}"
                )
            print(movies.json())
            
            context['movies'] = movies.json().get('Search', False)

    return render(request, 'movies/search.html', context)
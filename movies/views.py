from django.shortcuts import render
from django.conf import settings

import requests

from .forms import SearchMoviesForm


def search_movies(request):
    form = SearchMoviesForm(request.GET or None)
    context = {
        'form': form
    }
    page_number = request.GET.get('page', 1)

    if request.method == "GET":
        if form.is_valid():
            movies = requests.get(
                f"http://www.omdbapi.com/?s={form.cleaned_data['title']}&page={page_number}&apikey={settings.OMDB_API_KEY}"
                )
            
            context['movies'] = movies.json().get('Search', False)
            context['max_page'] = range(1, int(movies.json().get('totalResults', 0)) // 10 + 1) 

    return render(request, 'movies/search.html', context)
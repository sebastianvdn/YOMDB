from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q

import requests

from .forms import SearchMoviesForm
from .models import WatchList


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
            context['max_page'] = range(1, round(int(movies.json().get('totalResults', 0)) / 10 + 1))

    return render(request, 'movies/search.html', context)


def toggle_movie_to_watchlist(request, movie_id):
    user = request.user
    resp = {}
    if request.method == 'POST':
        if not user.is_authenticated:
            return JsonResponse({'error': 'Login'}, status='400')

        movie = requests.get(
                    f"http://www.omdbapi.com/?i={movie_id}&apikey={settings.OMDB_API_KEY}"
                    ).json()

        if WatchList.objects.filter(user=user, movie_id=movie_id).exists():
            WatchList.objects.filter(user=user, movie_id=movie_id).delete()
            resp['removed'] = True

        else:
            resp['removed'] = False
            watch = WatchList()
            watch.movie_title = movie['Title']
            watch.movie_actors = movie['Actors']
            watch.movie_genre = movie['Genre']
            watch.movie_poster = movie['Poster']
            watch.user = user
            watch.movie_id = movie_id

            watch.save()
    return JsonResponse(resp)


class WatchListView(LoginRequiredMixin, ListView):
    model = WatchList
    template_name = 'movies/user_watchlist.html'


    def get_queryset(self):
        watched = self.request.GET.get('watched')
        actor = self.request.GET.get('actor')
        genre = self.request.GET.get('genre')
        filter_watchlist = Q()
        if watched:
            filter_watchlist &= Q(watched=watched)
        if actor:
            filter_watchlist &= Q(movie_actors__icontains=actor)
        if genre:
            filter_watchlist &= Q(movie_genre__icontains=genre)
        return self.model.objects.filter(user=self.request.user).filter(filter_watchlist)


@require_http_methods(['POST'])
def update_watchlist_item(request, movie_id):
    if request.method == "POST":
        watched = request.POST.get('watched')
        if watched == 'True':
            code = messages.success
            message = 'Movie set to watched successfully'
        else:
            code = messages.error
            message = "Movie set to not watched successfully"
        WatchList.objects.filter(user=request.user, movie_id=movie_id).update(watched=watched)
        code(request, message)
    return redirect('movies:WatchListView')
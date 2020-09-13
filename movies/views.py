from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

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
    print(movie_id)
    resp = {}
    if request.method == 'POST':
        if not user.is_authenticated:
            print('redirext')
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
            print(movie)
            watch.movie_title = movie['Title']
            watch.movie_actors = movie['Actors']
            watch.movie_genre = movie['Genre']
            watch.user = user
            watch.movie_id = movie_id

            watch.save()
    return JsonResponse(resp)

def like_recipe_toggle(request, slug):
    user = request.user
    recipe = get_object_or_404(Recipe, slug=slug)
    liked = user in recipe.likes.all()
    if request.method == 'POST':
        if user.is_authenticated:
            if liked:
                # user has already liked this recipes
                # remove like/user
                recipe.likes.remove(user)
            else:
                # add a new like for a recipe
                recipe.likes.add(user)
            user_likes_count = user.recipe_likes.count()
        else:
            user_likes_count = 0
            messages.info(request, 'You need to login in order to like recipes.')

    return JsonResponse({
        'liked': liked, 'liked_recipe': recipe.pk, 'liked_recipe_slug': recipe.slug,
        'likes_count': recipe.likes.count(),
        'logged_in': user.is_authenticated,
        'user_likes_count': user_likes_count
        })
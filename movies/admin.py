from django.contrib import admin

from .models import WatchList

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_filter = ('watched', )
    search_fields = ('movie_actors', 'movie_genre')

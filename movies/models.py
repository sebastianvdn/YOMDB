from django.db import models

from django.contrib.auth.models import User


class WatchList(models.Model):
    movie_title = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=9, db_index=True)
    movie_genre = models.CharField(max_length=255)
    movie_actors = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name='watchlist', on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    added = models.DateField(auto_now_add=True,)

    def __str__(self):
        return f'{self.user} wants to watch {self.movie_title}'

    class Meta:
        ordering = ['-added']
        unique_together = ['movie_id', 'user']
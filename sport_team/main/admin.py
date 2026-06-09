from django.contrib import admin

from .models import Player, Team, Game, PlayerRating


# Register your models here
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(PlayerRating)
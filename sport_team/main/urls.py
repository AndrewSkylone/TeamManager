from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('players', views.players, name='players'),
    path('player/<int:pk>/', views.player, name='player'),
    path('accounts/login/', views.PlayerLoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.PlayerLogoutView.as_view(), name='logout'),
    path('accounts/profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/password/edit/', views.PasswordEditView.as_view(), name='password_edit'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('player_search/<int:game_pk>/', views.player_search, name='player_search'),
    path('game/new', views.GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/edit', views.GameEditView.as_view(), name='game_edit'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('game/<int:game_pk>/remove_player/<int:player_pk>', views.remove_player_from_game, name='game_remove_player'),
    path('game/<int:game_pk>/add_player/<int:player_pk>', views.add_player_to_game, name='game_add_player'),
    path('game/<int:pk>/teams', views.game_teams, name='game_teams'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
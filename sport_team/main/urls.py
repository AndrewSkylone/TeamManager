from django.urls import path

from .views import PlayerLoginView, PlayerLogoutView, ProfileEditView, GameCreateView, PasswordEditView, GameDetailView, GameEditView
from .views import index, profile, player, players, game_teams
from django.conf.urls.static import static
from django.conf import settings
from .views import RegisterView


app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('players', players, name='players'),
    path('player/<int:pk>/', player, name='player'),
    path('accounts/login/', PlayerLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', PlayerLogoutView.as_view(), name='logout'),
    path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/password/edit/', PasswordEditView.as_view(), name='password_edit'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('game/new', GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/edit', GameEditView.as_view(), name='game_edit'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('game/<int:pk>/teams', game_teams, name='game_teams'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
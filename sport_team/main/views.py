from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Avg
import math

from .forms import ProfileEditForm, RegisterForm, PlayerRatingForm, GameCreateForm
from .models import Player, PlayerRating, Game, Team




class GameCreateView(CreateView):
    model = Game
    template_name = 'main/game/form.html'
    form_class = GameCreateForm
    success_url = reverse_lazy('main:game_detail')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.organizer = self.request.user
        game.save()

        form.save_m2m()

        self.object = game

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'main:game_detail',
            kwargs={'pk': self.object.pk}
        )
    

class GameDetailView(DetailView):
    model = Game
    template_name = 'main/game/detail.html'

    def get(self, request, *args, **kwargs):
        game = Game.objects.get(pk=kwargs['pk'])
        for player in game.players.all():
            print(player.username, player.avg_rating)

        return super().get(
            request,
            *args,
            **kwargs
        )


class GameEditView(UpdateView):
    model = Game
    template_name = 'main/game/form.html'
    form_class = GameCreateForm

    def get_queryset(self):
        return Game.objects.filter(
            organizer=self.request.user
        )

    def get_success_url(self):
        return reverse(
            'main:game_detail',
            kwargs={'pk': self.object.pk}
        )


class RegisterView(CreateView):
    model = Player
    template_name = 'main/profile/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:profile')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user=user)

        return super().form_valid(form)


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Player
    template_name = 'main/profile/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Дані користувача змінено'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    

class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin,PasswordChangeView):
    template_name = 'main/profile/password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль користувача змінений'


class PlayerLoginView(LoginView):
    template_name = 'main/profile/login.html'


class PlayerLogoutView(LogoutView):
    pass


@login_required
def game_teams(request, pk: int):
    game = get_object_or_404(Game, pk=pk)
    players = game.players.annotate(average_rating=Avg('received_ratings__rating')).order_by('-average_rating').all()

    max_players_in_team = math.ceil(min(len(players), game.max_players) / game.teams_num)
    teams_players = [[] for i in range(game.teams_num)]
    teams_totals = [0] * game.teams_num

    for player in players[:game.max_players]:
        for i in range(game.teams_num):
            is_not_enough_players = len(teams_players[i]) < max_players_in_team
            is_min_team_rating = teams_totals[i] <= min(teams_totals)

            if is_not_enough_players and is_min_team_rating:
                teams_players[i].append(player)
                teams_totals[i] += player.average_rating or 0
                break

    teams = []

    for i in range(game.teams_num):
        teams.append({
            'id': i + 1,
            'players': teams_players[i],
            'avg_rating': teams_totals[i] / len(teams_players[i]),
            'total_rating': teams_totals[i]
        })

    context = {'teams': teams}
    return render(request, 'main/game/teams.html', context=context)

@login_required
def profile(request):
    return render(request, 'main/profile/profile.html')

@login_required
def players(request):
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'main/players.html', context=context)

@login_required
def player(request, pk: int):
    player = get_object_or_404(Player, pk=pk)
    if player == request.user:
        return redirect('main:profile')
    
    existing = PlayerRating.objects.filter(
        from_player=request.user,
        to_player=player
    ).first()

    if request.method == 'POST':
        form = PlayerRatingForm(request.POST)

        if form.is_valid():
            PlayerRating.objects.update_or_create(
                from_player=request.user,
                to_player=player,
                defaults={
                    'rating': form.cleaned_data['rating']
                }
            )
            messages.success(request=request, message='Оцінку гравця збережено')
        else:
            messages.error(request=request, message='Помилка збереження')
    else:
        initial = {} if not existing else {'rating': existing.rating}
        form = PlayerRatingForm(initial=initial)

    context = {'player': player, 'rating_form': form}
    return render(request, 'main/player.html', context=context)

@login_required
def index(request):
    context = {}
    return render(request, 'main/index.html', context)

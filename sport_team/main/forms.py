from django import forms

from .models import Player, Game, Team


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = (
            'organizer',
            'created_at',
            'players'
        )
    starts_at = forms.SplitDateTimeField(
        label='Дата і час',
        widget=forms.SplitDateTimeWidget(
            date_format='%Y-%m-%d',
            date_attrs={"type": "date"},
            time_attrs={"type": "time"},
        )
    )



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('username', 'password', 'first_name', 'last_name', 'about_me')
        widgets = {
            'password': forms.PasswordInput()
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('username', 'first_name', 'last_name', 'avatar', 'about_me')



RATING_CHOICES = [(i, str(i)) for i in range(0, 11)]

class PlayerRatingForm(forms.Form):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )
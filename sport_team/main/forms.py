from django import forms

from .models import Player, Game, Team


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = (
            'organizer',
            'created_at',
        )


class GameEditForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = (
            'organizer',
            'created_at',
        )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('username', 'password', 'first_name', 'last_name')
        widgets = {
            'password': forms.PasswordInput()
        }


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Ім'я")
    last_name = forms.CharField(required=True, label="Прізвище")

    class Meta:
        model = Player
        fields = ('username', 'first_name', 'last_name', 'avatar')



RATING_CHOICES = [(i, str(i)) for i in range(0, 11)]

class PlayerRatingForm(forms.Form):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )
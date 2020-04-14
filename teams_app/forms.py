from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from user_app.models import MyUser
from teams_app.models import Team, TeamMembers


class CreateTeam(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_picture', 'start_time', 'end_time', 'description','team_picture']
        widgets = {
            'start_time': forms.SelectDateWidget(),
            'end_time': forms.SelectDateWidget(),
        }


class CreateMember(forms.ModelForm):
    class Meta:
        model = TeamMembers
        fields = ['member', 'member_status']
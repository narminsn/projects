from django.db import models
from user_app.models import MyUser
import uuid
from django.utils.translation import ugettext_lazy as _


def token_generator():
    id = uuid.uuid4()
    return str(id)


# Create your models here.
class Team(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    team_picture = models.ImageField(upload_to='team_profile',null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # document = models.FileField(upload_to='documents/')

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f'{self.team_name}'

class TeamDocuments(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return f'{self.team_id}'

class TeamMembers(models.Model):
    team = models.ForeignKey(Team, related_name='files', on_delete=models.CASCADE)
    member = models.ForeignKey(MyUser, related_name='member', on_delete=models.CASCADE)
    member_status = models.CharField(max_length=244)
    is_active = models.BooleanField(_('active'),
                                    default=False,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts.'
                                    ),
                                    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f'{self.team} {self.id}'


class TokenModelTeam(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    create_date = models.DateField(auto_now=True)
    token = models.CharField(max_length=55, default=token_generator)

    def __str__(self):
        return f'{self.user},{self.create_date}'

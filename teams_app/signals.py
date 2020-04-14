from django.db.models.signals import post_save
from django.dispatch import receiver
from teams_app.models import TeamMembers, TokenModelTeam
from teams_app.tasks import send_team_task
from threading import Thread

print('SIGNAL FOR Team VERIFY')


@receiver(post_save, sender=TeamMembers)
def create_token(sender, instance, created, **kwargs):
    print('FROM SIGNAL !')
    if created:
        TokenModelTeam.objects.create(
            user=instance.member
        )
        print('CREATED TOKEN')
        print("FROM SIGNAL 2")


@receiver(post_save, sender=TokenModelTeam)
def user_verify(sender, instance, created, **kwargs):
    if created:
        link = f'http://localhost:8000/verify_team/{instance.token}/{instance.user.id}/'
        background = Thread(target=send_team_task, args=(instance.user.email, link))
        background.start()

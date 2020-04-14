from django.db.models.signals import post_save
from django.dispatch import receiver
from user_app.models import MyUser, TokenModel
from user_app.tasks import send_mail_task
from threading import Thread

print('SIGNAL FOR USER VERIFY')


@receiver(post_save, sender=MyUser)
def create_token(sender, instance, created, **kwargs):
    if created:
        TokenModel.objects.create(
            user=instance
        )


@receiver(post_save, sender=TokenModel)
def user_verify(sender, instance, created, **kwargs):
    if created:
        link = f'http://localhost:8000/verify/{instance.token}/{instance.user.id}/'

        background = Thread(target=send_mail_task, args=(instance.user.email, link))
        background.start()

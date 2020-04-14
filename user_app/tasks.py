from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives


def send_mail_task(to_mail, link):
    subject, from_email, to = 'Aida', 'quluzadef4@gmail.com', to_mail
    text_content = 'Click for Verify account'
    html_content = f'<a href="{link}">Tesdiqlemek ucun bura click edin</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


@shared_task
def add(x, y):
    return x + y

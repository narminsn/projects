import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


def token_generator():
    id = uuid.uuid4()
    return str(id)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    country = models.CharField(_(' country'), max_length=150, blank=True)
    city = models.CharField(_(' city'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
    about = models.TextField(_('about'), blank=True, null=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    profile_photo = models.ImageField(_('profilephoto'), default="default.png", blank=True)
    cover_photo = models.ImageField(_('coverphoto'), blank=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    # aditional fields

    gender = models.BooleanField(choices=(
        (True, "Male"),
        (False, "Female")
    ), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    # def get_following_list(self):
    #     if self.following_list:
    #         return json.loads(self.following_list)
    # def get_followers_list(self):
    #     if self.followers_list:
    #         return json.loads(self.followers_list)


class TokenModel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    create_date = models.DateField(auto_now=True)
    token = models.CharField(max_length=55, default=token_generator)


User = MyUser()

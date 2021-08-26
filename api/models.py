import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.id)+str(instance.username)+str(".")+str(ext)])


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username_validator = ASCIIUsernameValidator() 
    username = models.CharField(
      _('username'),
      max_length=150,
      unique=True,
      validators=[username_validator],
      error_messages={
        'unique': _("A user with that username already exists."),
      }
    )
    email = models.EmailField(_('email address'), blank=True)
    user_img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='reverse_following')
    followees = models.ManyToManyField('self', blank=True, symmetrical=False,  related_name='reverse_followees')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
      verbose_name = _('user')
      verbose_name_plural = _('users')
      db_table = 'users'
      swappable = 'AUTH_USER_MODEL'

    def clean(self):
      super().clean()
      self.email = self.__class__.objects.normalize_email(self.email)


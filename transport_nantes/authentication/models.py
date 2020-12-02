"""Module to create authentication models."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    """Class defining the creation of user and superuser."""

    def create_user(self, email, username, password=None):
        """Create user function."""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(email=self.normalize_email(email), username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Create superuser fonction."""
        user = self.create_user(
            email=self.normalize_email(email),
            password=password, username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

# count=0
# total = User.objects.count()
# def gen_db():
#     global count

#     user = User.objects.get(pk=count)
#     if count < total:
#         count +=1
#         return [user.email, user.username, user.password, user.is_admin, user.is_active, user.is_staff, user.is_superuser]
#     else:
#         return [None, None, None, False, False, False, False]

class Profile(AbstractBaseUser):
    """User model in database."""

    email = models.EmailField(verbose_name="email", max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    # date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Set email_confirmed to True after clicking on validation mail
    email_confirmed = models.BooleanField(default=False)
    # Most user informations
    commune = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=5, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True



# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Rather than insisting the user invent a unique user name, we
#     # courteously create the username for the user, set it to a random
#     # value, and initially set the display_name to the part before the
#     # "@" in the email.  The user can change the display name and
#     # email as s/he sees fit.
#     display_name = models.CharField(max_length=80, blank=True)
#     email_confirmed = models.BooleanField(default=False)
#     # We'll set this to False if the user provides a password.  If
#     # it's true, we should have initialised the password to something
#     # random.  (This is why we don't abandon it altogether and just
#     # check the password.)
#     authenticates_by_mail = models.BooleanField(default=True)

#     # We would like to know something about where people think of
#     # themselves as being attached to.  Note that this is quite
#     # different from where they actually connect from.
#     commune = models.CharField(max_length=100, blank=True)
#     code_postal = models.CharField(max_length=10, blank=True)

#     def __str__(self):
#         if self.email_confirmed:
#             confirmed = "email confirmed"
#         else:
#             confirmed = "confirmation pending"
#         if self.authenticates_by_mail:
#             auth = "authenticates by mail"
#         else:
#             auth = "authenticates by password"
#         return '{email}/[{uid}] / {conf} / {auth} ({commune}, {cp})'.format(
#             email=self.user.email,
#             uid=self.user.pk,
#             conf=confirmed, auth=auth,
#             commune=self.commune, cp=self.code_postal)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

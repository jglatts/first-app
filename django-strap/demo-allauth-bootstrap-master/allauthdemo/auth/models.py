import hashlib
import requests
import faker
import psutil
import time 

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from faker import Faker
from bs4 import BeautifulSoup


try:
    from django.utils.encoding import force_text

except ImportError:
    from django.utils.encoding import force_unicode as force_text
from allauth.account.signals import user_signed_up

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date of pub')
    load_time = psutil.cpu_freq('/')
      

class BlogText(models.Model):
    """ Playing with forms. This will help with POST """
    new_blog = models.CharField(max_length=1200)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=900)
    votes = models.IntegerField(default=0)


class MyUserManager(UserManager):
    """
    Custom User Model manager.

    It overrides default User Model manager's create_user() and create_superuser,
    which requires username field.
    """

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User instances represent a user on this site.

    Important: You don't have to use a custom user model. I did it here because
    I didn't want a username to be part of the system and I wanted other data
    to be part of the user and not in a separate table. 

    You can avoid the username issue without writing a custom model but it
    becomes increasingly obtuse as time goes on. Write a custom user model, then
    add a custom admin form and model.

    Remember to change ``AUTH_USER_MODEL`` in ``settings.py``.
    """

    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=14, blank=True, null=True, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    def get_absolute_url(self):
        # TODO: what is this for?
        return "/users/%s/" % urlquote(self.email)  # TODO: email ok for this? better to have uuid?

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.display_name:
            return self.display_name
        return 'You'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])  # like "Andrew E"
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'You'
        self.display_name = dn.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email

    def natural_key(self):
        return self.email

    def dr_scrap(self):
        """ Get the news heading from the middle column @ drudgerp """
        if self.display_name:
            pass
        else:
            url = "https://www.drudgereport.com"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            src = requests.get(url)
            pln_txt = src.text
            dasoup = BeautifulSoup(pln_txt, "html.parser")
            
            for news in dasoup.find_all("div",{"id":"app_col2"}):
                tits = news.get_text()
                return tits

    def mo_scrap(self):
        """ Another Scrap """
        if self.display_name:           
            pass
        else:
            url = "https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            src = requests.get(url, headers = headers)
            pln_txt = src.text
            dasoup = BeautifulSoup(pln_txt, "html.parser")
            
            # Had a hard time extracting data. This loop finds ALOT of articles 
            # on google news, trying to limit the amount of results. 
            all_news = dasoup.find_all("main",{"class":"HKt8rc CGNRMc"}, limit=1)
            for news in all_news:
                return news.get_text()

    def odd_scrap(self):
        """ Scrap random gear from odditymall
            Have to clean scrap up, too much is displayed
        """
        if self.display_name:           
            pass
        else:
            url = "https://www.odditymall.com"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            src = requests.get(url, headers = headers)
            pln_txt = src.text
            dasoup = BeautifulSoup(pln_txt, "html.parser")
            
            #Extracting data 
            all_news = dasoup.find_all("div",{"class":"list-item-inner-cont"})
            for news in all_news:
                return news.get_text()

    def load_time():
        # data to display on question page
        now0 = time.time()
        now1 = time.time()
        speed = now1 - now0
    
        return speed

    def fake_name(self):
        """ Fun script to generate fake data for webpage """
        fake = Faker()
        return fake.name()
        
    def fake_ssn(self):
        """ Fun script to generate fake data for webpage """
        fake = Faker()
        return fake.ssn()

    def fake_address(self):
        """ Fun script to generate fake data for webpage """
        fake = Faker()
        return fake.address()
        
    def fake_job(self):
        """ Fun script to generate fake data for webpage """
        fake = Faker()
        return fake.job()

    def utils_times(self):
        """ Return some data about user's CPU time """
        stat = psutil.cpu_times()
        return stat
        
    def utils_users(self):
        """ Return some data about user's machine """
        stat = psutil.users()
        return stat

    def utils_boot(self):
        """ Return some data about user's machine """
        stat = psutil.boot_time()
        return stat

@python_2_unicode_compatible
class UserProfile(models.Model):
    """Profile data about a user.
    Certain data makes sense to be in the User model itself, but some
    is more "profile" data than "user" data. I think this is things like
    date-of-birth, favourite colour, etc. If you have domain-specific
    profile information you might create additional profile classes, like
    say UserGeologistProfile.
    """
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)

    # I oscillate between whether the ``avatar_url`` should be
    # a) in the User model
    # b) in this UserProfile model
    # c) in a table of it's own to track multiple pictures, with the
    #    "current" avatar as a foreign key in User or UserProfile.
    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    dob = models.DateField(verbose_name="dob", blank=True, null=True)

    def __str__(self):
        return force_text(self.user.email)

    class Meta():
        db_table = 'user_profile'


@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    preferred_avatar_size_pixels = 256

    picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
        preferred_avatar_size_pixels
    )

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            user.first_name = name.split()[0]
            user.last_name = name.split()[1]

        if sociallogin.account.provider == 'facebook':
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']
            # verified = sociallogin.account.extra_data['verified']
            picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                sociallogin.account.uid, preferred_avatar_size_pixels)

        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']
            # verified = sociallogin.account.extra_data['verified_email']
            picture_url = sociallogin.account.extra_data['picture']

    profile = UserProfile(user=user, avatar_url=picture_url)
    profile.save()

    user.guess_display_name()
    user.save()

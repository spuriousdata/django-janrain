from django.contrib.auth.models import User
from hashlib import sha1
from base64 import b64encode


class JanrainBackend(object):

    def authenticate(self, profile):
        # django.contrib.auth.models.User.username is required and 
        # has a max_length of 30 so to ensure that we don't go over 
        # 30 characters we base64 encode the sha1 of the identifier 
        # returned from janrain 
        hashed_user = b64encode(sha1(profile['identifier']).digest())
        try :
            u = User.objects.get(username=hashed_user)
        except User.DoesNotExist:
            u = User(
                    username=hashed_user,
                    password='',
                    first_name=profile.get('name').get('givenName'),
                    last_name=profile.get('name').get('familyName'),
                    email=profile.get('email')
                )
            u.is_active = True
            u.is_staff = False
            u.is_superuser = False
            u.save()
        return u

    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None

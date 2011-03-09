##############
django-janrain
##############

Janrain integration into Django using built-in django.contrib.auth package. It
creates a django user using django.contrib.auth.models.User on first login and
retrieves that User object on future logins.

============
Installation
============

Add a url entry in ``urls.py``::

	urlpatterns += patterns('',
		(r'^janrain/', include('janrain.urls')),
	)

Add ``janrain`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'djangoratings',
	)

Add ``janrain.backends.JanrainBackend`` to ``AUTHENTICATION_BACKENDS``::

	# put janrain.backends.JanrainBackend first
	AUTHENTICATION_BACKENDS = (
		'janrain.backends.JanrainBackend',
		'django.contrib.auth.backends.ModelBackend',
	)

Add your janrain api key to ``settings``::

	JANRAIN_RPX_API_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef"

=====
Usage
=====

Configure your ``token_url`` in janrain to be http://yoursite.com/janrain/login/

Create a template called ``janrain/loginpage.html`` to contain your janrain
login iframe::

	<iframe src="http://yoursite.rpxnow.com/openid/embed?token_url=http{% if request.is_secure()%}s{%endif%}{{("://" + request.get_host() + "/janrain/login/?redirect_to=" + next)|urlencode}}" scrolling="no" frameBorder="no" allowtransparency="true" style="width:400px;height:240px"></iframe>

Place your javascript overlay sign in buttons in your template::
	<a class="rpxnow" onclick="return false;"
		href="https://yoursite.rpxnow.com/openid/v2/signin?token_url=http{% if request.is_secure()%}s{%endif%}{{("://" + request.get_host() + "/janrain/login/?redirect_to=" + 'http://yoursite.com/redirect/to/path/')|urlencode}}">Sign In</a>

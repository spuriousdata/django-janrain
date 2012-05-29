from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.dispatch import Signal

from janrain import api
from janrain.models import JanrainUser

class JanrainSignal(object):
    pass

pre_login         = Signal(providing_args=['request'])
post_profile_data = Signal(providing_args=['profile_data'])
post_authenticate = Signal(providing_args=['user', 'profile_data'])
post_janrain_user = Signal(providing_args=['janrain_user', 'profile_data'])
post_login        = Signal(providing_args=['user', 'profile_data'])
pre_redirect      = Signal(providing_args=['type', 'redirect'])
login_failure     = Signal(providing_args=['message','data'])

pre_logout        = Signal(providing_args=['request'])
logout            = Signal(providing_args=['request'])


@csrf_exempt
def login(request):
    pre_login.send(JanrainSignal, request=request)
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        login_failure.send(JanrainSignal, message='Error retreiving token', data=None)
        return HttpResponseRedirect('/')

    try:
        profile = api.auth_info(token)
    except api.JanrainAuthenticationError:
        login_failure.send(JanrainSignal, message='Error retreiving profile', data=None)
        return HttpResponseRedirect('/')
    post_profile_data.send(JanrainSignal, profile_data=profile)

    u = None
    p = profile['profile']
    u = auth.authenticate(profile=p)
    post_authenticate.send(JanrainSignal, user=u, profile_data=profile)

    juser = JanrainUser.objects.get_or_create(
                user=u,
                username=p.get('preferredUsername'),
                provider=p.get('providerName').lower(),
                identifier=p.get('identifier'),
                avatar=p.get('photo'),
                url=p.get('url'),
            )[0]
    juser.save()
    post_janrain_user.send(JanrainSignal, janrain_user=juser, profile_data=profile)

    if u is not None:
        request.user = u
        auth.login(request, u)
        post_login.send(JanrainSignal, user=u, profile_data=profile)

    try:
        redirect = pre_redirect.send(JanrainSignal, type='login', 
                redirect=request.GET.get('next', '/'))[-1][1]
    except IndexError:
        redirect = '/'
    return HttpResponseRedirect(redirect)

def logout(request):
    pre_logout.send(JanrainSignal, request=request)
    auth.logout(request)
    try:
        redirect = pre_redirect.send(JanrainSignal, type='logout', 
                redirect=request.GET.get('next', '/'))[-1][1]
    except IndexError:
        redirect = '/'
    return HttpResponseRedirect(redirect)

def loginpage(request):
    context = {'next':request.GET['next']}
    return render_to_response(
        'janrain/loginpage.html',
        context,
        context_instance=RequestContext(request)
    )
    

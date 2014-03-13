from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

from janrain import api
from janrain.models import JanrainUser
from janrain.signals import *

@csrf_exempt
def login(request):
    pre_login.send(JanrainSignal, request=request)
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        login_failure.send(JanrainSignal, message='Error retrieving token', data=None)
        return HttpResponseRedirect('/')

    try:
        profile = api.auth_info(token)
    except api.JanrainAuthenticationError:
        login_failure.send(JanrainSignal, message='Error retrieving profile', data=None)
        return HttpResponseRedirect('/')
    post_profile_data.send(JanrainSignal, profile_data=profile)

    u = None
    p = profile['profile']
    u = auth.authenticate(profile=p)
    post_authenticate.send(JanrainSignal, user=u, profile_data=profile)

    juser, created = JanrainUser.objects.get_or_create(user=u)
    juser.username = p.get('preferredUsername')
    juser.provider = p.get('providerName').lower()
    juser.identifier = p.get('identifier')
    juser.avatar = p.get('photo')
    juser.url = p.get('url')
    juser.save()
    post_janrain_user.send(JanrainSignal, janrain_user=juser, profile_data=profile)

    if u is not None:
        request.user = u
        auth.login(request, u)
        post_login.send(JanrainSignal, user=u, profile_data=profile)

    next = request.GET.get('next', '/')
    try:
        redirect = pre_redirect.send(JanrainSignal, type='login',
                redirect=next)[-1][1]
    except IndexError:
        redirect = next
    return HttpResponseRedirect(redirect)

def logout(request):
    pre_logout.send(JanrainSignal, request=request)
    auth.logout(request)
    next = request.GET.get('next', '/')
    try:
        redirect = pre_redirect.send(JanrainSignal, type='logout',
                redirect=next)[-1][1]
    except IndexError:
        redirect = next
    return HttpResponseRedirect(redirect)

def loginpage(request):
    context = {'next':request.GET.get('next', '/')}
    return render_to_response(
        'janrain/loginpage.html',
        context,
        context_instance=RequestContext(request)
    )
    

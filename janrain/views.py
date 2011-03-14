from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

from janrain import api

@csrf_exempt
def login(request):
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        return HttpResponseRedirect('/')

    auth_info = api.auth_info(token)

    u = None
    if auth_info['stat'] == 'ok':
        profile = auth_info['profile']
        u = auth.authenticate(profile=profile)

    if u is not None:
        request.user = u
        auth.login(request, u)
    try:
        return HttpResponseRedirect(request.GET['redirect_to'])
    except KeyError:
        return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    try:
        return HttpResponseRedirect(request.GET['redirect_to'])
    except KeyError:
        return HttpResponseRedirect('/')

def loginpage(request):
    context = {'next':request.GET['next']}
    return render_to_response(
        'janrain/loginpage.html',
        context,
        context_instance=RequestContext(request)
    )
    

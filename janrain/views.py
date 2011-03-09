from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

import urllib, urllib2, json

@csrf_exempt
def login(request):
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        return HttpResponseRedirect('/')

    api_params = {
        'token': token,
        'apiKey': settings.JANRAIN_RPX_API_KEY,
        'format': 'json',
    }

    janrain_response = urllib2.urlopen(
            "https://rpxnow.com/api/v2/auth_info",
            urllib.urlencode(api_params))
    resp_json = janrain_response.read()
    auth_info = json.loads(resp_json)

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
    

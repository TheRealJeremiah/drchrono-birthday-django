from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import json

def login(request):
    token = json.loads(request.user.social_auth.values_list('extra_data')[0][0])['access_token']
    context = RequestContext(request, {
        'request': request, 'user': request.user, 'token': token})
    return render_to_response('login.html', context_instance=context)
    # return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')

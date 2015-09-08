from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
# from django.template.context import RequestContext
from django.http import JsonResponse
from datetime import date
import json, requests, pdb

def login(request):
    # token = json.loads(request.user.social_auth.values_list('extra_data')[0][0])['access_token']
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user, 'token': token})
    # return render_to_response('login.html', context_instance=context)
    return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def patients(request):
    # we parse the drchrono data in the backend so as not to send unnecessary data to the frontend
    if request.user.is_anonymous():
        return JsonResponse({})
    token = json.loads(request.user.social_auth.values_list('extra_data')[0][0])['access_token']
    url = 'https://drchrono.com/api/patients'
    auth = 'Bearer ' + token
    data = requests.get(url, headers={'Authorization': auth}).json()
    parsed = map(parse_patient, data['results'])
    return JsonResponse(parsed, safe=False)

def parse_patient(patient):
    if patient['date_of_birth']:
        hasBday = True
        bday = "-".join([str(date.today().year)] + patient['date_of_birth'].split('-')[1:])
    else:
        hasBday = False
        bday = '1970-01-01'
    return {'title': patient['first_name'],
            'email': patient['email'],
            'start': bday,
            'has_birthday': hasBday}

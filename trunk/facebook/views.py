from django.shortcuts import render
from fbmanager import FacebookManager
from django.http import HttpResponse
import json

# Create your views here.
PAGE = '217907011622497' #static for now
fbmanager = FacebookManager()
def fanpage_age_sex(request):
    result = fbmanager.get_likes_sex_age(PAGE)
    return HttpResponse(json.dumps(result))

def get_long_lived_token(request):
    vars = request.GET
    result = fbmanager.get_long_lived_token(vars.get('token'))
    return HttpResponse(json.dumps(result))

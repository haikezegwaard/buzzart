from django.shortcuts import render_to_response
from django.template import RequestContext



# Create your views here.
def index(request):

    bar = 3
    return render_to_response('template.html', {'foo' : bar}, context_instance=RequestContext(request))
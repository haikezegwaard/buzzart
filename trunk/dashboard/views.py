from django.template import RequestContext
from django.shortcuts import render_to_response
import json
from django.http import HttpResponse,Http404

# Create your views here.
def index(request):
    return render_to_response("index.html",context_instance = RequestContext(request))

def javamap(request):
    """
    Demo view function for usage in highcharts
    """

    #if request.is_ajax():
    years = ["2012","2013"]
    months = [[12,14,13,15,17,16,14,31,21,11,17,19],[12,19,10,13,40]]
    ranges = []
    for n in range (0,12):
        ranges.append([9,16])
    series = []
    for i,j in enumerate(years):
        series.append({
            'name':years[i],
            'data':months[i],
            'zIndex' : '1'
        })
    series.append({'name':'range','zIndex':'0','fillOpacity': '0.3','type':'arearange','linkedTo': ':previous','data':ranges})
    return HttpResponse(json.dumps(series), mimetype='application/json')
    #raise Http404
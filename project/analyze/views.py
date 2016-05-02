from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import json

# this is the input page
def index(request):
    context = {
        'stuff': "print me!",
    }
    return render(request, 'analyze/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

# this is the results page 
def results(request):
	data = callBackend(request.POST)
	print(type(data))
	print(json.dumps(data))
	return render(request, 'analyze/results.html', {'data': json.dumps(data)})

# this is basically a controller/handler - it's the destination of index (which has the input form), 
# it does some logic, and then redirects to the results page 
def upload(request):
    try:
    	data = callBackend(request.POST)
        
    	# make fieldNameOfData a static variable
        dataField = request.POST['fieldNameOfData']
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'analyze/index.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('analyze:index'))

def callBackend(data):
	return HARDCODED_JSON

HARDCODED_JSON = {
	"apps":[
		{
			"name":"facebook",
			"components":["a","b","c","l","k"]
		},
		{
			"name":"bob",
			"components":["e","f","g"]
		},
		{
			"name":"evernote",
			"components":["x","xc","xz","xv","xs","xa","xg","xw","xr","xy","xu"]
		}
	],
	"covert":
	[
		{"start":"a","end":"g"},
		{"start":"c","end":"f"},
		{"start":"x","end":"f"},
		{"start":"xc","end":"k"},
		{"start":"xz","end":"l"},
		{"start":"xv","end":"b"},
		{"start":"xa","end":"e"},
		{"start":"xw","end":"f"},
		{"start":"xw","end":"e"}
	],
	"didfail":
	[
		{"start":"a","end":"g"},
		{"start":"c","end":"f"}
	]
}

"""
def visualization(request, nodesJson, linksJson):
    return RenderTemplate(nodesJson, linksJson)

"""
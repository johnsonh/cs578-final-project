from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import json
import os

from models import Document
from forms import DocumentForm
from django.shortcuts import render_to_response
from django.template import RequestContext

import parser

media_dir = "/media/apks"

# OLD INPUT PAGE
def index(request):
	context = {
		'stuff': "print me!",
	}
	return render(request, 'analyze/index.html', context)

# OLD RESULT PAGE
def results(request):
	try:
		data = callBackend(request.POST)
	except (KeyError):
		# Redisplay the question voting form.
		return render(request, 'analyze/index.html', {
			'error_message': "You didn't select a choice.",
		})
	else:		
		return render(request, 'analyze/results.html', {'data': json.dumps(data)})

# this is the results page 
def results(request):
	data = callBackend(request.POST)
	print(type(data))
	print(json.dumps(data))
	return render(request, 'analyze/results.html', {'data': json.dumps(data)})

def callBackend(data):
	return HARDCODED_JSON

###################

# New input page
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('analyze/list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    deleteAllDocs(documents)
    
    # Render list page with the documents and the form
    return render_to_response(
        'analyze/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

# just for cleaning up 
def deleteAllDocs(documents):
    for doc in documents:
    	doc.delete()


# new result page
def visualization(request):
	try:
		data = getAnalysisJson('/root/cs578/final/project' + media_dir)
		request.session['data'] = data
	except (KeyError):
		# Redisplay the question voting form.
		return render(request, 'analyze/index.html', {
			'error_message': "You didn't select a choice.",
		})
	else:		
		return render(request, 'analyze/visualization.html', {'data': json.dumps(data)})

def feedback(request):
	return render(request, 'analyze/feedback.html', {'data': json.dumps(request.session['data'])})

def getAnalysisJson(path):
	print("Directory is: " + path)
	resultJson = parser.analyze(path)	
	# dirs = os.listdir( path )
	# print("files in dir are: " + str(dirs))
	return resultJson
	# return HARDCODED_JSON


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

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import json

from models import Document
from forms import DocumentForm
from django.shortcuts import render_to_response
from django.template import RequestContext


# this is the input page
def index(request):
	context = {
		'stuff': "print me!",
	}
	print("dfdfd")
	return render(request, 'analyze/index.html', context)


def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)

# this is the results page 
def results(request):
	try:
		data = callBackend(request.POST)
		print(type(data))
		print(json.dumps(data))
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'analyze/index.html', {
			'error_message': "You didn't select a choice.",
		})
	else:		
		return render(request, 'analyze/results.html', {'data': json.dumps(data)})

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['uploadedFile'])
            print(newdoc)
            newdoc.save()

            print("yayayay")
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('analyze/list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    print("fuck")
    # Render list page with the documents and the form
    return render_to_response(
        'analyze/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

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
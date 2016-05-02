from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

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
	return render(request, 'analyze/results.html', {'data': data})

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
	return { 'dictionaryKey1': 'dictionaryValue1' }

"""
def visualization(request, nodesJson, linksJson):
    return RenderTemplate(nodesJson, linksJson)

"""
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'stuff': "print me!",
    }
    return render(request, 'analyze/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % 67)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


"""
def visualization(request, nodesJson, linksJson):
    return RenderTemplate(nodesJson, linksJson)

"""
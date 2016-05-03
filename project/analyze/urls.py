
from django.conf.urls import url

from . import views

app_name = 'analyze'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/results/
    url(r'^results/$', views.results, name='results'),
    url(r'^results2/$', views.results2, name='results2'),
    url(r'^list/$', views.list, name='list'),
]
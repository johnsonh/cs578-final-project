
from django.conf.urls import url

from . import views

app_name = 'analyze'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/results/
    url(r'^results/$', views.results, name='results'),
    url(r'^visualization/$', views.visualization, name='visualization'),
    url(r'^list/$', views.list, name='list'),
]
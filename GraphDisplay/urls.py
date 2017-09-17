from django.conf.urls import url

from . import views

app_name = 'GraphDisplay'
urlpatterns = [
    url(r'jobs/new$', views.GraphJobCreateView.as_view(), name='job_new'),
    url(r'jobs/(?P<pk>[0-9]+)/view$', views.GraphJobDetailView.as_view(), name='job_view'),
    url(r'jobs/(?P<pk>[0-9]+)/edit$', views.GraphJobUpdateView.as_view(), name='job_form'),
    url(r'jobs/(?P<pk>[0-9]+)/delete$', views.GraphJobDeleteView.as_view(), name='job_delete'),
    url(r'^$', views.GraphJobManageView.as_view(), name='dashboard'),

    url(r'graphs/new$', views.ALFileCreateView.as_view(), name='graph_new'),
    url(r'graphs/$', views.ALFileManageView.as_view(), name='graphs'),
    url(r'graphs/(?P<pk>[0-9]+)/update$', views.ALFileUpdateView.as_view(), name='graph_update'),
    url(r'graphs/(?P<pk>[0-9]+)/delete$', views.ALFileDeleteView.as_view(), name='graph_delete'),
]
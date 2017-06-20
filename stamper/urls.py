from django.conf.urls import url

from stamper import views

urlpatterns = [
    url(r'^pages/$', views.page_list),
    url(r'^pages/(?P<pk>[0-9]+)/$', views.page_detail),
]

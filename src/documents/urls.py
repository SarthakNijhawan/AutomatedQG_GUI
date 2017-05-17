from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_redirect),
    url(r'^home/$', views.home_page, name='home_page'),
    url(r'^(?P<slug>[\w-]+)/$', views.doc_detail, name='doc_detail'),
    url(r'^create_from_a_file/$', views.doc_create, name='doc_create'),
    url(r'^create_online/$', views.doc_online_create, name='doc_online_create'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.doc_edit, name='doc_edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.doc_delete, name='doc_delete'),
    url(r'^questions/create', views.question_create, name="ques_create"),
]

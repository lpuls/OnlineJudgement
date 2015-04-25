from django.conf.urls import patterns, include, url

from django.contrib import admin
from OJ.views import hi, questions, upload
from OJ.models import index, question
import os
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Judgement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hi/',hi),
    url(r'index/', index),
    url(r'upload/', upload),
    url(r'question/', question),
    url(r'questions/', questions),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.dirname(os.path.dirname(__file__)) + '/media'})
)

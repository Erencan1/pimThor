from django.conf.urls import url
from .CreateCFunction import indexCF
from .views import index, cellGraphs, myTests, search, test_main_page
from django.conf import settings
from django.conf.urls.static import static
from .viewsLogin import login_page, log_out


urlpatterns = [
    url(r'^$', index),
    url(r'^cf/$', indexCF),
    url(r'^mytests/$', myTests, name='mytests'),
    url(r'^mytests/(?P<test_id>[0-9]+)/$', myTests, name='mytests_test_id'),
    url(r'^tests/$', myTests, name='tests'),
    url(r'^tests/(?P<test_id>[0-9]+)/$', myTests, name='tests_test_id'),
    url(r'^detail/$', test_main_page),
    url(r'^search/$', search),

    url(r'^(?P<cell_id>[0-9]+)/$', cellGraphs),

    url(r'^login/$', login_page),
    url(r'^logout/$', log_out),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
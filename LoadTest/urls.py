from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import index, my_load_tests, load_tests, load_search, index_load_test, cell_graphs


urlpatterns = [
    url(r'^$', index),
    url(r'^myloadtests/$', my_load_tests),
    url(r'^loadtests/$', load_tests),
    url(r'^loadsearch/$', load_search),
    url(r'^loadtest/$', index_load_test),
    url(r'^loadtest/cell/$', cell_graphs),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
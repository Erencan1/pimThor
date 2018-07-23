from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'', include('home3.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^loadTest/', include('LoadTest.urls')),
]

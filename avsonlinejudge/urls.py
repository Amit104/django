from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('avs.urls')),
    url(r'^avs/', include('avs.urls')),
]

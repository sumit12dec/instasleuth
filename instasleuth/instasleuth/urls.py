from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^extract_pan_data/', 'instasleuth.views.get_pan_data', name='get_pan_data'),
    url(r'^cloud_extract_data/', 'instasleuth.views.cloud_extract_data', name='cloud_extract_data'),

]

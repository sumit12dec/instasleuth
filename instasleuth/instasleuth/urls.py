from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^extract_pan_data/', 'instasleuth.views.get_pan_data', name='get_pan_data'),
    url(r'^cloud_extract_data/', 'instasleuth.views.cloud_extract_data', name='cloud_extract_data'),
    url(r'^user_data/', 'instasleuth.views.user_data', name='user_data'),
    url(r'^user_points/', 'instasleuth.views.user_points', name='user_points'),

]

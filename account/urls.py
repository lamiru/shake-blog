from django.conf.urls import include, url

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'', include('django.contrib.auth.urls')),
]

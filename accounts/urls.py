from django.conf.urls import include, url
from accounts.views import SignupView


urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'', include('django.contrib.auth.urls')),
]

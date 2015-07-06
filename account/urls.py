from django.conf.urls import include, url
from account.views import SignupView


urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'account/login.html'}, name='login'),
    url(r'', include('django.contrib.auth.urls')),
]

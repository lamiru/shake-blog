from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='blog:index'), name='root'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),  # noqa
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),
]

if settings.DEBUG and settings.MEDIA_URL.startswith('/'):
    media_url = settings.MEDIA_URL.strip('/')               # '/media/' -> 'media'  # noqa
    media_url_pattern = '^' + media_url + '/(?P<path>.*)$'  # '^media/(?P<path>.*)$'  # noqa
    urlpatterns += [
        url(media_url_pattern, 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

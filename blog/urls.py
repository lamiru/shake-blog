from django.conf.urls import patterns, url


urlpatterns = patterns(
    'blog.views_cbv',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<id>\d+)/$', 'detail', name='post_detail'),
    url(r'^new/$', 'new', name='post_new'),
    url(r'^(?P<id>\d+)/edit/$', 'edit', name='post_edit'),
    url(r'^(?P<id>\d+)/delete/$', 'delete', name='post_delete'),
    url(r'^(?P<id>\d+)/comments/new/$', 'comment_new', name='comment_new'),
    url(r'^(?P<id>\d+)/comments/(?P<comment_id>\d+)/edit/$', 'comment_edit',
        name='comment_edit'),
)

urlpatterns += patterns(
    'blog.views',
    url(r'^(?P<id>\d+)/comments/(?P<comment_id>\d+)/delete/$',
        'comment_delete', name='comment_delete'),
)

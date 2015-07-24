from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from blog.signals import app_ready


def on_app_ready(sender, **kwargs):
    def is_follow(self, to_user):
        if (self.id is not None) and (to_user.id is not None):
            return self.following_set.filter(to_user=to_user).exists()
        return False
    setattr(get_user_model(), 'is_follow', is_follow)

    def follow(self, to_user):
        if self.id is None:
            raise ValueError('Save {} model instance to DB first.'.format(self))  # noqa
        if not self.is_follow(to_user):
            self.following_set.create(to_user=to_user)
    setattr(get_user_model(), 'follow', follow)

    def unfollow(self, to_user):
        if self.id is None:
            raise ValueError('Save {} model instance to DB first.'.format(self))  # noqa
        self.following_set.filter(to_user=to_user).delete()
    setattr(get_user_model(), 'unfollow', unfollow)

    def following_summary(self):
        count = self.following_set.all().count()
        return ungettext('%(count)d post (single)', '%(count)d posts (plural)', count) % {  # noqa
            'count': count,
        }

    setattr(AnonymousUser, 'is_follow', lambda *args: False)
    setattr(AnonymousUser, 'follow', lambda *args: None)
    setattr(AnonymousUser, 'unfollow', lambda *args: None)

app_ready.connect(on_app_ready)


class UserFollow(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')  # noqa
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_set')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))  # noqa
    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    attached_image = models.ImageField(blank=True, default='', verbose_name=_('attached_image'))  # noqa
    lnglat = models.CharField(max_length=50, default='', verbose_name=_('lnglat'))  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.author.username, self.id])  # noqa

    @property
    def lng(self):
        if self.lnglat:
            return self.lnglat.split(',')[0]

    @property
    def lat(self):
        if self.lnglat:
            return self.lnglat.split(',')[1]


class Comment(models.Model):
    post = models.ForeignKey(Post)
    message = models.TextField(verbose_name=_('message'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def as_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

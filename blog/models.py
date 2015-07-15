from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


def author_is_follow(from_user, to_user):
    if from_user.is_authenticated() and to_user.is_authenticated():
        return from_user.following_set.filter(to_user=to_user).exists()
    return False


def author_follow(from_user, to_user):
    if not author_is_follow(from_user, to_user):
        from_user.following_set.create(to_user=to_user)


def author_unfollow(from_user, to_user):
    from_user.following_set.filter(to_user=to_user).delete()


class UserFollow(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')  # noqa
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_set')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    lnglat = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

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
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def as_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

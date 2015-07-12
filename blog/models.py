from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


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

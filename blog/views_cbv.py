from django.views.generic import ListView, DetailView
from blog.models import Post
from blog.forms import CommentForm


index = ListView.as_view(model=Post, template_name='blog/index.html')


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

detail = PostDetailView.as_view()

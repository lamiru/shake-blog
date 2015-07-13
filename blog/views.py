from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView   # noqa
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from blog.mixins import FormValidMessageMixin


index = ListView.as_view(model=Post)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

detail = PostDetailView.as_view()


class PostCreateView(FormValidMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    form_valid_message = 'Added a new post.'

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

new = login_required(PostCreateView.as_view())


class PostUpdateView(FormValidMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    form_valid_message = 'Edited a post.'

edit = login_required(PostUpdateView.as_view())


class PostDeleteView(FormValidMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    form_valid_message = 'Deleted a post.'

delete = PostDeleteView.as_view()


class CommentCreateView(FormValidMessageMixin, CreateView):
    form_class = CommentForm
    form_valid_message = 'Added a new comment.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        if self.request.is_ajax():
            return self.object

        return super(CommentCreateView, self).form_valid(form)

comment_new = CommentCreateView.as_view()


class CommentUpdateView(FormValidMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    form_valid_message = 'Edited a new comment.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(FormValidMessageMixin, DeleteView):
    model = Comment
    form_valid_message = 'Deleted a comment.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_delete = CommentDeleteView.as_view()

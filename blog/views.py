from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView   # noqa
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from blog.mixins import FormValidMessageMixin


index = ListView.as_view(
    model=get_user_model(),
    context_object_name='author_list',
    template_name='blog/author_list.html'
)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['author'] = self.object.author
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
        return reverse(self.object.post.get_absolute_url())

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
        return reverse(self.object.post.get_absolute_url())

comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(FormValidMessageMixin, DeleteView):
    model = Comment
    form_valid_message = 'Deleted a comment.'

    def get_success_url(self):
        return reverse(self.object.post.get_absolute_url())

comment_delete = CommentDeleteView.as_view()


class AuthorHomeView(ListView):
    model = Post

    def get_queryset(self):
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['username'])  # noqa
        qs = super(AuthorHomeView, self).get_queryset()
        return qs.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super(AuthorHomeView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

author_home = AuthorHomeView.as_view()


@login_required
def author_follow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    if not author.follower_set.filter(from_user=request.user).exists():
        messages.info(request, 'Followed.')
        author.follower_set.create(from_user=request.user)
    else:
        messages.warning(request, 'Aleady followed this user.')
    return redirect('blog:author_home', username)


@login_required
def author_unfollow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    author.follower_set.filter(from_user=request.user).delete()
    messages.info(request, 'Unfollowed.')
    return redirect('blog:author_home', username)

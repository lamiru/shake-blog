from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post
from blog.forms import PostForm, CommentForm


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


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

    def form_valid(self, form):
        response = super(PostCreateView, self).form_valid(form)
        messages.info(self.request, 'Added a new post.')
        return response

new = PostCreateView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'id'
    template_name = 'blog/form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

    def form_valid(self, form):
        response = super(PostUpdateView, self).form_valid(form)
        messages.info(self.request, 'Edited a post.')
        return response

edit = PostUpdateView.as_view()


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'blog/post_delete_confirm.html'
    success_url = reverse_lazy('blog:index')

    def delete(self, request, *args, **kwargs):
        response = super(PostDeleteView, self).delete(request, *args, **kwargs)
        messages.error(self.request, 'Delete a post.')
        return response

delete = PostDeleteView.as_view()


class CommentCreateView(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        if self.request.is_ajax():
            return self.object

        messages.info(self.request, 'Added a new comment.')

        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_new = CommentCreateView.as_view()

from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import PostForm, CommentForm
from blog.models import Post


def index(request):
    post_list = Post.objects.all().order_by('-id')
    return render(request, 'blog/index.html', {
        'post_list': post_list,
    })


def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', post.id)
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })


def edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {
        'form': form,
    })


def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/post_delete_confirm.html', {
        'post': post,
    })


def comment_new(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id)
    else:
        form = CommentForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })

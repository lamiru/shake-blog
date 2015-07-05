from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from django.contrib import messages


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
            messages.info(request, 'Added a new post.')
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
            messages.info(request, 'Edited a post.')
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
        messages.error(request, 'Deleted a post.')
        return redirect('blog:index')
    return render(request, 'blog/post_delete_confirm.html', {
        'post': post,
    })


def comment_new(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.info(request, 'Added a new comment.')
            return redirect('blog:post_detail', id)
    else:
        form = CommentForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })


def comment_edit(request, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.info(request, 'Edited a comment.')
            return redirect('blog:post_detail', id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/form.html', {
        'form': form,
    })


def comment_delete(request, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id)

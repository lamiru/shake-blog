from django.shortcuts import redirect, render
from blog.forms import PostForm
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
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })

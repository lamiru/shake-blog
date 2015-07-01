from django.shortcuts import redirect, render
from blog.forms import PostForm


def index(request):
    return render(request, 'blog/index.html', {
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

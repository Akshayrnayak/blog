from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        author = request.POST.get('author')
        text = request.POST.get('text')

        Comment.objects.create(post=post, author=author, text=text)
        return redirect('post_detail', pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.text = request.POST.get('text')

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()
        return redirect('post_detail', pk=pk)

    return render(request, 'blog/post_edit.html', {'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

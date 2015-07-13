from django import forms
from blog.models import Post, Comment
from blog.widgets import PointWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'lnglat': PointWidget,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', )
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

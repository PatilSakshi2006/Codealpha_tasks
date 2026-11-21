from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        widgets = {"content": forms.Textarea(attrs={"rows": 3, "placeholder": "What's on your mind?"})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {"content": forms.TextInput(attrs={"placeholder": "Write a comment..."})}

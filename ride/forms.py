from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    """
    The class uses the Comment model
    and displays the body field on the form.
    """
    class Meta:
        model = Comment
        fields = ('body',)
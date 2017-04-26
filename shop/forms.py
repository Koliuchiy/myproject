from django import forms
from .models import Comment

class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100)
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

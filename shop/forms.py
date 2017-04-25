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

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data

    def save(self):
        cleaned_data = super(CommentForm, self).clean()

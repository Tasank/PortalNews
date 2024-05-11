from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',

        ]

    def clean(self):

        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 40:
            raise ValidationError({
                "text": "Описание не может быть менее 40 символов."
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )
        return cleaned_data
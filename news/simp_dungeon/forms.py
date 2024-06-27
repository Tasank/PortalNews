from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'category', 'author',]
        widgets = {
            'type': forms.HiddenInput(),  # Скрываем, так как значение будет устанавливаться автоматически
        }


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

# Форма для админ-панели
class GlassForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Post
        fields = '__all__'

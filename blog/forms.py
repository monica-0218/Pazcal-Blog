from django import forms
from .models import Post, Dungeon, Comment

class CreatePostForm(forms.ModelForm):
    dungeon = forms.ModelMultipleChoiceField(label='ダンジョン', queryset=Dungeon.objects, widget=forms.CheckboxSelectMultiple())
    thumbnail = forms.ImageField(label='サムネ',widget=forms.ClearableFileInput(attrs={'onchange': 'previewImage(this);'},))

    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'tags', 'content')

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

from django.db import models
from markdown import markdown
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
from django.conf import settings

class Dungeon(models.Model):
    img = models.ImageField('サムネ', upload_to='images/')
    name = models.CharField('ダンジョン名', max_length=255)
    slug = models.SlugField('url名', unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ダンジョン'
        verbose_name_plural = 'ダンジョン'

    def __str__(self):
        return self.name

class Post(models.Model):
    dungeon = models.ForeignKey(Dungeon, on_delete=models.PROTECT, related_name='dungeon')
    tags = TaggableManager(blank=True)
    thumbnail = models.ImageField('サムネ', upload_to='images/')
    title = models.CharField('タイトル', max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False)
    content = MarkdownxField('本文')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_markdown_text_as_html(self):
        """MarkDown記法で書かれたtextをHTML形式に変換して返す"""
        return markdown(self.content, extensions=['fenced_code', 'attr_list', 'nl2br', 'tables', 'sane_lists'])

    class Meta:
        ordering = ['-created_at']
        verbose_name = '記事'
        verbose_name_plural = '投稿記事'

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False)
    content = MarkdownxField('本文')
    post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_at']
        verbose_name = 'コメント'
        verbose_name_plural = 'コメントリスト'

class CommentReply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False)
    content = MarkdownxField('本文')
    reply = models.ForeignKey(to=Comment, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_at']
        verbose_name = '返信'
        verbose_name_plural = '返信リスト'

class Favolate(models.Model):
    post = models.ForeignKey(to=Post, related_name='favolate', on_delete=models.CASCADE)
    is_favolate =
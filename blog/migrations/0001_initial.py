# Generated by Django 3.1 on 2020-10-06 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markdownx.models.MarkdownxField(verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'コメント',
                'verbose_name_plural': 'コメントリスト',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Dungeon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/', verbose_name='サムネ')),
                ('name', models.CharField(max_length=255, verbose_name='ダンジョン名')),
                ('slug', models.SlugField(unique=True, verbose_name='url名')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'ダンジョン',
                'verbose_name_plural': 'ダンジョン',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='images/', verbose_name='サムネ')),
                ('title', models.CharField(max_length=30, verbose_name='タイトル')),
                ('content', markdownx.models.MarkdownxField(verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('dungeon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dungeon', to='blog.dungeon')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': '記事',
                'verbose_name_plural': '投稿記事',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markdownx.models.MarkdownxField(verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='blog.comment')),
            ],
            options={
                'verbose_name': '返信',
                'verbose_name_plural': '返信リスト',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='blog.post'),
        ),
    ]

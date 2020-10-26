from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Dungeon, Post, Comment, CommentReply


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','comment_amounts', 'tag_list', 'thumbnail_preview', 'created_at')

    def thumbnail_preview(self, obj):
        return mark_safe('<img src="{}" style="width:100px; height:auto;">'.format(obj.thumbnail.url))

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def comment_amounts(self, obj):
        context = []
        for i in Comment.objects.filter(post=obj.id):
            context.append(i)
        return f"{len(context)}コメント"

class DungeonAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_preview')

    def img_preview(self, obj):
        return mark_safe('<img src="{}" style="width:100px; height:auto;">'.format(obj.img.url))

admin.site.register(Post, PostAdmin)
admin.site.register(Dungeon, DungeonAdmin)
admin.site.register(Comment)
admin.site.register(CommentReply)
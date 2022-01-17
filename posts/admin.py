from django.contrib import admin

from .models import Post, Comment, Reply, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    # readonly_fields = ['text', 'author', 'created', 'updated']


class LikeInline(admin.StackedInline):
    model = Like
    extra = 0
    
    
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['text', 'author', 'created', 'updated']
    inlines = [CommentInline, LikeInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
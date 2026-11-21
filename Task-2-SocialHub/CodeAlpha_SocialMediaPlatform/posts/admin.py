from django.contrib import admin
from .models import Comment, Like, Post

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at")
    search_fields = ("author__username", "content")
    inlines = [CommentInline]

admin.site.register(Like)
admin.site.register(Comment)

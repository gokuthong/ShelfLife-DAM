from django.contrib import admin
<<<<<<< HEAD
from .models import ActivityLog
=======
from .models import ActivityLog, Comment
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['user', 'action', 'asset', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'asset__title', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
=======
    list_display = ('user', 'asset', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'asset__title', 'ip_address')
    readonly_fields = ('log_id', 'timestamp')
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'content_preview', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'user')
    search_fields = ('user__username', 'asset__title', 'content')
    readonly_fields = ('comment_id', 'created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)

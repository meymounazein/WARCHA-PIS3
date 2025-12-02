from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Request, Review

# ------------------------------
# Inline Admin for Profile
# ------------------------------
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# ------------------------------
# Custom User Admin
# ------------------------------
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_select_related = ('profile',)

    def get_phone(self, instance):
        return instance.profile.phone if hasattr(instance, 'profile') else 'N/A'
    get_phone.short_description = 'Phone'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


# ------------------------------
# Request Admin
# ------------------------------
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at', 'is_urgent')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ------------------------------
# Review Admin
# ------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating_stars', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'stars')
    list_per_page = 20

    def rating_stars(self, obj):
        return obj.stars
    rating_stars.short_description = 'Rating'

    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Read-only Fields', {
            'fields': ('stars',),
            'classes': ('collapse',)
        }),
    )


# ------------------------------
# Register Models
# ------------------------------
# Unregister default User admin and register with custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Profile is registered inline with User, so no separate registration needed


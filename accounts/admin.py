from django.contrib import admin
from .models import (
    Profile,
    Request,
    Review,
    Category,
    Service,
    Professional,
)


# ==========================
# PROFILE ADMIN
# ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone")


# ==========================
# REQUEST ADMIN
# ==========================
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "user__username")


# ==========================
# REVIEW ADMIN
# ==========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rating", "created_at")
    list_filter = ("rating",)


# ==========================
# CATEGORY ADMIN
# ==========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


# ==========================
# SERVICE ADMIN
# ==========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)


# ==========================
# PROFESSIONAL ADMIN
# ==========================
@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "is_active")
    list_filter = ("is_active",)


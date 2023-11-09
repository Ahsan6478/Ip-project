from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "ip", "status", "req_count", "unblock_time"]
    # list_filter = ["pub_date"]
    # search_fields = ["question_text"]
    # fieldsets = [
    #     (None, {"fields": ["question_text"]}),
    #     ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    # ]
    # inlines = [ChoiceInline]

admin.site.register(User, UserAdmin)
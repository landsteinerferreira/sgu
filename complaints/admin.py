from django.contrib import admin
from complaints.models import Category, Complaints, Suggestion


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'priority', 'address', 'sector', 'photo', 'user', 'created_at', 'updated_at')
    search_fields = ('title',)


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created_at')
    search_fields = ('title',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Complaints, ComplaintsAdmin)
admin.site.register(Suggestion, SuggestionAdmin)

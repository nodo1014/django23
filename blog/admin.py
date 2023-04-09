from django.contrib import admin
from .models import Category, Tag, Post
from markdownx.admin import MarkdownxModelAdmin
# register(모델, 모델Admin)
# admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
#//TODO: register(모델, 모델Admin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, MarkdownxModelAdmin)


# list_display = ["id", "__str__", "publishing_date",
#                 "updating_date", "category", "highlighted"]
# list_filter = ["publishing_date"]
# search_fields = ["title", "short_description",
#                  "contents", "keyconcept", "category"]
# prepopulated_fields = {"slug": ("title", "keyconcept", "category",)}

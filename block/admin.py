from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.

class BlockAdmin(admin.ModelAdmin):
    list_display =['id','name','modified_at']
    list_editable = ['name']

class BlockItemAdmin(admin.ModelAdmin):
    list_display = ["pk","name_fk","d_date1","요일","stay","r_date2","d_fltno", "r_fltno","d_city1","d_city2"]
    list_editable = ["name_fk", ]
    
    
admin.site.register(Block, BlockAdmin)
admin.site.register(BlockItem, BlockItemAdmin)
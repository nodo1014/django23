from django.contrib import admin
from .models import *

# register(모델, 모델Admin)
# admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BasicCodeAdmin(admin.ModelAdmin):
    list_display = ["name","title"]

# class DetailCodeAdmin(admin.ModelAdmin):
#     list_display = ["basic_code","detail_code", "title"]
    # list_editable = ["detail_code", "title"]

class TourItemAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['item_code']}),
    #     ('필드셋', {'fields': ['']}),
        
    # ]
    list_display = ["pk","price","share_iti_chk","iti_name","share_air_chk","d_date1","요일","item_code","air_code","suffix_code","r_date1","d_time1", "d_time2",  "title", "d_city1", "d_city2","airline"]
    list_editable = ["share_iti_chk","share_air_chk","iti_name","title","suffix_code","d_city1","d_city2","air_code","price"]

class ItiNameAdmin(admin.ModelAdmin):
    list_display =['id','name','modified_at']
    list_editable = ['name']

class ItiAdmin(admin.ModelAdmin):
    list_display = ["pk","iti_name","touritem","day","city","trans","food"]
    list_editable = ["iti_name","touritem","day", "city", "trans","food"]

# class BlockAdmin(admin.ModelAdmin):
#     list_display =['id','name','modified_at']
#     list_editable = ['name']

# class BlockItemAdmin(admin.ModelAdmin):
#     list_display = ["pk","name_fk","d_date1","요일","stay","r_date2","d_fltno", "r_fltno","d_city1","d_city2"]
#     list_editable = ["name_fk", ]
    
    
# admin.site.register(Block, BlockAdmin)
# admin.site.register(BlockItem, BlockItemAdmin)
#   
# class ShareItiAdmin(admin.ModelAdmin):
#     list_display = ["pk","iti_name","day","city","trans","food"]
#     list_editable = ["iti_name","day", "city", "trans","food"]

# class ShareItiNameAdmin(admin.ModelAdmin):
#     list_display =['id','name','modified_at']
#     list_editable = ['name']

# class TourItemInline(admin.StackedInline):
# class TourItemInline(admin.TabularInline):
#     model = TourItem
#     extra = 3
    # list_display = ["id", "basic_code", "d_city1","d_city2","d_date1","d_daychange","d_time1","d_time2", "content", "etc", "airline", "price", "created_at"]

# class TourItemAdmin(admin.ModelAdmin):
#     list_display = ["id", "basic_code", "content", "etc", "airline", "price","created_at"]
#     list_filter = ['price']
#     search_fields = ['etc', 'airline', 'content']

# class BasicCodeAdmin(admin.ModelAdmin):
    # list_display = ["id", "category","basic_code", "title","created_at"]
    # fieldsets = [
    #     ('1단계',{'fields' : ['title','category','basic_code']}),
    #     ('상품 설명', {'fields' : ['hook_text', 'content'],'classes' : ['collapse']}),
    # ]
    # inlines = [TourItemInline] #TourItemInline 모델 같이 보기
    # list_filter = ['basic_code','title', 'category']
    # list_filter = ('title',
    #                ('created_at', DateRangeFilter),
    #                ('created_at', DateRangeFilter),
    #                )
    # search_fields = ['title']

# admin.site.register(DetailCode, DetailCodeAdmin)
admin.site.register(TourItem, TourItemAdmin)
admin.site.register(BasicCode, BasicCodeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Iti, ItiAdmin)
admin.site.register(ItiName, ItiNameAdmin)

# admin.site.register(ShareIti, ShareItiAdmin)
# admin.site.register(ShareItiName, ShareItiNameAdmin)

# list_display = ["id", "__str__", "publishing_date",
#                 "updating_date", "category", "highlighted"]
# list_filter = ["publishing_date"]
# search_fields = ["title", "short_description",
#                  "contents", "keyconcept", "category"]
# prepopulated_fields = {"slug": ("title", "keyconcept", "category",)}

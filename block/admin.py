from django.contrib import admin
from .models import *


# register(모델, 모델Admin)
# admin.site.register(Post)

    
    

class BlockItemAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['item_code']}),
    #     ('필드셋', {'fields': ['']}),
        
    # ]
    list_display = ['pk']
    # list_editable = ["price"]
    
class BlockAdmin(admin.ModelAdmin):
    list_display = ['pk','name', 'content']

admin.site.register(BlockItem, BlockItemAdmin)
admin.site.register(Block, BlockAdmin)



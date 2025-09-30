from django.contrib import admin
from banners import models
from django.utils.html import format_html  

# Register your models here.
class FrontPageConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_location",
        "image_channel",
        "order",
        "provider",
        "is_active"
    )
    list_filter = (
        "image_location",
        "image_channel",
        "provider"
    ) 
    search_fields =(
        "id", 
        "cta_text", 
        "cta_link"
    )
    
       

    def image_preview(self, obj):
        """Show a small preview of the original photo"""
        if obj.photo:
            return format_html('<img src="{}" width="80" style="object-fit: cover;"/>', obj.photo.url)
        return "-"
    image_preview.short_description = "Photo Preview"
admin.site.register(models.LangLocale)
admin.site.register(models.Configuration)
admin.site.register(models.FrontPageImageConfiguration,FrontPageConfigurationAdmin)
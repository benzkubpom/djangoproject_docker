from django.contrib import admin
from django.utils.html import format_html

from .models import Brand, Category, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'name', 'brand', 'category', 'price')
    list_filter = ('brand', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('preview',)
    fields = (
        'name', 'brand', 'category', 'description', 'price',
        'image', 'image_url', 'preview',
    )

    @admin.display(description='รูป')
    def thumbnail(self, obj):
        """รูปย่อในตาราง เพื่อเห็นได้ทันทีว่าสินค้าไหนยังไม่มีรูป"""
        return self._img(obj, 48) or format_html(
            '<span style="color:#999">—</span>'
        )

    @admin.display(description='ตัวอย่างรูป')
    def preview(self, obj):
        return self._img(obj, 240) or 'ยังไม่มีรูป — หน้าเว็บจะใช้ภาพลายเส้นตามหมวดหมู่แทน'

    @staticmethod
    def _img(obj, size):
        url = obj.photo_url if obj.pk else ''
        if not url:
            return ''
        return format_html(
            '<img src="{}" style="max-width:{}px;max-height:{}px;'
            'object-fit:contain;border:1px solid #e5e5e5">',
            url, size, size,
        )

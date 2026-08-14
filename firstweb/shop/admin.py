from django.contrib import admin
from django.templatetags.static import static
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
    # thumbnail อ่าน category เพื่อเลือกภาพประกอบ ดึงมาพร้อมกันกันคิวรีต่อแถว
    list_select_related = ('brand', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('preview',)
    fields = (
        'name', 'brand', 'category', 'description', 'price',
        'image', 'image_url', 'preview',
    )

    @admin.display(description='รูป')
    def thumbnail(self, obj):
        """รูปย่อในตาราง เห็นได้ทันทีว่าแถวไหนใช้รูปถ่ายจริง แถวไหนใช้ภาพประกอบ"""
        return self._img(obj, 48)

    @admin.display(description='ตัวอย่างรูป')
    def preview(self, obj):
        if not obj.pk:
            return 'บันทึกสินค้าก่อน แล้วตัวอย่างรูปจะแสดงที่นี่'
        note = (
            'รูปถ่ายที่ตั้งไว้กับสินค้ารายการนี้'
            if obj.photo_url else
            f'ยังไม่มีรูปถ่าย — หน้าเว็บใช้ภาพประกอบ {obj.photo_static} ให้ก่อน'
        )
        return format_html('{}<p style="margin-top:8px;color:#666">{}</p>',
                           self._img(obj, 240), note)

    @staticmethod
    def _img(obj, size):
        """รูปถ่ายของสินค้าถ้ามี ถ้าไม่มีก็ภาพประกอบตามหมวดหมู่ (เหมือนที่หน้าเว็บใช้)"""
        if not obj.pk:
            return ''
        url = obj.photo_url or static(obj.photo_static)
        return format_html(
            '<img src="{}" style="max-width:{}px;max-height:{}px;'
            'object-fit:contain;border:1px solid #e5e5e5">',
            url, size, size,
        )

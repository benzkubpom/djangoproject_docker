import re

from django.db import models
from django.urls import reverse

# ชื่อสินค้าในฐานข้อมูลเก็บรหัสรุ่นไว้ท้ายชื่อ เช่น 'Power Supply S3809-045'
CODE_PATTERN = re.compile(r'\s([A-Z0-9]{1,6}-\d{3})$')

# หมวดหมู่ -> คีย์ภาพลายเส้นใน shop/_product_media.html
# ใช้เป็นภาพสำรองเมื่อสินค้ายังไม่มีรูปถ่ายในระบบ
CATEGORY_ICONS = {
    'พาวเวอร์ซัพพลาย': 'psu',
    'โน้ตบุ๊ก': 'laptop',
    'เคสคอมพิวเตอร์': 'case',
    'เมนบอร์ด': 'mainboard',
    'คีย์บอร์ด': 'keyboard',
    'การ์ดจอ': 'gpu',
    'เครื่องสำรองไฟ': 'ups',
    'เว็บแคม': 'webcam',
    'อุปกรณ์จัดเก็บข้อมูล': 'storage',
    'คอมพิวเตอร์ตั้งโต๊ะ': 'desktop',
    'เมาส์': 'mouse',
    'ซีพียู': 'cpu',
    'หน่วยความจำ': 'ram',
    'อุปกรณ์เครือข่าย': 'network',
    'ชุดหูฟัง': 'headset',
    'จอภาพ': 'monitor',
}


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    # รูปสินค้า: อัปโหลดไฟล์เข้า MEDIA_ROOT/products/ หรือชี้ไปยังรูปภายนอกด้วยลิงก์
    # ทั้งสองช่องเว้นว่างได้ หน้าเว็บจะเปลี่ยนไปใช้ภาพลายเส้นตามหมวดหมู่ให้เอง
    image = models.ImageField(
        upload_to='products/', blank=True, verbose_name='รูปสินค้า'
    )
    image_url = models.URLField(
        blank=True,
        verbose_name='ลิงก์รูปสินค้า',
        help_text='ใช้เมื่อไม่ได้อัปโหลดไฟล์ ถ้าอัปโหลดไฟล์ไว้ระบบจะใช้ไฟล์ก่อน',
    )

    def __str__(self):
        return f'{self.name} - {self.price:,.0f} บาท'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk])

    # --- ตัวช่วยสำหรับหน้าเว็บ (property ไม่ต้อง makemigrations) ---

    @property
    def code(self):
        """รหัสรุ่นท้ายชื่อสินค้า เช่น 'S3809-045' (คืนค่าว่างถ้าไม่มี)"""
        match = CODE_PATTERN.search(self.name)
        return match.group(1) if match else ''

    @property
    def title(self):
        """ชื่อสินค้าที่ตัดรหัสรุ่นออกแล้ว เช่น 'Power Supply'"""
        return CODE_PATTERN.sub('', self.name).strip() or self.name

    @property
    def spec_list(self):
        """แยก description ที่คั่นด้วยจุลภาคออกเป็นรายการสเปก"""
        return [part.strip() for part in self.description.split(',') if part.strip()]

    @property
    def photo_url(self):
        """ที่อยู่รูปสินค้า: ไฟล์ที่อัปโหลดมาก่อน ถ้าไม่มีจึงใช้ลิงก์ภายนอก"""
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def icon(self):
        """คีย์ภาพลายเส้นตามหมวดหมู่ ใช้เป็นภาพสำรองเมื่อยังไม่มีรูปถ่าย"""
        return CATEGORY_ICONS.get(self.category.name, 'generic')

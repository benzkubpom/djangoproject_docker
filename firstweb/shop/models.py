import re

from django.db import models
from django.urls import reverse

# ชื่อสินค้าในฐานข้อมูลเก็บรหัสรุ่นไว้ท้ายชื่อ เช่น 'Power Supply S3809-045'
CODE_PATTERN = re.compile(r'\s([A-Z0-9]{1,6}-\d{3})$')


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

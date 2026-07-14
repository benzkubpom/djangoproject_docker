from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=50)
    email = models.EmailField()
    point = models.IntegerField(default=1)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        # return self.name + ' คะแนน: ' + str(self.point) +  ' point'
        return 'ชื่อ: {} คะแนน: {}'.format(self.name,self.point)


class Fruit(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อผลไม้")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียด")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา")
    stock = models.IntegerField(default=0, verbose_name="จำนวนคงเหลือ")
    image = models.ImageField(upload_to='fruits/', blank=True, null=True, verbose_name="รูปภาพ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่อัปเดต")

    def __str__(self):
        return self.name
    

class VehicleLog(models.Model):
    license_plate = models.CharField(max_length=20, verbose_name="ทะเบียนรถ")
    vehicle_type = models.CharField(
        max_length=50,
        choices=[
            ("car", "รถยนต์"),
            ("motorcycle", "มอเตอร์ไซค์"),
            ("truck", "รถบรรทุก"),
        ],
        verbose_name="ประเภทรถ"
    )
    entry_time = models.DateTimeField(verbose_name="เวลาเข้า")
    exit_time = models.DateTimeField(null=True, blank=True, verbose_name="เวลาออก")
    driver_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="ชื่อผู้ขับ")
    note = models.TextField(blank=True, verbose_name="หมายเหตุ")

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"
# 🔬 ผ่าโค้ดทีละบรรทัด — Models และ Query ของ app `shop`

> เอกสารคู่มือฉบับ "อธิบายทุกบรรทัด ทุกคำ" สำหรับผู้เริ่มต้น
> ใช้คู่กับ [Django-Shell-Query-Tutorial.md](Django-Shell-Query-Tutorial.md)

---

## สารบัญ

1. [ผ่าไฟล์ models.py ทีละบรรทัด](#ส่วนที่-1)
2. [รู้จักกับ Django ORM และ Django Shell (ส่วนเสริม)](#ส่วนเสริม-orm-shell)
3. [ผ่าคำสั่ง import ใน shell](#ส่วนที่-2)
4. [ผ่าคำสั่ง `Product.objects.all()`](#ส่วนที่-3)
5. [ผ่าผลลัพธ์ `<QuerySet [...]>` — อ่านยังไง](#ส่วนที่-4)
6. [ผ่า for loop ใน shell](#ส่วนที่-5)
7. [ผ่าคำสั่ง `.get()` และการเข้าถึงข้อมูลผ่านจุด (.)](#ส่วนที่-6)
8. [ผ่าคำสั่ง `.filter()` และ underscore สองตัว (`__`)](#ส่วนที่-7)
9. [ผ่าคำสั่ง `.order_by()` และ slicing `[:5]`](#ส่วนที่-8)
10. [ผ่าคำสั่ง `.aggregate()` และ `.annotate()`](#ส่วนที่-9)
11. [ผ่าคำสั่งสร้าง/แก้/ลบข้อมูล](#ส่วนที่-10)

---

<a name="ส่วนที่-1"></a>
# ส่วนที่ 1 — ผ่าไฟล์ `models.py` ทีละบรรทัด

ไฟล์เต็มอยู่ที่ `firstweb/shop/models.py` — เราจะไล่อธิบายจากบนลงล่างทีละบรรทัด

## 1.1 บรรทัด import

```python
from django.db import models
```

| ส่วน | อธิบาย |
|------|--------|
| `from django.db` | ไปที่แพ็คเกจ `django.db` — ส่วนของ Django ที่จัดการเรื่อง**ฐานข้อมูล** (db = database) |
| `import models` | ดึงโมดูล `models` เข้ามาใช้ — ข้างในมีเครื่องมือสร้างตาราง เช่น `CharField`, `ForeignKey`, `Model` |
| ทำไมต้องมี | ถ้าไม่ import บรรทัดถัด ๆ ไปจะเรียก `models.Model` หรือ `models.CharField` ไม่ได้เลย (Python จะฟ้อง `NameError`) |

---

## 1.2 โมเดล `Brand` — ตารางแบรนด์

```python
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
```

### บรรทัดที่ 1: `class Brand(models.Model):`

| ส่วน | อธิบาย |
|------|--------|
| `class` | คีย์เวิร์ดของ Python สำหรับ**ประกาศคลาส** (พิมพ์เขียวของ object) |
| `Brand` | ชื่อคลาสที่เราตั้งเอง — ตามธรรมเนียมใช้ตัวใหญ่ขึ้นต้น และเป็น**เอกพจน์** (Brand ไม่ใช่ Brands) |
| `(models.Model)` | วงเล็บคือการ**สืบทอด (inherit)** — Brand รับความสามารถทั้งหมดมาจากคลาสแม่ชื่อ `Model` ของ Django |
| `:` | โคลอนบอกว่า "เนื้อหาของคลาสเริ่มบรรทัดถัดไป" (ทุกอย่างที่ย่อหน้าเข้าไปคือของคลาสนี้) |

> 📌 **หัวใจสำคัญ:** แค่สืบทอดจาก `models.Model` — Django จะรู้ทันทีว่า
> "คลาสนี้คือ**ตารางในฐานข้อมูล**" และแถมความสามารถให้ฟรี ๆ เพียบ:
> - สร้างตาราง SQL ให้อัตโนมัติ (ผ่าน `makemigrations` + `migrate`) → ได้ตารางชื่อ `shop_brand`
> - สร้างคอลัมน์ `id` (Primary Key) ให้อัตโนมัติ ไม่ต้องเขียนเอง
> - แถมตัวจัดการ `Brand.objects` ไว้ query ข้อมูล
> - แถมเมธอด `.save()`, `.delete()` ให้ทุก object

### บรรทัดที่ 2: `name = models.CharField(max_length=100, unique=True)`

| ส่วน | อธิบาย |
|------|--------|
| `name` | ชื่อฟิลด์ (= ชื่อ**คอลัมน์**ในตาราง) เราตั้งเอง — ในที่นี้เก็บชื่อแบรนด์ เช่น "Astra" |
| `=` | ผูกฟิลด์นี้เข้ากับคลาส |
| `models.CharField(...)` | ประเภทข้อมูลคือ**ข้อความสั้น** (Char = Character) เทียบกับ SQL คือ `VARCHAR` |
| `max_length=100` | ยาวได้**ไม่เกิน 100 ตัวอักษร** — CharField **บังคับ**ต้องระบุค่านี้เสมอ ลืมใส่ = error ตอน migrate |
| `unique=True` | **ห้ามซ้ำ** — มี "Astra" ได้แค่แถวเดียวในตาราง ถ้าพยายามสร้างซ้ำ ฐานข้อมูลจะปฏิเสธ (`IntegrityError`) |

เทียบเป็น SQL ที่ Django สร้างให้:

```sql
CREATE TABLE shop_brand (
    id    integer PRIMARY KEY AUTOINCREMENT,   -- Django แถมให้อัตโนมัติ
    name  varchar(100) NOT NULL UNIQUE          -- จากบรรทัดที่เราเขียน
);
```

### บรรทัดที่ 3–4: เมธอด `__str__`

```python
    def __str__(self):
        return self.name
```

| ส่วน | อธิบาย |
|------|--------|
| `def` | คีย์เวิร์ดประกาศฟังก์ชัน (พออยู่ในคลาสเรียกว่า "เมธอด") |
| `__str__` | ชื่อพิเศษของ Python (อ่านว่า "ดันเดอร์-เอสทีอาร์") — Python จะเรียกเมธอดนี้**อัตโนมัติ**ทุกครั้งที่ต้องแปลง object เป็นข้อความ เช่นตอน `print()` |
| `(self)` | `self` = ตัว object เอง (แถวข้อมูลแถวนั้น ๆ) — เมธอดในคลาสต้องรับ `self` เป็นตัวแรกเสมอ |
| `return self.name` | ตอบกลับด้วยค่าในฟิลด์ `name` ของแถวนั้น |

**เห็นผลต่างชัด ๆ:**

```python
# ❌ ถ้าไม่มี __str__            # ✅ มี __str__
>>> Brand.objects.first()        >>> Brand.objects.first()
<Brand: Brand object (1)>        <Brand: Astra>
```

ไม่มี `__str__` ก็ไม่ error แต่อ่านไม่รู้เรื่องว่าแถวไหนคือแบรนด์อะไร — จึงควรเขียนติดไว้ทุกโมเดล

---

## 1.3 โมเดล `Category` — ตารางหมวดหมู่

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
```

โครงสร้างเหมือน `Brand` ทุกอย่าง มีเพิ่มมาส่วนเดียวคือ:

### `class Meta:` คืออะไร

| ส่วน | อธิบาย |
|------|--------|
| `class Meta:` | คลาสซ้อนในคลาส — เป็นที่เก็บ**การตั้งค่าเสริม**ของโมเดล (ไม่ใช่คอลัมน์ข้อมูล) |
| `verbose_name_plural = 'Categories'` | บอก Django ว่ารูปพหูพจน์ของโมเดลนี้สะกดว่า "Categories" |
| ทำไมต้องบอก | ปกติ Django เติม s ท้ายชื่อให้อัตโนมัติ → จะได้ "Category**s**" (สะกดผิด!) โผล่ในหน้า admin เราเลย override บอกคำที่ถูก |

---

## 1.4 โมเดล `Product` — ตารางสินค้า (พระเอกของเรา)

```python
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.price:,.0f} บาท'
```

### บรรทัด: `name = models.CharField(max_length=200, unique=True)`

เหมือนของ Brand แต่ให้ยาวได้ 200 ตัวอักษร เพราะชื่อสินค้ายาวกว่าชื่อแบรนด์ และ `unique=True` เพราะชื่อรุ่นสินค้าไม่ควรซ้ำกัน (คำสั่ง `load_products` ก็อาศัยความ unique นี้กันข้อมูลซ้ำตอนรันซ้ำ)

### บรรทัด: `brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')`

**บรรทัดสำคัญที่สุดในไฟล์** — ขอผ่าละเอียดทีละ argument:

| ส่วน | อธิบาย |
|------|--------|
| `brand` | ชื่อฟิลด์ — ในฐานข้อมูลจริง Django จะสร้างคอลัมน์ชื่อ `brand_id` (เติม `_id` ให้เอง) เก็บ**หมายเลข id** ของแถวในตาราง Brand |
| `models.ForeignKey(...)` | ประเภทฟิลด์แบบ**เชื่อมโยงตาราง** — สร้างความสัมพันธ์ "หลายต่อหนึ่ง": สินค้า**หลาย**ตัวชี้ไปที่แบรนด์**หนึ่ง**แบรนด์ได้ |
| `Brand` (arg ตัวแรก) | ชี้ไปที่ตารางไหน — ในที่นี้คือคลาส `Brand` ที่ประกาศไว้ข้างบน (ต้องประกาศ Brand ก่อน Product ในไฟล์ ไม่งั้น Python ยังไม่รู้จักชื่อนี้) |
| `on_delete=models.CASCADE` | **ถ้าแบรนด์ถูกลบ ให้ทำยังไงกับสินค้าที่ชี้มาหามัน?** — `CASCADE` = "ลบตาม" เช่น ลบแบรนด์ Astra → สินค้า Astra ทั้ง 18 ตัวหายตามทันที (Django **บังคับ**ต้องระบุ argument นี้ ลืมใส่ = error) |
| `related_name='products'` | ตั้งชื่อ "ทางเดินย้อนกลับ" จากฝั่ง Brand → มาหาสินค้า ทำให้เขียน `brand.products.all()` ได้ ถ้าไม่ตั้ง Django จะใช้ชื่ออัตโนมัติว่า `brand.product_set.all()` (อ่านยากกว่า) |

**ตัวเลือกอื่นของ `on_delete` ที่ควรรู้จัก:**

| ค่า | ความหมาย |
|-----|----------|
| `models.CASCADE` | ลบแม่ → ลูกถูกลบตาม (ที่เราใช้) |
| `models.PROTECT` | ห้ามลบแม่ ถ้ายังมีลูกชี้อยู่ (จะ error) |
| `models.SET_NULL` | ลบแม่ → ช่องของลูกกลายเป็น NULL (ต้องใส่ `null=True` ด้วย) |
| `models.SET_DEFAULT` | ลบแม่ → ลูกเปลี่ยนไปใช้ค่า default |

### บรรทัด: `category = models.ForeignKey(Category, ...)`

เหมือนกับ `brand` ทุกประการ แค่ชี้ไปตาราง `Category` แทน

> 💡 **สงสัยไหม:** ทั้ง brand และ category ใช้ `related_name='products'` เหมือนกัน ทำไมไม่ชนกัน?
> เพราะมันอยู่**คนละคลาสปลายทาง** — ตัวหนึ่งเป็นทางย้อนของ Brand อีกตัวเป็นของ Category
> จะชนก็ต่อเมื่อ FK สองตัว**ในโมเดลเดียวกันชี้ไปตารางเดียวกัน** — แบบนั้นต้องตั้งชื่อต่างกัน

### บรรทัด: `description = models.TextField(blank=True)`

| ส่วน | อธิบาย |
|------|--------|
| `models.TextField()` | ข้อความ**ยาวไม่จำกัด** (ต่างจาก CharField ที่ต้องกำหนด max_length) เหมาะกับรายละเอียดสินค้า |
| `blank=True` | อนุญาตให้**เว้นว่าง**ได้ตอนกรอกฟอร์ม/แอดมิน — สินค้าไม่มีคำอธิบายก็บันทึกผ่าน |

> ⚠️ **`blank` กับ `null` ไม่เหมือนกัน!** จุดที่มือใหม่งงบ่อยที่สุด:
> - `blank=True` → กติกาฝั่ง**ฟอร์ม**: กรอกเว้นว่างได้ (validation)
> - `null=True` → กติกาฝั่ง**ฐานข้อมูล**: คอลัมน์เก็บค่า NULL ได้
> - สำหรับฟิลด์ข้อความ แนะนำใช้แค่ `blank=True` — ค่าว่างจะถูกเก็บเป็น string ว่าง `''` ไม่ใช่ NULL (จะได้ไม่ต้องเช็คสองแบบ)

### บรรทัด: `price = models.DecimalField(max_digits=10, decimal_places=2)`

| ส่วน | อธิบาย |
|------|--------|
| `models.DecimalField()` | ตัวเลข**ทศนิยมแบบเป๊ะ** เหมาะกับ**เงิน** |
| `max_digits=10` | จำนวนหลัก**รวมทั้งหมด**ไม่เกิน 10 หลัก (นับทั้งหน้าและหลังจุด) |
| `decimal_places=2` | เป็นทศนิยม 2 ตำแหน่ง → ราคาสูงสุดที่เก็บได้คือ 99,999,999.99 |

> 💡 **ทำไมไม่ใช้ `FloatField`?** เพราะ float เก็บเลขแบบประมาณ (`0.1 + 0.2 = 0.30000000000000004`)
> เอามาคิดเงินแล้วเพี้ยนได้ — งานเงินทองต้องใช้ `DecimalField` เสมอ ค่าที่ได้กลับมาใน Python จะเป็นชนิด `Decimal` เช่น `Decimal('6500.00')`

### บรรทัด: `created_at = models.DateTimeField(auto_now_add=True)`

| ส่วน | อธิบาย |
|------|--------|
| `models.DateTimeField()` | เก็บวันที่ + เวลา |
| `auto_now_add=True` | ให้ Django **ประทับเวลาให้อัตโนมัติครั้งเดียว**ตอนสร้างแถว (create) แล้วไม่เปลี่ยนอีก — เราไม่ต้อง (และไม่ควร) กรอกเอง |

| ตัวเลือก | ประทับเวลาเมื่อไหร่ | ใช้ทำอะไร |
|----------|--------------------|----------|
| `auto_now_add=True` | เฉพาะตอน**สร้าง** | วันที่เพิ่มสินค้า (ที่เราใช้) |
| `auto_now=True` | ทุกครั้งที่ **save** | วันที่แก้ไขล่าสุด |

### บรรทัด: `return f'{self.name} - {self.price:,.0f} บาท'`

| ส่วน | อธิบาย |
|------|--------|
| `f'...'` | **f-string** — string ที่ฝังตัวแปรได้ด้วย `{ }` |
| `{self.name}` | แทนที่ด้วยชื่อสินค้าของแถวนั้น |
| `{self.price:,.0f}` | แทนที่ด้วยราคา โดยหลัง `:` คือ**รูปแบบการแสดงผล** — `,` = ใส่ลูกน้ำคั่นหลักพัน, `.0f` = ทศนิยม 0 ตำแหน่ง → `50300.00` กลายเป็น `50,300` |
| ผลลัพธ์ | `Laptop C6684-081 - 50,300 บาท` |

---

<a name="ส่วนเสริม-orm-shell"></a>
# ส่วนเสริม — รู้จักกับ Django ORM และ python manage.py shell

ก่อนที่เราจะไปลองรันคำสั่งต่าง ๆ ใน shell เรามาทำความเข้าใจแนวคิดพื้นฐานและเครื่องมือที่เราจะใช้กันก่อนครับ

## 1. การ Query ข้อมูลด้วย Django ORM
**ORM (Object-Relational Mapping)** คือระบบของ Django ที่ทำหน้าที่เป็น "สะพานเชื่อม" ระหว่าง**คลาสในภาษา Python** กับ**ตารางในฐานข้อมูล (SQL Database)**

*   **แนวคิดดั้งเดิม:** หากเราต้องการดึงข้อมูลสินค้าทั้งหมดจากฐานข้อมูล เราจะต้องเขียนภาษา SQL แบบนี้:
    ```sql
    SELECT * FROM shop_product;
    ```
*   **แนวคิดแบบ Django ORM:** เราไม่ต้องเขียน SQL เอง แต่จะใช้ภาษา Python สั่งงานผ่านคลาส **Model** ของเราแทน เช่น:
    ```python
    Product.objects.all()
    ```
    Django ORM จะนำคำสั่ง Python นี้ไปแปลเป็นคำสั่ง SQL ที่ถูกต้องให้เราโดยอัตโนมัติ แล้วแปลงผลลัพธ์กลับมาเป็น Object ของ Python ให้เราใช้งานต่อได้ทันที

> 💡 **ข้อดีของ Django ORM:**
> 1. **เขียนง่ายและปลอดภัย:** ป้องกันการโจมตีประเภท SQL Injection ได้โดยอัตโนมัติ
> 2. **เป็นอิสระจากประเภทฐานข้อมูล:** ไม่ว่าจะใช้ SQLite, MySQL, หรือ PostgreSQL เราก็เขียนโค้ด Python เหมือนเดิมทุกประการ Django จะจัดการแปลงเป็นภาษา SQL ของแต่ละระบบให้เอง
> 3. **ทำงานในรูปแบบ Object:** ดึงข้อมูลมาแล้วสามารถเขียน `product.price` หรือ `product.name` เข้าถึงข้อมูลได้สะดวกรวดเร็ว

### ตารางเทียบ: โลก Python (ORM) ↔ โลกฐานข้อมูล (SQL)

หัวใจของ ORM คือการ "จับคู่" (Mapping) ของ 2 โลกนี้เข้าด้วยกัน — จำตารางนี้ได้ตารางเดียว จะอ่านโค้ด Django ออกทั้งหมด:

| โลก Python (ORM) | โลกฐานข้อมูล (SQL) | ตัวอย่างในโปรเจคเรา |
|------------------|--------------------|--------------------|
| คลาสโมเดล 1 คลาส | ตาราง 1 ตาราง | คลาส `Product` → ตาราง `shop_product` |
| object 1 ตัว | แถวข้อมูล 1 แถว | `p = Product.objects.first()` = แถวแรก |
| attribute ของ object | คอลัมน์ในแถวนั้น | `p.price` = ค่าในคอลัมน์ `price` |
| `objects.all()` | `SELECT * FROM ...` | ดึงทุกแถว |
| `objects.filter(...)` | `SELECT ... WHERE ...` | ดึงเฉพาะแถวที่ตรงเงื่อนไข |
| `objects.create(...)` / `.save()` | `INSERT INTO ...` | เพิ่มแถวใหม่ |
| แก้ attribute แล้ว `.save()` / `.update()` | `UPDATE ... SET ...` | แก้ไขแถว |
| `.delete()` | `DELETE FROM ...` | ลบแถว |
| `.order_by()` | `ORDER BY` | เรียงลำดับ |
| `.count()` | `SELECT COUNT(*)` | นับจำนวนแถว |

> 📌 อยากพิสูจน์ว่า ORM แปลเป็น SQL จริง ๆ? ใน shell ลองพิมพ์
> `print(Product.objects.filter(price__gt=60000).query)` — จะเห็นคำสั่ง SQL ที่ Django สร้างให้ทันที

---

## 2. python manage.py shell คืออะไร?
เมื่อเราสร้าง Model และติดตั้งฐานข้อมูลเสร็จแล้ว เรามักจะต้องการทดลองเขียนคำสั่งดึงข้อมูล เพิ่มข้อมูล หรือแก้ไขข้อมูล เพื่อดูว่าโค้ดทำงานถูกต้องตามต้องการหรือไม่ เครื่องมือที่ดีที่สุดสำหรับขั้นตอนนี้คือ **Django Shell**

*   **Django Shell (`python manage.py shell`)** คือหน้าต่างคำสั่งแบบโต้ตอบ (Interactive Console) ของ Python แต่**มีความพิเศษคือจะทำการโหลดโปรเจกต์ Django ของเราเข้ามาไว้ด้วยอัตโนมัติ**
*   **ต่างจาก Python Shell ปกติอย่างไร?**
    *   **Python Shell ปกติ** (เปิดด้วยคำสั่ง `python` หรือ `python3`): จะเป็นแค่ Python เปล่า ๆ ที่ไม่รู้จักโมเดล, ไม่รู้จักไฟล์ `settings.py` และไม่รู้จักโฟลเดอร์ของโปรเจกต์ Django ของเราเลย หากลอง import โมเดลจะขึ้นข้อความผิดพลาด `ModuleNotFoundError`
    *   **Django Shell** (เปิดด้วยคำสั่ง `python manage.py shell`): จะทำการเตรียมสภาพแวดล้อมที่จำเป็นของ Django (Environment settings) ไว้ให้พร้อม ทำให้เราสามารถเรียกใช้งาน Model, ทำการ Query ข้อมูล, หรือสั่งลบ/เพิ่มข้อมูลในฐานข้อมูลจริง ๆ ของเราได้ทันที

---

## 3. การใช้งาน python manage.py shell

### 3.1 วิธีเปิดใช้งาน
ให้ใช้ Terminal เปิดเข้าไปในโฟลเดอร์หลักของโปรเจกต์ (โฟลเดอร์ที่มีไฟล์ `manage.py` อยู่) จากนั้นพิมพ์คำสั่ง:
```bash
python manage.py shell
```
เมื่อคำสั่งรันสำเร็จ หน้าจอ Terminal จะเปลี่ยนเป็นเครื่องหมาย `>>>` ซึ่งแสดงว่าพร้อมให้เราพิมพ์คำสั่ง Python ได้แล้ว

### 3.2 ตัวอย่างการรันคำสั่งเบื้องต้น
เมื่ออยู่ใน Shell ให้ลองนำเข้า Model และลองสั่งดึงข้อมูลดู:
```python
# 1. นำเข้าโมเดล Product เข้ามาใน shell
from shop.models import Product

# 2. ลองดึงข้อมูลทั้งหมด
Product.objects.all()
```

### 3.3 วิธีออกจาก Shell
เมื่อใช้งานเสร็จสิ้นและต้องการกลับไปที่ Terminal ปกติ สามารถทำได้ด้วยวิธีใดวิธีหนึ่งดังนี้:
*   พิมพ์คำสั่ง `exit()` แล้วกด **Enter**
*   กดปุ่มคีย์ลัด **`Ctrl + D`** (สำหรับผู้ใช้ macOS / Linux)
*   กดปุ่มคีย์ลัด **`Ctrl + Z`** แล้วกด **Enter** (สำหรับผู้ใช้ Windows)

### 3.4 ผ่าตัวอย่างการใช้งานจริงทีละบรรทัด (ตัวอย่างคลาสสิกจาก app `polls`)

ตัวอย่างต่อไปนี้เป็น session จริงใน shell ของโปรเจคที่มีโมเดล `Question` (แบบสอบถาม มีฟิลด์ `text` กับ `pub_date`) — เป็นตัวอย่างจากบทเรียน polls ของ Django ที่เจอบ่อยที่สุด เราจะไล่อธิบายทุกบรรทัดว่าเกิดอะไรขึ้น:

```python
>>> from polls.models import Question
>>> from django.utils import timezone
>>> q = Question(text="What is python inheritance?", pub_date=timezone.now())
>>> q.save()
>>> q.text="This is updated"
>>> q.save()
>>> q.delete()
(1, {'polls.Question': 1})
>>> data = Question.objects.all()
>>> data
<QuerySet [<Question: Question object (1)>]>
>>> filter_q=Question.objects.filter(pub_date__year=2024)
>>> filter_q
<QuerySet []>
```

| บรรทัด | เกิดอะไรขึ้น | ยิง SQL ไหม? |
|--------|-------------|:---:|
| `from polls.models import Question` | ดึงโมเดล `Question` จาก app ชื่อ `polls` เข้ามาใน shell (เหมือนที่เรา import `Product` จาก `shop`) | ❌ |
| `from django.utils import timezone` | ดึงเครื่องมือจัดการเวลาของ Django — `timezone.now()` ให้วันเวลาปัจจุบัน**พร้อมข้อมูล timezone** ซึ่ง Django แนะนำให้ใช้แทน `datetime.now()` ของ Python เปล่า ๆ (กันปัญหาเวลาเพี้ยนข้ามประเทศ) | ❌ |
| `q = Question(text=..., pub_date=timezone.now())` | สร้าง object ขึ้นมา**ในหน่วยความจำเท่านั้น** — ส่งค่าเข้าฟิลด์ผ่านวงเล็บทีละตัว ⚠️ ตอนนี้ฐานข้อมูล**ยังไม่มีแถวนี้** และ `q.id` ยังเป็น `None` | ❌ |
| `q.save()` (ครั้งแรก) | บันทึกลงฐานข้อมูลจริง → SQL `INSERT` ทำงาน หลังบรรทัดนี้ `q.id` ถึงจะมีค่า (เลขรันอัตโนมัติ) | ✅ INSERT |
| `q.text = "This is updated"` | แก้ค่าในหน่วยความจำ — ฐานข้อมูล**ยังเป็นค่าเดิม** | ❌ |
| `q.save()` (ครั้งที่สอง) | คราวนี้ Django เห็นว่า `q.id` มีค่าแล้ว → เปลี่ยนจาก INSERT เป็น `UPDATE` แถวเดิมแทน (นี่คือเหตุผลที่ `.save()` ใช้ได้ทั้ง "สร้าง" และ "แก้") | ✅ UPDATE |
| `q.delete()` | ลบแถวนี้ออกจากฐานข้อมูล → ตอบกลับ `(1, {'polls.Question': 1})` = ลบสำเร็จ 1 แถว แจกแจงว่าเป็นโมเดล `polls.Question` 1 แถว | ✅ DELETE |
| `data = Question.objects.all()` | ขอทุกแถว เก็บใส่ตัวแปร `data` — ยังไม่ยิง SQL เพราะ Lazy Evaluation | ❌ |
| `data` | พิมพ์ชื่อตัวแปรเฉย ๆ = สั่งให้ shell แสดงผล → ตอนนี้แหละที่ SQL `SELECT` ทำงานจริง | ✅ SELECT |
| ผล: `<QuerySet [<Question: Question object (1)>]>` | มี 1 แถวในตาราง — สังเกต 2 อย่าง: ① ที่เห็น `Question object (1)` แทนข้อความดี ๆ เพราะโมเดลนี้**ไม่ได้เขียน `__str__`** (เลข `(1)` คือค่า id) ② แถวนี้เป็น**แถวเก่าที่มีอยู่ก่อนแล้ว**ในฐานข้อมูล ไม่ใช่ตัวที่เพิ่งลบไป — ตัวที่ลบหายไปจริง | — |
| `filter_q = Question.objects.filter(pub_date__year=2024)` | กรองเอาเฉพาะแถวที่**ปีของ** `pub_date` = 2024 — `__year` คือ lookup พิเศษของฟิลด์วันที่ (ดึงเฉพาะปีมาเทียบ) ยังมี `__month`, `__day`, `__week_day` ด้วย | ❌ |
| ผล: `<QuerySet []>` | **ลิสต์ว่าง = ไม่เจอสักแถว** — เพราะข้อมูลในตารางไม่มีแถวไหน pub_date เป็นปี 2024 เลย ⚠️ ว่างไม่ใช่ error! `filter` ไม่เจอจะได้ QuerySet ว่างเสมอ (ต่างจาก `get` ที่ไม่เจอแล้ว error) | ✅ SELECT |

**เทียบกลับมาเป็นโปรเจคเราแบบบรรทัดต่อบรรทัด:**

```python
>>> from shop.models import Product, Brand, Category
>>> from django.utils import timezone

>>> b = Brand.objects.get(name='Astra')
>>> c = Category.objects.get(name='เมาส์')
>>> p = Product(name='Mouse DEMO-001', brand=b, category=c, price=590)  # ยังไม่ลง DB
>>> p.save()                                   # INSERT — p.id มีค่าแล้ว
>>> p.price = 490
>>> p.save()                                   # UPDATE แถวเดิม
>>> p.delete()                                 # DELETE
(1, {'shop.Product': 1})

>>> Product.objects.filter(created_at__year=2026).count()   # lookup __year กับฟิลด์วันที่
100
```

### 3.5 ข้อผิดพลาดยอดฮิตใน shell (เจอกันทุกห้องเรียน)

จากภาพตัวอย่างเดียวกัน บรรทัดสุดท้ายผู้พิมพ์กำลังจะพิมพ์:

```python
>>> filter_q=Question.objects.filter(text_startswith="")
```

⚠️ **บรรทัดนี้จะ error!** เพราะ `text_startswith` ใช้ underscore **ขีดเดียว** — Django จะเข้าใจว่ากำลังหาฟิลด์ชื่อ `text_startswith` (ซึ่งไม่มีในโมเดล) แล้วฟ้อง:

```text
django.core.exceptions.FieldError: Cannot resolve keyword 'text_startswith' into field.
Choices are: id, text, pub_date, ...
```

ที่ถูกต้องคือ underscore **สองขีด** คั่นระหว่างชื่อฟิลด์กับ lookup:

```python
>>> Question.objects.filter(text__startswith="What")     # ✅ text + __ + startswith
```

**สรุปข้อผิดพลาดที่พบบ่อยที่สุด 5 อันดับ:**

| อาการ | สาเหตุ | วิธีแก้ |
|-------|--------|--------|
| `NameError: name 'Product' is not defined` | ลืม import โมเดลหลังเปิด shell ใหม่ | `from shop.models import Product` |
| `FieldError: Cannot resolve keyword ...` | พิมพ์ `__` เป็นขีดเดียว หรือสะกดชื่อฟิลด์/lookup ผิด | เช็คว่าเป็น `ฟิลด์__lookup` ขีดคู่เสมอ |
| `DoesNotExist` | ใช้ `.get()` แล้วไม่เจอข้อมูล | ใช้ `.filter(...).first()` แทนถ้าไม่แน่ใจ |
| เห็น `Xxx object (1)` อ่านไม่รู้เรื่อง | โมเดลไม่มีเมธอด `__str__` | เพิ่ม `def __str__(self): return self.name` |
| แก้ค่าแล้วข้อมูลไม่เปลี่ยน | แก้ attribute แล้ว**ลืม `.save()`** | แก้เสร็จต้อง `.save()` ทุกครั้ง |

---

<a name="ส่วนที่-2"></a>
# ส่วนที่ 2 — ผ่าคำสั่ง import ใน shell

```python
>>> from shop.models import Product, Brand, Category
```

| ส่วน | อธิบาย |
|------|--------|
| `>>>` | **ไม่ใช่โค้ด!** คือเครื่องหมาย prompt ของ shell แปลว่า "พิมพ์คำสั่งตรงนี้" — เวลาพิมพ์ตามอย่าพิมพ์ `>>>` ไปด้วย |
| `from shop.models` | จากแพ็คเกจ `shop` (โฟลเดอร์ app ของเรา) → เข้าไปที่ไฟล์ `models.py` |
| `import Product, Brand, Category` | ดึง 3 คลาสนี้เข้ามาในหน่วยความจำของ shell — คั่นด้วย comma import ทีเดียวหลายตัวได้ |
| ทำไมต้องทำทุกครั้ง | shell ที่เปิดใหม่คือ Python เปล่า ๆ ยังไม่รู้จักโมเดลของเรา ถ้าไม่ import แล้วพิมพ์ `Product` จะเจอ `NameError: name 'Product' is not defined` |

```python
>>> from django.db.models import Avg, Max, Min, Sum, Count, Q, F
```

| ส่วน | อธิบาย |
|------|--------|
| `django.db.models` | โมดูลเดียวกับที่ใช้ในไฟล์ models.py นั่นแหละ แต่คราวนี้ดึง**เครื่องมือ query** |
| `Avg, Max, Min, Sum, Count` | ฟังก์ชันสรุปยอด (เฉลี่ย, มากสุด, น้อยสุด, ผลรวม, นับ) ใช้กับ `aggregate` / `annotate` |
| `Q` | ตัวห่อเงื่อนไข ทำให้ใช้ OR (`\|`) และ NOT (`~`) ได้ |
| `F` | ตัวอ้างถึง "ค่าของฟิลด์อื่นในแถวเดียวกัน" ใช้คำนวณในฐานข้อมูลโดยตรง |

---

<a name="ส่วนที่-3"></a>
# ส่วนที่ 3 — ผ่าคำสั่ง `Product.objects.all()`

```python
>>> Product.objects.all()
```

คำสั่งนี้ประกอบด้วย 3 ชิ้นต่อกันด้วยจุด (`.`):

```text
Product.objects.all()
   │       │      │
   │       │      └─ ③ เมธอด: "เอาทุกแถว"
   │       └─ ② Manager: ประตูทางเข้าตาราง
   └─ ① คลาสโมเดล: ตัวแทนตาราง shop_product
```

### ① `Product` — คลาสโมเดล

คือคลาสที่เราประกาศใน models.py — ตัวแทนของ**ตาราง** `shop_product` ทั้งตาราง (ยังไม่ใช่ข้อมูลแถวไหน)

### ② `.objects` — Manager

| คำถาม | คำตอบ |
|--------|-------|
| มันคืออะไร | object พิเศษที่ Django **แถมให้ทุกโมเดลอัตโนมัติ** เรียกว่า **Manager** |
| หน้าที่ | เป็น "ประตู" สำหรับคุยกับฐานข้อมูล — คำสั่ง query ทุกตัว (`all`, `filter`, `get`, `count`, `create`, ...) ต้องเรียกผ่านมัน |
| จำง่าย ๆ | `Product` = ตาราง, `Product.objects` = พนักงานที่วิ่งไปหยิบข้อมูลจากตารางให้เรา |
| เรียกข้ามขั้นได้ไหม | ไม่ได้ — `Product.all()` จะ error ทันที ต้องผ่าน `.objects` เสมอ |

### ③ `.all()` — เมธอด

สั่งพนักงานว่า "เอา**ทุกแถว** ไม่ต้องกรอง" — เทียบ SQL คือ `SELECT * FROM shop_product;`

### ⏱ เบื้องหลังที่มองไม่เห็น: Lazy Evaluation

บรรทัด `Product.objects.all()` เฉย ๆ **ยังไม่ยิง SQL จริง!** Django แค่จดไว้ว่า "จะเอาทุกแถวนะ" — SQL จะถูกยิงตอนเรา "ใช้ผลลัพธ์จริง" เท่านั้น เช่น พอ shell ต้องพิมพ์ผลออกจอ ตอนนั้นแหละถึงยิง SQL

---

<a name="ส่วนที่-4"></a>
# ส่วนที่ 4 — ผ่าผลลัพธ์ `<QuerySet [...]>` อ่านยังไง

```python
<QuerySet [<Product: Power Supply S3809-045 - 6,500 บาท>, <Product: Laptop C6684-081 - 50,300 บาท>, ...]>
```

แกะออกเป็นชั้น ๆ จากนอกเข้าใน:

```text
<QuerySet [ <Product: ...>, <Product: ...>, ... ]>
│        │ │                                │ │
│        │ │                                │ └─ ปิดท้าย
│        │ └─ สมาชิกแต่ละตัว = Product object │
│        └─ [ ] = ลิสต์ของผลลัพธ์             └─ "..." = ยังมีต่อ แต่ตัดการแสดงผล
└─ ชนิดของผลลัพธ์คือ QuerySet
```

| ส่วน | อธิบาย |
|------|--------|
| `<QuerySet ...>` | บอกว่าสิ่งที่ได้กลับมาคือ **QuerySet** — "ชุดผลลัพธ์" ที่หน้าตาคล้าย list (วนลูปได้, นับได้, slice ได้) |
| `[...]` | สมาชิกข้างในเรียงเป็นลิสต์ |
| `<Product: Power Supply S3809-045 - 6,500 บาท>` | สมาชิก 1 ตัว = ข้อมูล **1 แถว** ห่อเป็น Product object — รูปแบบคือ `<ชื่อคลาส: ข้อความจาก __str__>` |
| `Power Supply S3809-045 - 6,500 บาท` | ข้อความส่วนนี้มาจากเมธอด `__str__` ที่เราเขียนไว้เป๊ะ ๆ (`f'{self.name} - {self.price:,.0f} บาท'`) — นี่คือเหตุผลว่าทำไมต้องเขียน `__str__`! |
| `...` ตอนท้าย | ข้อมูลมี 100 แถว แต่ shell **แสดงตัวอย่างแค่ 20 แถวแรก**แล้วละไว้ — ป้องกันจอเต็ม ไม่ได้แปลว่าข้อมูลมีแค่นี้ |

---

<a name="ส่วนที่-5"></a>
# ส่วนที่ 5 — ผ่า for loop ใน shell

```python
>>> for p in Product.objects.all()[:5]:
...     print(p.name, p.price)
...
Power Supply S3809-045 6500.00
Laptop C6684-081 50300.00
PC Case N3855-014 1600.00
Laptop W5685-049 65700.00
Motherboard A4180-053 13700.00
```

## บรรทัดที่ 1: `for p in Product.objects.all()[:5]:`

| ส่วน | อธิบาย |
|------|--------|
| `for ... in ...:` | โครงสร้างวนลูปของ Python — หยิบสมาชิกจากกลุ่มมาทีละตัว |
| `p` | ตัวแปรรับค่าในแต่ละรอบ — รอบแรก `p` = สินค้าแถวที่ 1, รอบสอง = แถวที่ 2, ... (จะตั้งชื่ออื่นก็ได้ เช่น `product` แต่ `p` สั้นดี) |
| `Product.objects.all()` | ชุดข้อมูลทุกแถว (จากส่วนที่ 3) |
| `[:5]` | **slicing** — ตัดเอาแค่ 5 ตัวแรก (index 0 ถึง 4) เหมือน list ปกติของ Python |
| `:` ท้ายบรรทัด | บอกว่า "คำสั่งในลูปเริ่มบรรทัดถัดไป" |

> 📌 ฉลาดกว่าที่คิด: `[:5]` ไม่ได้ดึง 100 แถวมาแล้วค่อยตัด — Django แปลงเป็น SQL `LIMIT 5`
> คือขอฐานข้อมูลมาแค่ 5 แถวตั้งแต่ต้น ประหยัดทั้งเวลาและหน่วยความจำ

## บรรทัดที่ 2: `...     print(p.name, p.price)`

| ส่วน | อธิบาย |
|------|--------|
| `...` | prompt ของ shell (เหมือน `>>>`) แปลว่า "กำลังพิมพ์คำสั่งต่อเนื่องหลายบรรทัด" — **ไม่ต้องพิมพ์ตาม** |
| ย่อหน้า (indent) | ต้องเคาะวรรค (แนะนำ 4 เคาะ) ก่อน `print` เพื่อบอกว่าบรรทัดนี้**อยู่ในลูป** — ไม่ย่อหน้า = `IndentationError` |
| `p.name` | เข้าถึงค่าในคอลัมน์ `name` ของแถวที่ `p` ถืออยู่ — ใช้จุด (`.`) ตามด้วยชื่อฟิลด์ที่ประกาศใน models.py |
| `p.price` | ค่าคอลัมน์ `price` — ได้เป็นชนิด `Decimal` |
| `print(a, b)` | พิมพ์สองค่าคั่นด้วยช่องว่าง 1 ช่อง |

## บรรทัดที่ 3: `...` (ว่างเปล่า)

ใน shell ต้อง**กด Enter บนบรรทัดว่างอีกครั้ง** เพื่อบอกว่า "จบลูปแล้ว เริ่มทำงานได้" — ลูปถึงจะรัน

## ทำไมผลลัพธ์แสดง `6500.00` ไม่ใช่ `6,500 บาท`?

จุดที่หลายคนงง! เทียบกัน:

| คำสั่ง | ผลลัพธ์ | เพราะ |
|--------|---------|-------|
| `print(p)` | `Power Supply S3809-045 - 6,500 บาท` | print ทั้ง object → Python เรียก `__str__` ที่เราแต่งรูปแบบไว้ |
| `print(p.price)` | `6500.00` | print เฉพาะค่าฟิลด์ price → ได้ค่า `Decimal('6500.00')` **ดิบ ๆ** ตรงจากฐานข้อมูล (decimal_places=2 เลยมีทศนิยม 2 ตำแหน่ง) ไม่ผ่าน `__str__` ของ Product |

ถ้าอยากให้สวยเอง ก็จัดรูปแบบใน f-string:

```python
>>> for p in Product.objects.all()[:5]:
...     print(f'{p.name:30} {p.price:>10,.0f} บาท')
...
Power Supply S3809-045              6,500 บาท
Laptop C6684-081                   50,300 บาท
```

| รูปแบบ | ความหมาย |
|--------|----------|
| `{p.name:30}` | จองพื้นที่ 30 ตัวอักษร ชิดซ้าย (คอลัมน์เลยตรงกัน) |
| `{p.price:>10,.0f}` | จอง 10 ตัวอักษร ชิด**ขวา** (`>`), คั่นหลักพันด้วย `,`, ทศนิยม 0 ตำแหน่ง |

---

<a name="ส่วนที่-6"></a>
# ส่วนที่ 6 — ผ่าคำสั่ง `.get()` และการเข้าถึงข้อมูลผ่านจุด

```python
>>> p = Product.objects.get(name='Laptop C6684-081')
```

| ส่วน | อธิบาย |
|------|--------|
| `p =` | เก็บผลลัพธ์ใส่ตัวแปร `p` ไว้ใช้ต่อหลายบรรทัด (ไม่เก็บก็ได้ แต่จะเรียกใช้ซ้ำไม่ได้) |
| `.get(...)` | ขอข้อมูล "**ตัวเดียวเป๊ะ ๆ**" — ได้กลับมาเป็น Product object เดี่ยว ๆ (ไม่ใช่ QuerySet) |
| `name='Laptop C6684-081'` | เงื่อนไข: คอลัมน์ name ต้องเท่ากับข้อความนี้เป๊ะ (ตัวพิมพ์เล็กใหญ่ต้องตรง) |

```python
>>> p.price
Decimal('50300.00')
>>> p.brand.name
'ZenCore'
```

### ผ่า `p.brand.name` — จุดสองชั้นทำงานยังไง

```text
p        .brand              .name
│        │                   │
│        │                   └─ ③ ฟิลด์ name ของ Brand object นั้น → 'ZenCore'
│        └─ ② ตามลูกศร FK ไปหยิบ Brand object ทั้งแถวที่สินค้านี้ชี้ไป
└─ ① Product object (สินค้า 1 แถว)
```

| ขั้น | เกิดอะไรขึ้น |
|------|-------------|
| ① `p` | ถือข้อมูลสินค้า 1 แถว ซึ่งในฐานข้อมูลจริงมีแค่ตัวเลข `brand_id = 2` |
| ② `.brand` | Django เห็นว่าเราอยากได้ "ทั้งก้อน" ของแบรนด์ → **ยิง SQL เพิ่ม 1 ครั้ง**ไปหยิบแถว id=2 จากตาราง shop_brand มาห่อเป็น Brand object |
| ③ `.name` | อ่านฟิลด์ name จาก Brand object → ได้ `'ZenCore'` |

> 📌 ขั้น ② นี่แหละคือที่มาของปัญหา **N+1 query** — ถ้าวนลูปสินค้า 100 ตัวแล้วแตะ `.brand` ทุกตัว จะยิง SQL เพิ่ม 100 ครั้ง วิธีแก้คือ `select_related('brand')` (ดูบทที่ 12 ของ Tutorial หลัก)

---

<a name="ส่วนที่-7"></a>
# ส่วนที่ 7 — ผ่าคำสั่ง `.filter()` และ underscore สองตัว

```python
>>> Product.objects.filter(brand__name='Astra', price__lt=20000)
```

| ส่วน | อธิบาย |
|------|--------|
| `.filter(...)` | ขอ "หลายแถวที่ตรงเงื่อนไข" — ได้ QuerySet เสมอ (ต่อให้เจอ 0 หรือ 1 แถวก็เป็น QuerySet) |
| เงื่อนไข 2 ตัวคั่น comma | ทุกเงื่อนไขต้องจริง**พร้อมกัน** (AND) |

### ผ่า `brand__name='Astra'` — underscore สองตัวหมายถึงอะไร

```text
brand    __    name    =    'Astra'
│        │     │            │
│        │     │            └─ ค่าที่ต้องการ
│        │     └─ ฟิลด์ name ในตาราง Brand
│        └─ "เดินข้ามตาราง" ผ่าน FK
└─ ฟิลด์ brand (FK) ในตาราง Product
```

อ่านเป็นภาษาคนว่า: *"เอาสินค้าที่ → แบรนด์ของมัน → ชื่อ → เท่ากับ Astra"*
เทียบ SQL: Django สร้าง `JOIN` ให้อัตโนมัติ:

```sql
SELECT * FROM shop_product
JOIN shop_brand ON shop_product.brand_id = shop_brand.id
WHERE shop_brand.name = 'Astra';
```

### ผ่า `price__lt=20000` — underscore กับ lookup

```text
price    __    lt    =    20000
│        │     │
│        │     └─ lookup: "less than" (น้อยกว่า)
│        └─ คั่นระหว่างชื่อฟิลด์กับ lookup
└─ ฟิลด์ price ในตาราง Product เอง (ไม่ข้ามตาราง)
```

> 📌 **สรุปกฎ `__` (underscore 2 ตัว):** Django ตีความจากซ้ายไปขวา —
> ถ้าคำถัดไปเป็น**ชื่อฟิลด์ของตารางที่เชื่อมกัน** = เดินข้ามตาราง,
> ถ้าเป็น**คำสั่งเปรียบเทียบ** (lt, gt, contains, in, ...) = ใช้เป็น lookup
> ต่อกันยาว ๆ ก็ได้ เช่น `brand__name__in=['Astra', 'Quantum']` (ข้ามตาราง → ฟิลด์ → lookup)

### ทำไมไม่เขียน `price < 20000` ตรง ๆ?

เพราะในวงเล็บของ `filter()` เราส่ง **keyword argument** ของ Python ซึ่งใช้ได้แค่รูป `ชื่อ=ค่า` — ใส่เครื่องหมาย `<` `>` ไม่ได้ Django เลยออกแบบให้ยัดตัวเปรียบเทียบเข้าไปในชื่อผ่าน `__lt`, `__gt` แทน

---

<a name="ส่วนที่-8"></a>
# ส่วนที่ 8 — ผ่าคำสั่ง `.order_by()` และ slicing

```python
>>> Product.objects.order_by('-price')[:5]
```

```text
Product.objects  .order_by('-price')  [:5]
                 │          │          │
                 │          │          └─ ③ เอาแค่ 5 ตัวแรก → SQL: LIMIT 5
                 │          └─ ② '-' นำหน้า = เรียงจากมากไปน้อย (DESC)
                 └─ ① เรียงลำดับตามฟิลด์ price
```

| ส่วน | อธิบาย |
|------|--------|
| `'price'` | เรียงน้อย → มาก (ASC) — ส่งชื่อฟิลด์เป็น **string** ต้องมี quote |
| `'-price'` | ขีดลบนำหน้า = เรียงมาก → น้อย (DESC) |
| `order_by('category__name', '-price')` | เรียงหลายชั้น: หมวดหมู่ก่อน (ก-ฮ) ถ้าหมวดเดียวกันค่อยเรียงราคาแพงก่อน |
| `[:5]` | 5 ตัวแรกหลังเรียงแล้ว → รวมกันแปลว่า "Top 5 แพงสุด" |
| `[5:10]` | ข้าม 5 ตัวแรก เอาอันดับ 6–10 → SQL: `LIMIT 5 OFFSET 5` |

> ⚠️ `[-1]` (index ติดลบ) ใช้กับ QuerySet ไม่ได้ จะเจอ error — เพราะฐานข้อมูลไม่รู้จัก "นับจากท้าย" ให้ใช้ `.last()` หรือเรียงกลับด้านแล้ว `.first()` แทน

---

<a name="ส่วนที่-9"></a>
# ส่วนที่ 9 — ผ่าคำสั่ง `.aggregate()` และ `.annotate()`

## 9.1 ผ่า aggregate

```python
>>> Product.objects.aggregate(Avg('price'))
{'price__avg': Decimal('15436')}
```

| ส่วน | อธิบาย |
|------|--------|
| `.aggregate(...)` | "ยุบ" ทั้ง QuerySet เหลือ**ค่าสรุปค่าเดียว** — ได้ผลเป็น dictionary ธรรมดา (ไม่ใช่ QuerySet แล้ว ใช้ .filter ต่อไม่ได้) |
| `Avg('price')` | ฟังก์ชันสรุปแบบ "ค่าเฉลี่ย" ของฟิลด์ price — ชื่อฟิลด์ส่งเป็น string |
| `'price__avg'` | **key ใน dict ที่ Django ตั้งให้อัตโนมัติ** จากสูตร `ชื่อฟิลด์__ชื่อฟังก์ชัน` |
| `Decimal('15436')` | ค่าเฉลี่ยจริง = 15,436 บาท |

ตั้งชื่อ key เองได้ด้วย keyword argument:

```python
>>> Product.objects.aggregate(avg_price=Avg('price'))
{'avg_price': Decimal('15436')}
     │
     └─ ใช้ชื่อที่เราตั้ง แทน price__avg
```

## 9.2 ผ่า annotate

```python
>>> Brand.objects.annotate(total=Count('products')).order_by('-total')
```

```text
Brand.objects  .annotate(  total  =  Count('products')  )  .order_by('-total')
│              │           │         │                     │
│              │           │         │                     └─ ⑤ เรียงตามคอลัมน์ใหม่ มาก→น้อย
│              │           │         └─ ④ นับจำนวนสินค้า "ของแบรนด์นั้น ๆ"
│              │           │            ('products' = related_name ที่ตั้งไว้ใน FK!)
│              │           └─ ③ ชื่อคอลัมน์ชั่วคราวที่เราตั้ง
│              └─ ② "แปะค่าคำนวณเพิ่ม" ให้แต่ละแถว
└─ ① เริ่มจากตารางแบรนด์ (10 แถว)
```

| จุดต่างสำคัญ | `aggregate` | `annotate` |
|--------------|------------|-----------|
| ผลลัพธ์ | dict ค่าเดียว (จบเลย) | QuerySet เดิม + คอลัมน์ใหม่ (query ต่อได้) |
| ตัวอย่างการใช้ต่อ | — | `.filter(total__gt=10)`, `.order_by('-total')`, เข้าถึงเป็น `b.total` |
| เทียบ SQL | `SELECT AVG(price)` | `GROUP BY` + ฟังก์ชันสรุปต่อกลุ่ม |

หลัง annotate แล้ว แต่ละ Brand object จะมี attribute ใหม่ `total` ใช้ได้เหมือนฟิลด์จริง:

```python
>>> b = Brand.objects.annotate(total=Count('products')).first()
>>> b.name, b.total
('Astra', 18)
```

---

<a name="ส่วนที่-10"></a>
# ส่วนที่ 10 — ผ่าคำสั่งสร้าง / แก้ / ลบข้อมูล

## 10.1 ผ่า `.create()`

```python
>>> p = Product.objects.create(
...     name='Mouse TEST-999',
...     brand=b,
...     category=c,
...     description='เมาส์ทดสอบ',
...     price=999
... )
```

| ส่วน | อธิบาย |
|------|--------|
| `.create(...)` | สร้าง object + บันทึกลงฐานข้อมูล **ในคำสั่งเดียว** (เทียบ SQL: `INSERT INTO ...`) |
| `name='Mouse TEST-999'` | ส่งค่าเข้าฟิลด์แบบ keyword argument ทีละฟิลด์ |
| `brand=b` | ฟิลด์ FK ต้องส่ง **object ทั้งตัว** (ตัวแปร `b` ที่ get มาก่อนหน้า) ไม่ใช่ string ชื่อแบรนด์ — หรือจะส่งเป็น `brand_id=1` (ตัวเลข id) ก็ได้ |
| `price=999` | ส่ง int ธรรมดาได้ Django แปลงเป็น Decimal ให้เอง |
| ไม่ต้องส่ง `id`, `created_at` | สองตัวนี้อัตโนมัติ (`id` รันต่อจากเดิม, `created_at` มาจาก `auto_now_add=True`) |
| ค่าที่คืนมา | object ที่เพิ่งสร้างเสร็จ (มี id แล้ว) — เก็บใส่ `p` ไว้ใช้ต่อได้เลย |

## 10.2 ผ่าการแก้ไขทีละตัว

```python
>>> p.price = 899      # ① แก้ค่าใน "หน่วยความจำ" — ฐานข้อมูลยังไม่เปลี่ยน!
>>> p.save()           # ② สั่งบันทึก → SQL UPDATE ถูกยิงตอนนี้
```

> ⚠️ จุดพลาดคลาสสิก: แก้ค่าแล้ว**ลืม `.save()`** — ใน shell เห็นค่าใหม่ แต่พอเปิดใหม่ค่าเดิมกลับมา เพราะไม่เคยบันทึกจริง

## 10.3 ผ่า `.update()` — แก้หลายแถวรวดเดียว

```python
>>> Product.objects.filter(name__contains='TEST').update(price=500)
2
```

| ส่วน | อธิบาย |
|------|--------|
| `.filter(...)` ก่อน | ล็อคเป้าก่อนว่าจะแก้แถวไหนบ้าง |
| `.update(price=500)` | แก้ทุกแถวที่กรองได้ **ใน SQL คำสั่งเดียว** — เร็วกว่าวนลูป save ทีละตัวมาก |
| `2` ที่คืนมา | จำนวนแถวที่ถูกแก้จริง |
| ข้อจำกัด | `.update()` ใช้กับ QuerySet เท่านั้น — object เดี่ยวจาก `.get()` ต้องใช้วิธี `.save()` |

## 10.4 ผ่า `.delete()`

```python
>>> Product.objects.filter(name__contains='TEST').delete()
(2, {'shop.Product': 2})
```

| ส่วน | อธิบาย |
|------|--------|
| `.delete()` | ลบทุกแถวใน QuerySet ทิ้งถาวร (SQL: `DELETE FROM ... WHERE ...`) |
| `(2, {...})` | tuple ตอบกลับ: ลบไปทั้งหมด 2 แถว, แจกแจงว่าเป็นโมเดลไหนกี่แถว (ถ้ามี CASCADE ลบลูกตาม จะเห็นโมเดลอื่นโผล่ใน dict ด้วย) |

> 🔥 **อันตรายสุดในเอกสารนี้:** `Product.objects.all().delete()` = ลบเกลี้ยงทั้งตาราง ไม่มี undo!
> โชคดีที่โปรเจคเราแก้ได้ด้วย `python manage.py load_products` — ข้อมูล 100 รายการกลับมาครบ

## 10.5 ผ่า `.get_or_create()`

```python
>>> brand, created = Brand.objects.get_or_create(name='Astra')
>>> created
False
```

| ส่วน | อธิบาย |
|------|--------|
| `.get_or_create(...)` | ลอง `get` ก่อน — เจอก็คืนตัวเดิม, ไม่เจอก็ `create` ใหม่ให้เลย |
| `brand, created =` | คำสั่งนี้คืน **tuple 2 ค่า** เลยต้องรับด้วยตัวแปร 2 ตัว (เทคนิค Python เรียกว่า unpacking) |
| `brand` | Brand object (ไม่ว่าจะของเดิมหรือสร้างใหม่) |
| `created` | `True` = เพิ่งสร้างใหม่, `False` = มีอยู่แล้วหยิบของเดิมมา |
| ใช้จริงที่ไหน | ในไฟล์ `load_products.py` ของเราใช้ตัวนี้กับ Brand/Category — รันกี่รอบแบรนด์ก็ไม่ซ้ำ |

---

# 🎯 สรุปภาพรวม — โครงสร้างประโยค Query ที่ต้องจำ

```text
┌─────────────────────────────────────────────────────────────┐
│   Model.objects.คำสั่ง(ฟิลด์__ข้ามตาราง__lookup=ค่า)              │
│     │      │      │      │        │        │                 │
│     │      │      │      │        │        └─ วิธีเปรียบเทียบ    │
│     │      │      │      │        └─ เดินผ่าน FK (มีได้หลายชั้น)  │
│     │      │      │      └─ ชื่อฟิลด์ตามที่ประกาศใน models.py     │
│     │      │      └─ all / filter / get / order_by / ...      │
│     │      └─ Manager (ประตูเข้าตาราง — ห้ามข้าม)               │
│     └─ คลาสโมเดล (ตัวแทนตาราง)                                │
└─────────────────────────────────────────────────────────────┘
```

| สิ่งที่ได้กลับมา | จากคำสั่ง | ใช้ต่อยังไง |
|-----------------|-----------|------------|
| **QuerySet** (หลายแถว) | `all()`, `filter()`, `exclude()`, `order_by()`, `annotate()` | filter ต่อ, วนลูป, slice, count ได้ |
| **Object เดี่ยว** (1 แถว) | `get()`, `first()`, `last()`, `create()` | เข้าถึงฟิลด์ด้วยจุด `.name` `.price`, แก้แล้ว `.save()` |
| **ตัวเลข / dict / bool** | `count()`, `aggregate()`, `exists()`, `update()`, `delete()` | ค่าธรรมดา จบที่ตรงนั้น query ต่อไม่ได้ |

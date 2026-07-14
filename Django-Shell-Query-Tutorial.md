# 📘 สอน Query ข้อมูลด้วย Django ORM ผ่าน `python manage.py shell`

> เอกสารประกอบการสอน — ใช้ข้อมูลจริงจาก app `shop` (สินค้าคอมพิวเตอร์ 100 รายการ, 10 แบรนด์, 16 หมวดหมู่)
> ทุกตัวอย่างในเอกสารนี้**รันได้จริง** และผลลัพธ์ที่แสดงคือ**ผลลัพธ์จริงจากฐานข้อมูล**

---

## สารบัญ

| บทที่ | หัวข้อ                                                                           |
| ---------- | -------------------------------------------------------------------------------------- |
| 0          | เตรียมความพร้อม — รู้จัก Django ORM และ Django Shell          |
| 1          | รู้จักโครงสร้าง Models                                                  |
| 2          | Query พื้นฐาน — all, count, first, last, get                                   |
| 3          | การกรองข้อมูลด้วย filter และ exclude                               |
| 4          | Field Lookups — เครื่องมือกรองขั้นเทพ                            |
| 5          | การเรียงลำดับและตัดข้อมูล (order_by, slicing)                 |
| 6          | เลือกเฉพาะคอลัมน์ที่ต้องการ (values, values_list, distinct) |
| 7          | Query ข้ามตาราง (ForeignKey)                                                  |
| 8          | Q Objects — เงื่อนไข OR / NOT                                                 |
| 9          | Aggregate — สรุปยอดทั้งตาราง                                          |
| 10         | Annotate — Group By ฉบับ Django                                                   |
| 11         | เพิ่ม แก้ไข ลบข้อมูล (CRUD)                                          |
| 12         | เทคนิคระดับโปร — select_related, F, ดู SQL จริง                   |
| 13         | โจทย์ฝึกหัด 20 ข้อ พร้อมเฉลย                                    |

---

# บทที่ 0 — เตรียมความพร้อม: รู้จัก Django ORM และ Django Shell

## 0.1 การ Query ข้อมูลด้วย Django ORM คืออะไร

**ORM (Object-Relational Mapping)** คือระบบของ Django ที่เป็น "ล่ามแปลภาษา" ระหว่างโลก 2 ใบ:
โลกของ **Python** (คลาส, object) กับโลกของ**ฐานข้อมูล** (ตาราง, แถว, SQL)

ปกติถ้าอยากดึงข้อมูลจากฐานข้อมูล เราต้องเขียนภาษา SQL เอง:

```sql
SELECT * FROM shop_product WHERE price < 5000;
```

แต่พอมี ORM เราเขียน **Python ล้วน ๆ** แทน แล้ว Django แปลเป็น SQL ให้เบื้องหลัง:

```python
Product.objects.filter(price__lt=5000)
```

การจับคู่ระหว่าง 2 โลกเป็นแบบนี้ — จำตารางนี้ได้ อ่านโค้ดออกทั้งเอกสาร:

| โลก Python (ORM)               | โลกฐานข้อมูล (SQL)   | ตัวอย่างในโปรเจคเรา             |
| --------------------------------- | -------------------------------- | -------------------------------------------------- |
| คลาสโมเดล 1 คลาส     | ตาราง 1 ตาราง          | คลาส`Product` → ตาราง `shop_product` |
| object 1 ตัว                   | แถวข้อมูล 1 แถว      | `p = Product.objects.first()`                    |
| attribute ของ object           | คอลัมน์ในแถวนั้น | `p.price`, `p.name`                            |
| `objects.all()` / `.filter()` | `SELECT` / `WHERE`           | ดึงข้อมูล                                 |
| `.create()` / `.save()`       | `INSERT` / `UPDATE`          | เพิ่ม/แก้ข้อมูล                      |
| `.delete()`                     | `DELETE`                       | ลบข้อมูล                                   |

**ทำไมไม่เขียน SQL ตรง ๆ?**

1. **ปลอดภัยกว่า** — ORM กันการโจมตีแบบ SQL Injection ให้อัตโนมัติ
2. **ย้ายฐานข้อมูลได้ฟรี** — โค้ด Python เดิมใช้ได้ทั้ง SQLite, MySQL, PostgreSQL โดยไม่ต้องแก้สักบรรทัด
3. **ได้ object กลับมาใช้ต่อทันที** — ผลลัพธ์เป็น Python object เขียน `p.brand.name` ต่อได้เลย ไม่ต้อง parse ผลดิบเอง

> 💡 อยากเห็นว่า ORM แปลเป็น SQL อะไร พิมพ์ `print(Product.objects.filter(price__lt=5000).query)` ใน shell ได้เลย (รายละเอียดในบทที่ 12)

## 0.2 python manage.py shell คืออะไร

**Django Shell** คือหน้าจอพิมพ์คำสั่ง Python แบบโต้ตอบ (พิมพ์ปุ๊บ เห็นผลปั๊บ) ที่**โหลดโปรเจค Django ของเราเข้ามาให้พร้อมใช้** — เหมาะที่สุดสำหรับทดลอง query, ตรวจข้อมูล, และ debug ก่อนเอาโค้ดไปเขียนจริงใน views

**ต่างจาก Python shell ธรรมดายังไง?**

|                                      | `python3` (shell ธรรมดา) | `python manage.py shell` (Django Shell)                              |
| ------------------------------------ | -------------------------------- | ---------------------------------------------------------------------- |
| รู้จักโปรเจคเราไหม | ❌ ไม่รู้จักเลย      | ✅ โหลด`settings.py` ให้อัตโนมัติ                    |
| import โมเดลได้ไหม        | ❌ เจอ error ทันที       | ✅`from shop.models import Product` ได้เลย                     |
| ต่อกับฐานข้อมูลไหม | ❌                               | ✅ query/เพิ่ม/ลบข้อมูล**จริง**ได้ทันที |
| เหมาะกับ                     | ทดลอง Python ทั่วไป   | ทดลองทุกอย่างที่เกี่ยวกับโปรเจค Django  |

> ⚠️ ย้ำอีกครั้ง: ข้อมูลใน Django Shell คือ**ฐานข้อมูลจริง**ของโปรเจค — สั่ง `.delete()` คือหายจริง
> โชคดีที่โปรเจคเรากู้ได้เสมอด้วย `python manage.py load_products`

## 0.3 การใช้งาน python manage.py shell

**ขั้นที่ 1 — เปิด:** ไปที่โฟลเดอร์ที่มีไฟล์ `manage.py` แล้วพิมพ์:

```bash
python manage.py shell
```

พอเห็นเครื่องหมาย `>>>` แปลว่าพร้อมใช้งาน (เครื่องหมายนี้ shell พิมพ์ให้เอง เราไม่ต้องพิมพ์ตาม)

**ขั้นที่ 2 — import โมเดลก่อนเสมอ** (ทุกครั้งที่เปิด shell ใหม่):

```python
>>> from shop.models import Product, Brand, Category
```

**ขั้นที่ 3 — ลองวงจรชีวิตข้อมูลครบรอบ** สร้าง → บันทึก → แก้ → ลบ
(ตัวอย่างนี้อ้างถึงแบรนด์ Astra ในฐานข้อมูล — ถ้ายังไม่เคยโหลดข้อมูล ให้ทำหัวข้อ 0.4 ก่อนแล้วค่อยกลับมา):

```python
>>> b = Brand.objects.get(name='Astra')
>>> c = Category.objects.get(name='เมาส์')

>>> p = Product(name='Mouse DEMO-001', brand=b, category=c, price=590)
>>> p.save()          # ① INSERT — ก่อน save ข้อมูลอยู่แค่ในหน่วยความจำ ยังไม่ลงฐานข้อมูล!

>>> p.price = 490
>>> p.save()          # ② คราวนี้เป็น UPDATE — เพราะ p.id มีค่าแล้ว Django รู้ว่าเป็นแถวเดิม

>>> p.delete()        # ③ DELETE — ตอบกลับว่าลบอะไรไปกี่แถว
(1, {'shop.Product': 1})
```

จุดที่ต้องเข้าใจจากตัวอย่างนี้:

- `Product(...)` เฉย ๆ = สร้าง object **ในหน่วยความจำเท่านั้น** ต้อง `.save()` ข้อมูลถึงลงฐานข้อมูล
- `.save()` ฉลาดพอที่จะรู้เอง: object ใหม่ (ยังไม่มี id) → `INSERT` / object เก่า (มี id แล้ว) → `UPDATE`
- `.delete()` ตอบกลับเป็น tuple บอกจำนวนแถวที่ลบ

**ขั้นที่ 4 — ออกจาก shell:** พิมพ์ `exit()` หรือกด `Ctrl+D` (Mac/Linux) / `Ctrl+Z` แล้ว Enter (Windows)

> 📖 อยากได้คำอธิบายแบบผ่าทีละบรรทัด (รวมข้อผิดพลาดยอดฮิต เช่น `text_startswith` ขีดเดียวที่ทำให้ `FieldError`, หรือทำไมเห็น `object (1)` แทนชื่อสวย ๆ) อ่านต่อได้ที่ [Django-Code-Explained-Line-by-Line.md](Django-Code-Explained-Line-by-Line.md) ส่วนเสริม หัวข้อ 3.4–3.5

## 0.4 โหลดข้อมูลเข้าฐานข้อมูล (ทำครั้งแรกครั้งเดียว)

```bash
python manage.py migrate
python manage.py load_products
```

ผลลัพธ์:

```text
เสร็จสิ้น: เพิ่มใหม่ 100 รายการ, อัปเดต 0 รายการ (Brand 10, Category 16, Product 100)
```

> 💡 คำสั่ง `load_products` รันซ้ำกี่ครั้งก็ได้ ข้อมูลจะไม่ซ้ำ เพราะใช้ `update_or_create`
> เหมาะกับกรณีนักเรียนเผลอลบหรือแก้ข้อมูลจนเละ — รันใหม่ข้อมูลก็กลับมาเหมือนเดิม

## 0.5 import models ที่ต้องใช้

พิมพ์บรรทัดนี้ก่อนเสมอทุกครั้งที่เปิด shell ใหม่:

```python
from shop.models import Product, Brand, Category
```

และถ้าจะใช้ฟังก์ชันสรุปยอด/เงื่อนไขพิเศษ ให้ import เพิ่ม:

```python
from django.db.models import Avg, Max, Min, Sum, Count, Q, F
```

> 💡 ออกจาก shell ด้วยคำสั่ง `exit()` หรือกด `Ctrl+D` (Mac/Linux) / `Ctrl+Z` แล้ว Enter (Windows)

---

# บทที่ 1 — รู้จักโครงสร้าง Models

ข้อมูลของเราแบ่งเป็น 3 ตาราง เชื่อมกันด้วย ForeignKey:

```text
┌──────────┐         ┌─────────────────┐         ┌────────────┐
│  Brand   │ 1     N │     Product     │ N     1 │  Category  │
│──────────│◄────────│─────────────────│────────►│────────────│
│ name     │         │ name            │         │ name       │
└──────────┘         │ brand (FK)      │         └────────────┘
                     │ category (FK)   │
                     │ description     │
                     │ price           │
                     │ created_at      │
                     └─────────────────┘
```

```python
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
```

## ข้อมูลที่มีในระบบ

**10 แบรนด์:** Astra, ByteCraft, CoreLink, Nexora, NovaTech, Orionix, PixelForge, Quantum, VoltEdge, ZenCore

**16 หมวดหมู่:** การ์ดจอ, คอมพิวเตอร์ตั้งโต๊ะ, คีย์บอร์ด, จอภาพ, ชุดหูฟัง, ซีพียู, พาวเวอร์ซัพพลาย, หน่วยความจำ, อุปกรณ์จัดเก็บข้อมูล, อุปกรณ์เครือข่าย, เครื่องสำรองไฟ, เคสคอมพิวเตอร์, เมนบอร์ด, เมาส์, เว็บแคม, โน้ตบุ๊ก

---

# บทที่ 2 — Query พื้นฐาน

## 2.1 ดึงข้อมูลทั้งหมด — `.all()`

```python
>>> Product.objects.all()
<QuerySet [<Product: Power Supply S3809-045 - 6,500 บาท>, <Product: Laptop C6684-081 - 50,300 บาท>, ...]>
```

> 📌 `Product.objects` คือ **Manager** — ประตูทางเข้าสู่ตาราง
> ผลลัพธ์ที่ได้เรียกว่า **QuerySet** — เปรียบเหมือน "รายการผลลัพธ์" ที่วนลูปต่อได้

วนลูปแสดงทีละตัว:

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

## 2.2 นับจำนวน — `.count()`

```python
>>> Product.objects.count()
100
>>> Brand.objects.count()
10
>>> Category.objects.count()
16
```

## 2.3 ตัวแรก / ตัวสุดท้าย — `.first()` / `.last()`

```python
>>> Product.objects.first()
<Product: Power Supply S3809-045 - 6,500 บาท>

>>> Product.objects.last()
<Product: Router X3500-076 - 1,900 บาท>
```

## 2.4 ดึงข้อมูล "ตัวเดียวเป๊ะ ๆ" — `.get()`

```python
>>> p = Product.objects.get(name='Laptop C6684-081')
>>> p.price
Decimal('50300.00')
>>> p.brand.name        # เข้าถึงข้อมูลแบรนด์ผ่าน FK ได้เลย
'ZenCore'
>>> p.category.name
'โน้ตบุ๊ก'
>>> p.description
'Intel Core i7, RAM 8GB, SSD 2TB NVMe, จอ 16 นิ้ว 2.5K, สีดำ'
```

ดึงด้วย id (primary key):

```python
>>> Product.objects.get(id=1)
<Product: Power Supply S3809-045 - 6,500 บาท>
>>> Product.objects.get(pk=1)      # pk = primary key เขียนแบบนี้ก็ได้
<Product: Power Supply S3809-045 - 6,500 บาท>
```

## ⚠️ ข้อควรระวังของ `.get()`

`.get()` ต้องเจอ **1 รายการเท่านั้น** ไม่งั้น error:

```python
>>> Product.objects.get(name='ไม่มีสินค้านี้')
# ❌ shop.models.Product.DoesNotExist: Product matching query does not exist.

>>> Product.objects.get(brand__name='Astra')
# ❌ shop.models.Product.MultipleObjectsReturned: get() returned more than one Product -- it returned 18!
```

| ต้องการ                                                 | ใช้                                                              |
| -------------------------------------------------------------- | ------------------------------------------------------------------- |
| หลายรายการ                                           | `.filter()`                                                       |
| รายการเดียวแน่นอน (เช่นค้นด้วย id) | `.get()`                                                          |
| รายการเดียว แต่ไม่แน่ใจว่ามีไหม  | `.filter(...).first()` (ไม่เจอได้ `None` ไม่ error) |

---

# บทที่ 3 — การกรองข้อมูลด้วย filter และ exclude

## 3.1 `.filter()` — เอาเฉพาะที่ตรงเงื่อนไข (เหมือน WHERE ใน SQL)

```python
>>> Product.objects.filter(category__name='โน้ตบุ๊ก')
<QuerySet [<Product: Laptop C6684-081 - 50,300 บาท>, <Product: Laptop W5685-049 - 65,700 บาท>,
 <Product: Laptop M2295-065 - 60,100 บาท>, <Product: Laptop Q4376-017 - 52,800 บาท>,
 <Product: Laptop G9831-033 - 23,900 บาท>, <Product: Laptop S2279-097 - 40,000 บาท>,
 <Product: Laptop A3909-001 - 55,500 บาท>]>

>>> Product.objects.filter(category__name='โน้ตบุ๊ก').count()
7
```

## 3.2 หลายเงื่อนไขพร้อมกัน (AND)

ใส่หลายเงื่อนไขคั่นด้วย comma = ทุกเงื่อนไขต้องเป็นจริง:

```python
>>> Product.objects.filter(brand__name='Astra', category__name='โน้ตบุ๊ก', price__lt=55000)
<QuerySet [<Product: Laptop Q4376-017 - 52,800 บาท>]>
```

แปลว่า: หาโน้ตบุ๊กแบรนด์ Astra ที่ราคาต่ำกว่า 55,000 → เจอ 1 รายการ

## 3.3 `.exclude()` — เอาทุกอย่าง "ยกเว้น" ที่ตรงเงื่อนไข

```python
>>> Product.objects.exclude(brand__name='Astra').count()
82
```

(ทั้งหมด 100 − Astra 18 = 82)

## 3.4 filter ต่อกันเป็นลูกโซ่ (Chaining)

QuerySet สามารถ filter ซ้อนต่อกันได้เรื่อย ๆ:

```python
>>> qs = Product.objects.filter(category__name='โน้ตบุ๊ก')
>>> qs = qs.filter(price__lt=55000)
>>> qs = qs.exclude(brand__name='Astra')
>>> qs.count()
3
```

> 📌 Django ยังไม่ยิง SQL จนกว่าเราจะ "ใช้ผลลัพธ์จริง" (เช่น print, count, วนลูป)
> คุณสมบัตินี้เรียกว่า **Lazy Evaluation** — ต่อโซ่กี่ชั้นก็ยิง SQL แค่ครั้งเดียว

## 3.5 `.exists()` — เช็คว่า "มีไหม" (เร็วกว่า count)

```python
>>> Product.objects.filter(price__lt=300).exists()
False
>>> Product.objects.filter(brand__name='Quantum').exists()
True
```

---

# บทที่ 4 — Field Lookups: เครื่องมือกรองขั้นเทพ

รูปแบบคือ `ชื่อฟิลด์__lookup=ค่า` (underscore 2 ตัว)

## 4.1 ตารางสรุป Lookups ที่ใช้บ่อย

| Lookup           | ความหมาย                                          | เทียบ SQL    |
| ---------------- | --------------------------------------------------------- | ----------------- |
| `exact`        | เท่ากับเป๊ะ (default)                          | `=`             |
| `iexact`       | เท่ากับ ไม่สนตัวพิมพ์เล็กใหญ่ | `ILIKE`         |
| `contains`     | มีคำนี้อยู่ข้างใน                        | `LIKE '%...%'`  |
| `icontains`    | มีคำนี้ ไม่สนตัวพิมพ์                 | `ILIKE '%...%'` |
| `startswith`   | ขึ้นต้นด้วย                                    | `LIKE '...%'`   |
| `endswith`     | ลงท้ายด้วย                                      | `LIKE '%...'`   |
| `gt` / `gte` | มากกว่า / มากกว่าหรือเท่ากับ     | `>` / `>=`    |
| `lt` / `lte` | น้อยกว่า / น้อยกว่าหรือเท่ากับ | `<` / `<=`    |
| `in`           | อยู่ในลิสต์                                    | `IN (...)`      |
| `range`        | อยู่ระหว่าง (รวมหัวท้าย)             | `BETWEEN`       |
| `isnull`       | เป็นค่าว่าง NULL                               | `IS NULL`       |

## 4.2 เปรียบเทียบตัวเลข — gt, gte, lt, lte

สินค้าราคาต่ำกว่า 2,000 บาท:

```python
>>> Product.objects.filter(price__lt=2000)
<QuerySet [<Product: PC Case N3855-014 - 1,600 บาท>, <Product: Mouse P5380-042 - 400 บาท>,
 <Product: PC Case P2244-094 - 1,300 บาท>, <Product: Mouse V2999-074 - 1,000 บาท>,
 <Product: Webcam Q9845-095 - 1,600 บาท>, <Product: PC Case T7995-046 - 1,700 บาท>,
 <Product: Router X3500-076 - 1,900 บาท>]>
```

สินค้าราคาเกิน 60,000 บาท:

```python
>>> Product.objects.filter(price__gt=60000).count()
4
```

## 4.3 ช่วงราคา — `range`

สินค้าราคา 10,000 – 15,000 บาท:

```python
>>> Product.objects.filter(price__range=(10000, 15000)).count()
13
```

## 4.4 ค้นหาคำในข้อความ — `contains`

สินค้าที่สเปคมี "RAM 32GB":

```python
>>> Product.objects.filter(description__contains='RAM 32GB').count()
7
```

จอภาพที่รีเฟรชเรต 144Hz:

```python
>>> Product.objects.filter(category__name='จอภาพ', description__contains='144Hz')
<QuerySet [<Product: Monitor T5854-072 - 17,800 บาท>, <Product: Monitor X6168-024 - 25,800 บาท>]>
```

## 4.5 ขึ้นต้น / ลงท้าย — `startswith` / `endswith`

```python
>>> Product.objects.filter(name__startswith='Laptop').count()
7

>>> Product.objects.filter(name__endswith='-001')
<QuerySet [<Product: Laptop A3909-001 - 55,500 บาท>]>
```

## 4.6 อยู่ในลิสต์ — `in`

สินค้าของแบรนด์ Quantum หรือ Orionix:

```python
>>> Product.objects.filter(brand__name__in=['Quantum', 'Orionix']).count()
12
```

> 📌 สังเกต `brand__name__in` — ข้าม FK ไปที่ `brand` → เข้าฟิลด์ `name` → ใช้ lookup `in`
> underscore คู่ (`__`) ใช้ทั้ง "ข้ามตาราง" และ "เรียก lookup" ในตัวเดียวกัน

---

# บทที่ 5 — การเรียงลำดับและตัดข้อมูล

## 5.1 เรียงลำดับ — `.order_by()`

เรียงราคาถูก → แพง:

```python
>>> Product.objects.order_by('price').first()
<Product: Mouse P5380-042 - 400 บาท>
```

เรียงแพง → ถูก (ใส่ `-` นำหน้า):

```python
>>> Product.objects.order_by('-price').first()
<Product: Desktop D7663-082 - 76,200 บาท>
```

เรียงหลายชั้น — หมวดหมู่ก่อน แล้วราคาแพงสุดก่อนในแต่ละหมวด:

```python
>>> Product.objects.order_by('category__name', '-price')
```

## 5.2 ตัดเอาบางส่วน — Slicing (เหมือน LIMIT ใน SQL)

Top 5 สินค้าแพงที่สุดในร้าน:

```python
>>> for p in Product.objects.order_by('-price')[:5]:
...     print(f'{p.name:30} {p.price:>10,.0f} บาท')
...
Desktop D7663-082                  76,200 บาท
Laptop W5685-049                   65,700 บาท
Graphics Card J9276-036            61,200 บาท
Laptop M2295-065                   60,100 บาท
Graphics Card T3027-020            57,800 บาท
```

5 สินค้าถูกที่สุด:

```python
>>> for p in Product.objects.order_by('price')[:5]:
...     print(f'{p.name:30} {p.price:>10,.0f} บาท')
...
Mouse P5380-042                       400 บาท
Mouse V2999-074                     1,000 บาท
PC Case P2244-094                   1,300 บาท
PC Case N3855-014                   1,600 บาท
Webcam Q9845-095                    1,600 บาท
```

อันดับ 6–10 (ข้าม 5 ตัวแรก):

```python
>>> Product.objects.order_by('-price')[5:10]
```

> ⚠️ QuerySet ใช้ index ติดลบไม่ได้ (`[-1]` จะ error) — ถ้าต้องการตัวสุดท้ายให้ใช้ `.last()` หรือเรียงกลับด้านแล้ว `.first()`

---

# บทที่ 6 — เลือกเฉพาะคอลัมน์ที่ต้องการ

## 6.1 `.values()` — ได้ dictionary

```python
>>> Product.objects.filter(price__gt=60000).values('name', 'brand__name', 'price')
<QuerySet [
 {'name': 'Laptop W5685-049', 'brand__name': 'VoltEdge', 'price': Decimal('65700.00')},
 {'name': 'Laptop M2295-065', 'brand__name': 'PixelForge', 'price': Decimal('60100.00')},
 {'name': 'Desktop D7663-082', 'brand__name': 'NovaTech', 'price': Decimal('76200.00')},
 {'name': 'Graphics Card J9276-036', 'brand__name': 'CoreLink', 'price': Decimal('61200.00')}
]>
```

## 6.2 `.values_list()` — ได้ tuple

```python
>>> Product.objects.filter(category__name='โน้ตบุ๊ก').values_list('name', 'price')
<QuerySet [('Laptop C6684-081', Decimal('50300.00')), ('Laptop W5685-049', Decimal('65700.00')), ...]>
```

ถ้าเอาคอลัมน์เดียว ใส่ `flat=True` จะได้ลิสต์ค่าตรง ๆ:

```python
>>> Brand.objects.values_list('name', flat=True)
<QuerySet ['Astra', 'ZenCore', 'VoltEdge', 'Nexora', 'Orionix', 'PixelForge', 'CoreLink',
 'ByteCraft', 'NovaTech', 'Quantum']>
```

## 6.3 `.distinct()` — ตัดค่าซ้ำ

แบรนด์ Astra ขายสินค้ากี่หมวดหมู่ อะไรบ้าง:

```python
>>> Product.objects.filter(brand__name='Astra').values_list('category__name', flat=True).distinct()
<QuerySet ['พาวเวอร์ซัพพลาย', 'เคสคอมพิวเตอร์', 'เว็บแคม', 'เครื่องสำรองไฟ', 'เมนบอร์ด',
 'โน้ตบุ๊ก', 'ซีพียู', 'เมาส์', 'คอมพิวเตอร์ตั้งโต๊ะ', 'การ์ดจอ', 'ชุดหูฟัง', 'คีย์บอร์ด']>
```

→ Astra ขายครอบคลุมถึง 12 หมวดหมู่

---

# บทที่ 7 — Query ข้ามตาราง (ForeignKey)

## 7.1 เดินหน้า: จาก Product → Brand/Category

ใช้ `__` (underscore สองตัว) เจาะเข้าไปในตารางที่เชื่อมกัน:

```python
>>> Product.objects.filter(brand__name='Astra').count()
18

>>> Product.objects.filter(category__name='อุปกรณ์จัดเก็บข้อมูล',
...                        description__contains='NVMe').count()
4
```

หรือดึง object มาก่อนแล้วเข้าถึง attribute:

```python
>>> p = Product.objects.first()
>>> p.brand          # ได้ Brand object
<Brand: Astra>
>>> p.brand.name
'Astra'
>>> p.category.name
'พาวเวอร์ซัพพลาย'
```

## 7.2 ย้อนกลับ: จาก Brand → Products (ใช้ related_name)

ใน model เรากำหนด `related_name='products'` ไว้ ทำให้เรียกย้อนกลับได้:

```python
>>> b = Brand.objects.get(name='Quantum')
>>> b.products.all()
<QuerySet [<Product: UPS V4826-048 - 11,600 บาท>, <Product: UPS F9435-032 - 4,700 บาท>,
 <Product: Headset Q2291-043 - 2,700 บาท>, <Product: Power Supply O5114-093 - 7,800 บาท>,
 <Product: Mouse L9644-090 - 5,400 บาท>, <Product: Processor O4097-067 - 18,500 บาท>]>

>>> b.products.count()
6

>>> b.products.filter(price__gt=10000)
<QuerySet [<Product: UPS V4826-048 - 11,600 บาท>, <Product: Processor O4097-067 - 18,500 บาท>]>
```

เช่นเดียวกับ Category:

```python
>>> c = Category.objects.get(name='โน้ตบุ๊ก')
>>> c.products.count()
7
```

> 📌 `b.products` เป็น Manager เหมือน `Product.objects` — ใช้ `.filter()`, `.count()`, `.order_by()` ต่อได้หมด แต่ขอบเขตจำกัดอยู่แค่สินค้าของแบรนด์นั้น

---

# บทที่ 8 — Q Objects: เงื่อนไข OR / NOT

`filter(a, b)` ปกติคือ AND — ถ้าอยากได้ **OR** ต้องใช้ `Q`

```python
from django.db.models import Q
```

## 8.1 OR — ใช้ `|`

สินค้าที่เป็น "เมาส์ หรือ คีย์บอร์ด":

```python
>>> Product.objects.filter(Q(category__name='เมาส์') | Q(category__name='คีย์บอร์ด')).count()
12
```

## 8.2 AND — ใช้ `&` (เหมือน filter ปกติ)

```python
>>> Product.objects.filter(Q(brand__name='Astra') & Q(price__gt=20000)).count()
4
```

## 8.3 NOT — ใช้ `~`

สินค้าที่ "ไม่ใช่" ของ Astra (ผลเหมือน exclude):

```python
>>> Product.objects.filter(~Q(brand__name='Astra')).count()
82
```

## 8.4 ผสมกันซับซ้อน

โน้ตบุ๊กหรือคอมตั้งโต๊ะ ที่ราคาไม่เกิน 50,000:

```python
>>> Product.objects.filter(
...     Q(category__name='โน้ตบุ๊ก') | Q(category__name='คอมพิวเตอร์ตั้งโต๊ะ'),
...     price__lte=50000
... ).count()
6
```

> 📌 ผสม Q กับเงื่อนไขปกติได้ แต่ **Q ต้องมาก่อน** keyword argument เสมอ

---

# บทที่ 9 — Aggregate: สรุปยอดทั้งตาราง

`aggregate()` คืนค่าเป็น dictionary — สรุปยอดจากทั้ง QuerySet เหลือค่าเดียว

```python
from django.db.models import Avg, Max, Min, Sum, Count
```

## 9.1 สถิติราคาสินค้าทั้งร้าน

```python
>>> Product.objects.aggregate(Avg('price'), Max('price'), Min('price'), Sum('price'))
{'price__avg': Decimal('15436'),
 'price__max': Decimal('76200'),
 'price__min': Decimal('400'),
 'price__sum': Decimal('1543600')}
```

อ่านผล: ราคาเฉลี่ย 15,436 / แพงสุด 76,200 / ถูกสุด 400 / มูลค่าสต๊อกรวม 1,543,600 บาท

## 9.2 ตั้งชื่อ key เอง

```python
>>> Product.objects.aggregate(ราคาเฉลี่ย=Avg('price'), แพงสุด=Max('price'))
{'ราคาเฉลี่ย': Decimal('15436'), 'แพงสุด': Decimal('76200')}
```

## 9.3 aggregate เฉพาะกลุ่มที่ filter แล้ว

ราคาเฉลี่ยเฉพาะโน้ตบุ๊ก:

```python
>>> Product.objects.filter(category__name='โน้ตบุ๊ก').aggregate(Avg('price'))
{'price__avg': Decimal('49757.1428571429')}
```

→ โน้ตบุ๊กเฉลี่ยเครื่องละ ~49,757 บาท (สูงกว่าค่าเฉลี่ยทั้งร้านกว่า 3 เท่า)

---

# บทที่ 10 — Annotate: Group By ฉบับ Django

`annotate()` คำนวณค่า "แปะเพิ่ม" ให้แต่ละแถว — ใช้ทำรายงานแบบ GROUP BY

## 10.1 นับจำนวนสินค้าของแต่ละแบรนด์

```python
>>> for b in Brand.objects.annotate(total=Count('products')).order_by('-total'):
...     print(f'{b.name:12} {b.total} รายการ')
...
Astra        18 รายการ
ByteCraft    12 รายการ
Nexora       11 รายการ
CoreLink     11 รายการ
ZenCore      10 รายการ
NovaTech     10 รายการ
PixelForge    9 รายการ
VoltEdge      7 รายการ
Orionix       6 รายการ
Quantum       6 รายการ
```

> 📌 `Count('products')` นับผ่าน related_name — ค่า `total` กลายเป็น attribute ใหม่ของแต่ละ Brand ชั่วคราว

## 10.2 ราคาเฉลี่ยของแต่ละหมวดหมู่ (Top 5)

```python
>>> for c in Category.objects.annotate(avg_price=Avg('products__price')).order_by('-avg_price')[:5]:
...     print(f'{c.name:22} {c.avg_price:>12,.0f} บาท')
...
โน้ตบุ๊ก                     49,757 บาท
คอมพิวเตอร์ตั้งโต๊ะ           45,457 บาท
การ์ดจอ                     36,186 บาท
จอภาพ                       16,817 บาท
ซีพียู                       14,800 บาท
```

## 10.3 มูลค่าสินค้ารวมของแต่ละแบรนด์ (Top 3)

```python
>>> for b in Brand.objects.annotate(total_value=Sum('products__price')).order_by('-total_value')[:3]:
...     print(f'{b.name:12} {b.total_value:>12,.0f} บาท')
...
CoreLink          349,100 บาท
Astra             232,900 บาท
NovaTech          145,300 บาท
```

## 10.4 filter ต่อจาก annotate ได้ (เหมือน HAVING ใน SQL)

แบรนด์ที่มีสินค้ามากกว่า 10 รายการ:

```python
>>> Brand.objects.annotate(total=Count('products')).filter(total__gt=10).values_list('name', 'total')
<QuerySet [('Astra', 18), ('Nexora', 11), ('CoreLink', 11), ('ByteCraft', 12)]>
```

## สรุปความต่าง aggregate vs annotate

|                  | `aggregate()`                    | `annotate()`                            |
| ---------------- | ---------------------------------- | ----------------------------------------- |
| ผลลัพธ์   | dictionary ค่าเดียว        | QuerySet (แปะค่าให้ทุกแถว) |
| ใช้เมื่อ | สรุปยอดรวมทั้งหมด | สรุปยอด "แยกตามกลุ่ม"   |
| เทียบ SQL   | `SELECT AVG(...)`                | `GROUP BY`                              |

---

# บทที่ 11 — เพิ่ม แก้ไข ลบข้อมูล (CRUD)

## 11.1 เพิ่มข้อมูล — `.create()`

```python
>>> b = Brand.objects.get(name='Astra')
>>> c = Category.objects.get(name='เมาส์')
>>> p = Product.objects.create(
...     name='Mouse TEST-999',
...     brand=b,
...     category=c,
...     description='เมาส์ทดสอบสำหรับสอน CRUD',
...     price=999
... )
>>> p.id
101
```

หรือแบบสร้าง object ก่อนแล้วค่อย `.save()`:

```python
>>> p2 = Product(name='Keyboard TEST-998', brand=b,
...              category=Category.objects.get(name='คีย์บอร์ด'),
...              description='ทดสอบ', price=1500)
>>> p2.save()
```

## 11.2 แก้ไขทีละตัว — แก้ attribute แล้ว `.save()`

```python
>>> p = Product.objects.get(name='Mouse TEST-999')
>>> p.price = 899
>>> p.save()
```

## 11.3 แก้ไขทีเดียวหลายแถว — `.update()`

ลดราคาสินค้าทดสอบทุกตัวเหลือ 500:

```python
>>> Product.objects.filter(name__contains='TEST').update(price=500)
2
```

(ตัวเลขที่คืนมา = จำนวนแถวที่ถูกแก้)

## 11.4 ลบข้อมูล — `.delete()`

```python
>>> Product.objects.filter(name__contains='TEST').delete()
(2, {'shop.Product': 2})
```

> ⚠️ **ระวังสุด ๆ:** `Product.objects.all().delete()` = ลบทั้งตาราง!
> ถ้าเผลอลบข้อมูลจริง ให้รัน `python manage.py load_products` โหลดกลับมาใหม่ได้

## 11.5 `.get_or_create()` — มีก็เอาเลย ไม่มีก็สร้างใหม่

```python
>>> brand, created = Brand.objects.get_or_create(name='Astra')
>>> created
False        # มีอยู่แล้ว ไม่ได้สร้างใหม่
```

---

# บทที่ 12 — เทคนิคระดับโปร

## 12.1 แอบดู SQL ที่ Django สร้างให้

```python
>>> qs = Product.objects.filter(price__gt=60000)
>>> print(qs.query)
SELECT "shop_product"."id", "shop_product"."name", ... FROM "shop_product"
WHERE "shop_product"."price" > 60000
```

เหมาะมากเวลาสอนเชื่อม Django ORM ↔ SQL

## 12.2 `select_related()` — แก้ปัญหา N+1 Query

โค้ดนี้ยิง SQL 1 + 100 ครั้ง (ทุกครั้งที่แตะ `p.brand` จะ query เพิ่ม):

```python
for p in Product.objects.all():
    print(p.name, p.brand.name)     # ❌ ช้า — 101 queries
```

แบบนี้ยิง SQL แค่ **1 ครั้ง** (JOIN มาให้เลย):

```python
for p in Product.objects.select_related('brand', 'category'):
    print(p.name, p.brand.name)     # ✅ เร็ว — 1 query
```

พิสูจน์ด้วยตัวเอง:

```python
>>> from django.db import connection, reset_queries
>>> reset_queries()
>>> _ = [p.brand.name for p in Product.objects.all()]
>>> len(connection.queries)
101
>>> reset_queries()
>>> _ = [p.brand.name for p in Product.objects.select_related('brand')]
>>> len(connection.queries)
1
```

## 12.3 F Expression — คำนวณจากค่าในฐานข้อมูลโดยตรง

ขึ้นราคาสินค้าทุกตัวในหมวดเมาส์ 10% โดยไม่ต้องดึงมาเข้า Python เลย:

```python
>>> from django.db.models import F
>>> Product.objects.filter(category__name='เมาส์').update(price=F('price') * 1.10)
6
```

(อย่าลืมรัน `load_products` เพื่อคืนราคาเดิมหลังทดลอง)

## 12.4 annotate ค่าคำนวณรายแถว

แปะราคาหลัง VAT 7% ให้ทุกสินค้า:

```python
>>> qs = Product.objects.annotate(price_vat=F('price') * 1.07)
>>> p = qs.first()
>>> print(p.name, p.price, '→', p.price_vat)
Power Supply S3809-045 6500.00 → 6955.0000
```

---

# บทที่ 13 — โจทย์ฝึกหัด 20 ข้อ พร้อมเฉลย

> วิธีใช้ในห้องเรียน: ให้นักเรียนลองทำเองก่อน แล้วค่อยเปิดเฉลย
> ทุกข้อมี **คำตอบตัวเลขจริง** ให้ตรวจได้ทันที

## 🟢 ระดับง่าย (ข้อ 1–7)

**ข้อ 1.** ในร้านมีสินค้าทั้งหมดกี่รายการ?

<details><summary>เฉลย</summary>

```python
Product.objects.count()
# 100
```

</details>

**ข้อ 2.** มีโน้ตบุ๊กขายกี่รุ่น?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(category__name='โน้ตบุ๊ก').count()
# 7
```

</details>

**ข้อ 3.** สินค้าที่**แพงที่สุด**ในร้านคืออะไร ราคาเท่าไหร่?

<details><summary>เฉลย</summary>

```python
Product.objects.order_by('-price').first()
# <Product: Desktop D7663-082 - 76,200 บาท>
```

</details>

**ข้อ 4.** สินค้าที่**ถูกที่สุด**ในร้านคืออะไร?

<details><summary>เฉลย</summary>

```python
Product.objects.order_by('price').first()
# <Product: Mouse P5380-042 - 400 บาท>  (เมาส์เกมมิ่ง 400 บาท!)
```

</details>

**ข้อ 5.** แบรนด์ Astra มีสินค้ากี่รายการ?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(brand__name='Astra').count()
# 18
```

</details>

**ข้อ 6.** แสดงชื่อแบรนด์ทั้งหมดที่มีในร้าน

<details><summary>เฉลย</summary>

```python
Brand.objects.values_list('name', flat=True)
# ['Astra', 'ZenCore', 'VoltEdge', 'Nexora', 'Orionix',
#  'PixelForge', 'CoreLink', 'ByteCraft', 'NovaTech', 'Quantum']
```

</details>

**ข้อ 7.** สินค้าชื่อ `Laptop C6684-081` เป็นของแบรนด์อะไร ราคาเท่าไหร่?

<details><summary>เฉลย</summary>

```python
p = Product.objects.get(name='Laptop C6684-081')
p.brand.name, p.price
# ('ZenCore', Decimal('50300.00'))
```

</details>

## 🟡 ระดับกลาง (ข้อ 8–14)

**ข้อ 8.** มีสินค้าราคาต่ำกว่า 2,000 บาทกี่รายการ อะไรบ้าง?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(price__lt=2000).count()
# 7 รายการ: PC Case N3855-014 (1,600), Mouse P5380-042 (400), PC Case P2244-094 (1,300),
# Mouse V2999-074 (1,000), Webcam Q9845-095 (1,600), PC Case T7995-046 (1,700),
# Router X3500-076 (1,900)
```

</details>

**ข้อ 9.** สินค้าราคาระหว่าง 10,000 – 15,000 บาท มีกี่รายการ?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(price__range=(10000, 15000)).count()
# 13
```

</details>

**ข้อ 10.** แสดง Top 5 สินค้าราคาแพงที่สุด พร้อมราคา

<details><summary>เฉลย</summary>

```python
Product.objects.order_by('-price').values_list('name', 'price')[:5]
# Desktop D7663-082 (76,200), Laptop W5685-049 (65,700),
# Graphics Card J9276-036 (61,200), Laptop M2295-065 (60,100),
# Graphics Card T3027-020 (57,800)
```

</details>

**ข้อ 11.** โน้ตบุ๊กที่ใช้ซีพียู Intel Core i7 มีรุ่นไหนบ้าง?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(category__name='โน้ตบุ๊ก', description__contains='Core i7')
# Laptop C6684-081 (50,300), Laptop S2279-097 (40,000), Laptop A3909-001 (55,500)
```

</details>

**ข้อ 12.** มีสินค้ากี่รายการที่สเปคระบุ "RAM 32GB"?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(description__contains='RAM 32GB').count()
# 7
```

</details>

**ข้อ 13.** สินค้าของแบรนด์ Quantum หรือ Orionix รวมกันมีกี่รายการ? (ทำ 2 วิธี: `__in` และ `Q`)

<details><summary>เฉลย</summary>

```python
# วิธีที่ 1
Product.objects.filter(brand__name__in=['Quantum', 'Orionix']).count()
# วิธีที่ 2
Product.objects.filter(Q(brand__name='Quantum') | Q(brand__name='Orionix')).count()
# 12 (Quantum 6 + Orionix 6)
```

</details>

**ข้อ 14.** จอภาพที่รีเฟรชเรต 144Hz มีรุ่นไหนบ้าง?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(category__name='จอภาพ', description__contains='144Hz')
# Monitor T5854-072 (17,800), Monitor X6168-024 (25,800)
```

</details>

## 🔴 ระดับยาก (ข้อ 15–20)

**ข้อ 15.** ราคาเฉลี่ย / แพงสุด / ถูกสุด / มูลค่ารวม ของสินค้าทั้งร้าน?

<details><summary>เฉลย</summary>

```python
Product.objects.aggregate(Avg('price'), Max('price'), Min('price'), Sum('price'))
# {'price__avg': 15436, 'price__max': 76200, 'price__min': 400, 'price__sum': 1543600}
```

</details>

**ข้อ 16.** ราคาเฉลี่ยของ "โน้ตบุ๊ก" อย่างเดียวคือเท่าไหร่?

<details><summary>เฉลย</summary>

```python
Product.objects.filter(category__name='โน้ตบุ๊ก').aggregate(Avg('price'))
# {'price__avg': Decimal('49757.14...')} ≈ 49,757 บาท
```

</details>

**ข้อ 17.** แบรนด์ไหนมีสินค้า**เยอะที่สุด** และมีกี่รายการ? (เรียงทุกแบรนด์จากมาก → น้อย)

<details><summary>เฉลย</summary>

```python
Brand.objects.annotate(total=Count('products')).order_by('-total').values_list('name', 'total')
# Astra 18, ByteCraft 12, Nexora 11, CoreLink 11, ZenCore 10,
# NovaTech 10, PixelForge 9, VoltEdge 7, Orionix 6, Quantum 6
```

</details>

**ข้อ 18.** หมวดหมู่ไหนมี**ราคาเฉลี่ยสูงสุด** 3 อันดับแรก?

<details><summary>เฉลย</summary>

```python
Category.objects.annotate(avg=Avg('products__price')).order_by('-avg')[:3].values_list('name', 'avg')
# โน้ตบุ๊ก ~49,757 / คอมพิวเตอร์ตั้งโต๊ะ ~45,457 / การ์ดจอ ~36,186
```

</details>

**ข้อ 19.** แบรนด์ไหนมีมูลค่าสินค้ารวม (Sum ของราคา) สูงสุด?

<details><summary>เฉลย</summary>

```python
Brand.objects.annotate(s=Sum('products__price')).order_by('-s').first()
# CoreLink — มูลค่ารวม 349,100 บาท
# (แม้มีสินค้าแค่ 11 ชิ้น แต่ล้วนเป็นของแพง เช่น การ์ดจอ 61,200!)
```

</details>

**ข้อ 20.** ลูกค้างบ 55,000 บาท อยากได้ "โน้ตบุ๊ก หรือ คอมพิวเตอร์ตั้งโต๊ะ" มีตัวเลือกกี่รายการ? แสดงชื่อ แบรนด์ ราคา เรียงจากถูกไปแพง

<details><summary>เฉลย</summary>

```python
qs = Product.objects.filter(
    Q(category__name='โน้ตบุ๊ก') | Q(category__name='คอมพิวเตอร์ตั้งโต๊ะ'),
    price__lte=55000
).order_by('price')

for p in qs:
    print(f'{p.name:22} {p.brand.name:12} {p.price:>10,.0f} บาท')

# 9 รายการ:
# Desktop R3612-018      Astra            16,500 บาท
# Desktop H6747-034      Astra            21,500 บาท
# Laptop G9831-033       Nexora           23,900 บาท
# Laptop S2279-097       PixelForge       40,000 บาท
# Desktop N8176-066      Astra            46,100 บาท
# Desktop B1714-002      Orionix          49,000 บาท
# Laptop C6684-081       ZenCore          50,300 บาท
# Laptop Q4376-017       Astra            52,800 บาท
# Desktop T4238-098      CoreLink         53,800 บาท
```

</details>

---

# 📎 ภาคผนวก — สรุปคำสั่งทั้งหมดในหน้าเดียว (Cheat Sheet)

```python
from shop.models import Product, Brand, Category
from django.db.models import Avg, Max, Min, Sum, Count, Q, F

# ===== พื้นฐาน =====
Product.objects.all()                          # ทั้งหมด
Product.objects.count()                        # นับจำนวน
Product.objects.first() / .last()              # ตัวแรก / ตัวสุดท้าย
Product.objects.get(id=1)                      # ตัวเดียวเป๊ะ ๆ (ไม่เจอ = error)

# ===== กรอง =====
Product.objects.filter(price__lt=5000)         # WHERE price < 5000
Product.objects.exclude(brand__name='Astra')   # WHERE NOT ...
Product.objects.filter(a=1, b=2)               # AND
Product.objects.filter(Q(a=1) | Q(b=2))        # OR
Product.objects.filter(~Q(a=1))                # NOT
Product.objects.filter(price__range=(1, 9))    # BETWEEN
Product.objects.filter(name__in=[...])         # IN
Product.objects.filter(name__contains='SSD')   # LIKE '%SSD%'
Product.objects.filter(name__startswith='A')   # LIKE 'A%'
Product.objects.filter(x__isnull=True)         # IS NULL
Product.objects.filter(...).exists()           # เช็คว่ามีไหม (True/False)

# ===== ข้ามตาราง =====
Product.objects.filter(brand__name='Astra')    # Product → Brand
brand.products.all()                           # Brand → Products (related_name)

# ===== เรียง + ตัด =====
Product.objects.order_by('price')              # ASC
Product.objects.order_by('-price')             # DESC
Product.objects.order_by('-price')[:5]         # LIMIT 5

# ===== เลือกคอลัมน์ =====
Product.objects.values('name', 'price')        # ได้ dict
Product.objects.values_list('name', flat=True) # ได้ list
qs.distinct()                                  # ตัดซ้ำ

# ===== สรุปยอด =====
Product.objects.aggregate(Avg('price'))                        # ทั้งตาราง
Brand.objects.annotate(n=Count('products'))                    # GROUP BY
Category.objects.annotate(avg=Avg('products__price'))          # GROUP BY + AVG
Brand.objects.annotate(n=Count('products')).filter(n__gt=10)   # HAVING

# ===== CRUD =====
Product.objects.create(name=..., brand=..., category=..., price=...)
p.price = 899; p.save()                        # แก้ทีละตัว
qs.update(price=500)                           # แก้หลายแถว
qs.update(price=F('price') * 1.1)              # แก้โดยคำนวณจากค่าเดิม
qs.delete()                                    # ลบ
Brand.objects.get_or_create(name='Astra')      # มีก็เอา ไม่มีก็สร้าง

# ===== ระดับโปร =====
print(qs.query)                                # ดู SQL จริง
Product.objects.select_related('brand')        # JOIN แก้ N+1
```

> 🔄 **ข้อมูลเละเมื่อไหร่ รันคำสั่งนี้เพื่อรีเซ็ตกลับ 100 รายการเดิมได้เสมอ:**
>
> ```bash
> python manage.py load_products
> ```

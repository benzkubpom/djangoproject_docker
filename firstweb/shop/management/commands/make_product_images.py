"""สร้างภาพประกอบสินค้าด้วย Pillow เก็บลง shop/static/shop/img/products/

    python manage.py make_product_images          # ข้ามไฟล์ที่มีอยู่แล้ว
    python manage.py make_product_images --force  # วาดใหม่ทับของเดิม

ได้ไฟล์ <หมวด>-<สี>.png ครบทุกคู่ที่หน้าเว็บเรียกใช้ (ดู Product.photo_static)
ไฟล์อยู่ใน static ของแอป จึง commit ขึ้น git ได้และทำงานใน Docker ได้เลย
โดยไม่ต้องต่ออินเทอร์เน็ต ส่วนสินค้าที่อัปโหลดรูปถ่ายจริงไว้ใน admin
หน้าเว็บจะใช้รูปถ่ายนั้นก่อนภาพจากไฟล์ชุดนี้
"""
import math
from pathlib import Path

from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFilter

from shop.models import CATEGORY_ICONS, PHOTO_VARIANTS

# ขนาดไฟล์ที่บันทึก อัตราส่วน 4:3 ตรงกับกรอบรูปในหน้าเว็บ
OUT_W, OUT_H = 900, 675
# วาดใหญ่กว่าจริง SS เท่าแล้วย่อลง เพราะ ImageDraw ไม่มี anti-alias ให้
SS = 3
# ระบบพิกัดที่ใช้เขียนโค้ดวาด (Pen คูณสเกลให้เอง)
W, H = 1200, 900

RED = (215, 38, 61)          # ตรงกับ red DEFAULT ในธีม Tailwind
GOLD = (198, 163, 92)        # ขาทองแดงของ RAM / การ์ดจอ
BG_TOP = (255, 255, 255)     # paper
BG_BOTTOM = (231, 231, 230)  # เข้มกว่า bone เล็กน้อยให้เห็นมิติ

# โทนสีตัวสินค้า 3 แบบ: ดำ / เงิน / ขาว
VARIANTS = {
    'dark': {
        'top': (60, 64, 72), 'body': (38, 41, 47), 'edge': (21, 23, 27),
        'part': (78, 83, 92), 'screen': (13, 15, 18), 'metal': (150, 156, 165),
    },
    'silver': {
        'top': (222, 225, 229), 'body': (196, 200, 207), 'edge': (139, 145, 154),
        'part': (176, 181, 189), 'screen': (18, 20, 24), 'metal': (232, 234, 237),
    },
    'white': {
        'top': (255, 255, 255), 'body': (238, 239, 240), 'edge': (188, 191, 195),
        'part': (222, 224, 227), 'screen': (16, 18, 22), 'metal': (208, 211, 215),
    },
}


def blend(c1, c2, t):
    """ผสมสองสีเชิงเส้น t=0 ได้ c1, t=1 ได้ c2"""
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def _linear(w, h, c1, c2, horizontal=False):
    """ไล่เฉดสีเชิงเส้น: วาดแถบ 1 พิกเซลแล้วยืดออก เร็วกว่าไล่ทีละพิกเซล"""
    n = max(2, w if horizontal else h)
    strip = Image.new('RGB', (n, 1) if horizontal else (1, n))
    px = strip.load()
    for i in range(n):
        col = blend(c1, c2, i / (n - 1))
        if horizontal:
            px[i, 0] = col
        else:
            px[0, i] = col
    return strip.resize((max(1, w), max(1, h)), Image.BILINEAR)


class Pen:
    """วาดด้วยพิกัดระบบ 1200x900 แล้วคูณสเกลขึ้นให้เองตอนลงภาพจริง"""

    def __init__(self, img, scale):
        self.img = img
        self.d = ImageDraw.Draw(img)
        self.s = scale

    def _s(self, v):
        return v * self.s

    def _box(self, x, y, w, h):
        return [self._s(x), self._s(y), self._s(x + w), self._s(y + h)]

    def _pts(self, pts):
        return [(self._s(x), self._s(y)) for x, y in pts]

    def rect(self, x, y, w, h, fill=None, outline=None, width=2, r=0):
        box = self._box(x, y, w, h)
        if r:
            self.d.rounded_rectangle(
                box, radius=self._s(r), fill=fill, outline=outline,
                width=round(self._s(width)),
            )
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=round(self._s(width)))

    def grad(self, x, y, w, h, c1, c2, r=0, horizontal=False):
        """สี่เหลี่ยม (มุมโค้งได้) ที่ไล่เฉดสีข้างใน"""
        pw, ph = round(self._s(w)), round(self._s(h))
        patch = _linear(pw, ph, c1, c2, horizontal)
        mask = Image.new('L', (pw, ph), 0)
        md = ImageDraw.Draw(mask)
        if r:
            md.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=self._s(r), fill=255)
        else:
            md.rectangle([0, 0, pw - 1, ph - 1], fill=255)
        self.img.paste(patch, (round(self._s(x)), round(self._s(y))), mask)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=2):
        self.d.ellipse(
            self._box(cx - rx, cy - ry, rx * 2, ry * 2),
            fill=fill, outline=outline, width=round(self._s(width)),
        )

    def circle(self, cx, cy, r, fill=None, outline=None, width=2):
        self.ellipse(cx, cy, r, r, fill=fill, outline=outline, width=width)

    def line(self, pts, fill, width=2):
        self.d.line(self._pts(pts), fill=fill, width=round(self._s(width)), joint='curve')

    def poly(self, pts, fill=None, outline=None, width=2):
        self.d.polygon(self._pts(pts), fill=fill, outline=outline, width=round(self._s(width)))

    def arc(self, cx, cy, rx, ry, start, end, fill, width=2):
        self.d.arc(
            self._box(cx - rx, cy - ry, rx * 2, ry * 2),
            start, end, fill=fill, width=round(self._s(width)),
        )


# ─────────────────────────── ชิ้นส่วนที่ใช้ซ้ำ ───────────────────────────

def fan(p, v, cx, cy, r, blades=7):
    """พัดลม 1 ตัว ใช้กับพาวเวอร์ซัพพลายและการ์ดจอ"""
    hub = r * 0.3
    p.circle(cx, cy, r, fill=v['edge'])
    p.circle(cx, cy, r - r * 0.06, fill=blend(v['body'], v['edge'], 0.55))
    for i in range(blades):
        a = math.radians(i * 360 / blades)
        a2 = a + math.radians(30)
        p.poly([
            (cx + math.cos(a) * hub, cy + math.sin(a) * hub),
            (cx + math.cos(a2) * hub, cy + math.sin(a2) * hub),
            (cx + math.cos(a2 + 0.38) * (r - r * 0.1), cy + math.sin(a2 + 0.38) * (r - r * 0.1)),
            (cx + math.cos(a + 0.38) * (r - r * 0.1), cy + math.sin(a + 0.38) * (r - r * 0.1)),
        ], fill=v['part'])
    p.circle(cx, cy, hub, fill=blend(v['part'], v['top'], 0.5))


def gold_pins(p, x, y, w, h, notch_at=None):
    """แถบขาทองแดงพร้อมร่องบาก ใช้กับ RAM และการ์ดจอ"""
    p.rect(x, y, w, h, fill=GOLD)
    step = 9
    for i in range(int(w // step)):
        p.rect(x + i * step + 3, y, 3, h, fill=blend(GOLD, (90, 70, 30), 0.45))
    if notch_at is not None:
        p.rect(notch_at, y - 2, 26, h + 4, fill=blend(BG_TOP, BG_BOTTOM, 0.6))


def screw_holes(p, v, boxes, r=13):
    for cx, cy in boxes:
        p.circle(cx, cy, r, fill=v['edge'])
        p.circle(cx, cy, r - 5, fill=blend(v['edge'], (0, 0, 0), 0.45))


# ─────────────────────────── ภาพแต่ละหมวดหมู่ ───────────────────────────

def draw_psu(p, v):
    p.grad(330, 270, 540, 350, v['top'], v['body'], r=16)
    p.rect(330, 270, 540, 350, outline=v['edge'], width=3, r=16)
    fan(p, v, 540, 445, 145)
    # สติกเกอร์สเปกด้านขวา แถบแดงคือจุดเน้นสีเดียวของภาพ
    p.rect(715, 320, 130, 150, fill=v['part'], r=8)
    p.rect(715, 320, 130, 22, fill=RED, r=8)
    for i in range(4):
        p.line([(732, 372 + i * 22), (828, 372 + i * 22)], blend(v['part'], v['edge'], 0.5), 5)
    # ช่องเสียบไฟและสายที่ถอดได้
    p.rect(715, 500, 100, 66, fill=v['edge'], r=6)
    p.rect(731, 516, 22, 34, fill=blend(v['metal'], v['edge'], 0.3), r=3)
    p.rect(777, 516, 22, 34, fill=blend(v['metal'], v['edge'], 0.3), r=3)
    for i, y in enumerate((340, 400, 460, 520)):
        p.line([(330, y), (240, y + 18), (150, y - 12), (60, y + 24)], v['edge'], 13)
        p.line([(330, y), (240, y + 18), (150, y - 12), (60, y + 24)], v['part'], 7)


def draw_laptop(p, v):
    # จอเอียงเล็กน้อยแบบมองจากด้านหน้าเยื้องล่าง
    p.poly([(404, 176), (836, 176), (880, 508), (360, 508)], fill=v['top'])
    p.poly([(404, 176), (836, 176), (880, 508), (360, 508)], outline=v['edge'], width=3)
    p.poly([(430, 200), (810, 200), (848, 482), (392, 482)], fill=v['screen'])
    p.poly([(430, 200), (596, 200), (470, 482), (392, 482)],
           fill=blend(v['screen'], (255, 255, 255), 0.07))
    p.line([(470, 440), (566, 440)], RED, 7)
    p.line([(470, 462), (620, 462)], blend(v['screen'], (255, 255, 255), 0.22), 5)
    # ฐานและแป้นพิมพ์
    p.poly([(360, 508), (880, 508), (966, 596), (274, 596)], fill=v['body'])
    p.poly([(360, 508), (880, 508), (966, 596), (274, 596)], outline=v['edge'], width=3)
    for i in range(4):
        y = 524 + i * 17
        p.line([(390 + i * 6, y), (852 + i * 10, y)], blend(v['body'], v['edge'], 0.55), 6)
    p.poly([(274, 596), (966, 596), (958, 614), (282, 614)], fill=v['edge'])


def draw_case(p, v):
    p.grad(420, 150, 300, 580, v['top'], v['body'], r=12)
    p.rect(420, 150, 300, 580, outline=v['edge'], width=3, r=12)
    # กระจกข้างมองเห็นอุปกรณ์ข้างใน
    p.rect(446, 186, 210, 470, fill=blend(v['screen'], v['body'], 0.25), r=6)
    p.rect(468, 226, 166, 54, fill=v['part'], r=4)
    p.rect(468, 306, 166, 26, fill=blend(v['part'], v['edge'], 0.4), r=4)
    p.rect(468, 352, 166, 26, fill=blend(v['part'], v['edge'], 0.4), r=4)
    p.rect(468, 430, 120, 120, fill=v['part'], r=6)
    p.circle(528, 490, 34, fill=v['edge'])
    p.rect(468, 578, 166, 52, fill=blend(v['part'], v['edge'], 0.55), r=4)
    # แถบหน้าเคส: ปุ่มเปิดและไฟสถานะสีแดง
    p.rect(676, 150, 44, 580, fill=v['edge'], r=12)
    p.circle(698, 196, 13, fill=v['part'])
    p.circle(698, 240, 8, fill=RED)
    for i in range(9):
        p.line([(686, 300 + i * 22), (710, 300 + i * 22)], blend(v['edge'], v['part'], 0.5), 4)
    p.rect(440, 730, 60, 22, fill=v['edge'], r=6)
    p.rect(640, 730, 60, 22, fill=v['edge'], r=6)


def draw_mainboard(p, v):
    p.grad(270, 190, 660, 520, blend(v['body'], v['edge'], 0.4), v['edge'], r=8)
    p.rect(270, 190, 660, 520, outline=blend(v['edge'], (0, 0, 0), 0.3), width=3, r=8)
    screw_holes(p, v, [(304, 224), (896, 224), (304, 676), (896, 676)], r=12)
    # ลายวงจร
    for i in range(7):
        y = 250 + i * 62
        p.line([(340, y), (520, y), (560, y + 26), (880, y + 26)],
               blend(v['edge'], v['metal'], 0.28), 3)
    # ซ็อกเก็ตซีพียู
    p.rect(348, 250, 190, 190, fill=v['part'], r=6)
    p.grad(370, 272, 146, 146, v['metal'], blend(v['metal'], v['edge'], 0.5), r=4)
    # สล็อตแรม 4 ช่อง ตัวล็อกช่องแรกเป็นสีแดง
    for i in range(4):
        x = 612 + i * 46
        p.rect(x, 246, 26, 260, fill=v['part'], r=5)
        p.rect(x + 5, 262, 16, 228, fill=blend(v['edge'], (0, 0, 0), 0.25), r=3)
        p.rect(x, 246, 26, 18, fill=RED if i == 0 else blend(v['part'], v['top'], 0.3), r=5)
    # สล็อต PCIe และฮีตซิงก์ชิปเซ็ต
    p.rect(330, 556, 430, 30, fill=v['part'], r=6)
    p.rect(346, 564, 398, 14, fill=blend(v['edge'], (0, 0, 0), 0.25), r=3)
    p.rect(792, 528, 116, 116, fill=v['part'], r=8)
    for i in range(5):
        p.line([(806, 546 + i * 20), (894, 546 + i * 20)], blend(v['part'], v['edge'], 0.6), 6)
    p.rect(330, 620, 120, 60, fill=blend(v['part'], v['edge'], 0.4), r=6)


def draw_keyboard(p, v):
    p.grad(140, 330, 920, 260, v['top'], v['body'], r=16)
    p.rect(140, 330, 920, 260, outline=v['edge'], width=3, r=16)
    cap = blend(v['part'], v['top'], 0.35)
    # ขอบปุ่มจำเป็นกับรุ่นสีขาว ไม่มีขอบแล้วปุ่มจะจมไปกับตัวเครื่อง
    edge = blend(v['edge'], v['body'], 0.3)
    for row in range(4):
        y = 356 + row * 46
        for col in range(16):
            x = 168 + col * 54
            fill = RED if (row == 0 and col == 0) else cap
            p.rect(x, y, 46, 38, fill=fill, outline=edge, width=2, r=6)
            p.rect(x + 4, y + 3, 38, 26, fill=blend(fill, v['top'], 0.35), r=4)
    # แถวล่าง: ปุ่มเว้นวรรคยาว
    for x, w in ((168, 120), (300, 460), (772, 250)):
        p.rect(x, 540, w, 38, fill=cap, outline=edge, width=2, r=6)
        p.rect(x + 4, 543, w - 8, 26, fill=blend(cap, v['top'], 0.35), r=4)
    p.line([(140, 592), (1060, 592)], v['edge'], 6)


def draw_gpu(p, v):
    p.grad(170, 310, 790, 250, v['top'], v['body'], r=10)
    p.rect(170, 310, 790, 250, outline=v['edge'], width=3, r=10)
    p.rect(170, 310, 790, 16, fill=RED, r=8)
    fan(p, v, 390, 442, 112)
    fan(p, v, 690, 442, 112)
    # โครงยึดท้ายการ์ดและขาเสียบ PCIe
    p.rect(930, 288, 44, 300, fill=v['metal'], r=4)
    for i in range(3):
        p.rect(940, 314 + i * 78, 24, 54, fill=v['edge'], r=3)
    gold_pins(p, 250, 560, 330, 34, notch_at=376)
    p.rect(700, 560, 200, 22, fill=v['edge'], r=4)


def draw_ups(p, v):
    p.grad(390, 210, 420, 510, v['top'], v['body'], r=14)
    p.rect(390, 210, 420, 510, outline=v['edge'], width=3, r=14)
    # หน้าจอสถานะพร้อมสัญลักษณ์สายฟ้า
    p.rect(424, 250, 352, 150, fill=v['screen'], r=8)
    p.poly([(596, 274), (546, 336), (588, 336), (566, 384), (630, 316), (588, 316)], fill=RED)
    for i in range(3):
        p.line([(452, 288 + i * 26), (524, 288 + i * 26)],
               blend(v['screen'], (255, 255, 255), 0.3), 6)
    p.line([(660, 288), (748, 288)], blend(v['screen'], (255, 255, 255), 0.3), 6)
    p.line([(660, 314), (720, 314)], blend(v['screen'], (255, 255, 255), 0.3), 6)
    # ปุ่มและเต้ารับไฟด้านล่าง
    p.circle(452, 442, 22, fill=v['part'])
    p.circle(516, 442, 22, fill=blend(v['part'], v['edge'], 0.4))
    for row in range(2):
        for col in range(2):
            x, y = 440 + col * 176, 500 + row * 104
            p.rect(x, y, 152, 84, fill=v['edge'], r=8)
            p.rect(x + 40, y + 20, 18, 30, fill=blend(v['metal'], v['edge'], 0.25), r=3)
            p.rect(x + 94, y + 20, 18, 30, fill=blend(v['metal'], v['edge'], 0.25), r=3)
            p.rect(x + 60, y + 56, 32, 12, fill=blend(v['metal'], v['edge'], 0.25), r=3)


def draw_webcam(p, v):
    p.grad(440, 286, 320, 214, v['top'], v['body'], r=100)
    p.rect(440, 286, 320, 214, outline=v['edge'], width=3, r=100)
    p.circle(600, 393, 86, fill=v['edge'])
    p.circle(600, 393, 68, fill=(16, 18, 24))
    p.circle(600, 393, 40, fill=(38, 44, 58))
    p.circle(600, 393, 20, fill=(12, 14, 18))
    p.circle(578, 371, 12, fill=(150, 170, 200))
    p.circle(712, 330, 13, fill=RED)
    # ขาหนีบและก้านตั้ง
    p.poly([(506, 500), (694, 500), (722, 566), (478, 566)], fill=v['body'])
    p.poly([(506, 500), (694, 500), (722, 566), (478, 566)], outline=v['edge'], width=3)
    p.rect(570, 566, 60, 108, fill=v['part'], r=6)
    p.rect(470, 674, 260, 26, fill=v['edge'], r=13)


def draw_storage(p, v):
    p.grad(320, 280, 560, 340, v['top'], v['body'], r=12)
    p.rect(320, 280, 560, 340, outline=v['edge'], width=3, r=12)
    # ฉลากพร้อมแถบแดงด้านบน
    p.rect(360, 320, 320, 176, fill=v['part'], r=8)
    p.rect(360, 320, 320, 22, fill=RED, r=8)
    for i in range(4):
        p.line([(382, 376 + i * 30), (658 - i * 46, 376 + i * 30)],
               blend(v['part'], v['edge'], 0.55), 6)
    screw_holes(p, v, [(356, 306), (844, 306), (356, 594), (844, 594)], r=12)
    # ขั้วต่อสัญญาณและไฟเลี้ยง
    p.rect(700, 518, 160, 56, fill=v['edge'], r=5)
    p.rect(714, 530, 60, 32, fill=blend(v['metal'], v['edge'], 0.2), r=3)
    p.rect(788, 530, 58, 32, fill=blend(v['metal'], v['edge'], 0.2), r=3)
    p.rect(700, 320, 160, 170, fill=blend(v['body'], v['edge'], 0.35), r=8)
    for i in range(6):
        p.line([(716, 344 + i * 26), (844, 344 + i * 26)], v['edge'], 5)


def draw_desktop(p, v):
    # เคสด้านซ้าย
    p.grad(220, 268, 200, 430, v['top'], v['body'], r=10)
    p.rect(220, 268, 200, 430, outline=v['edge'], width=3, r=10)
    p.rect(244, 300, 152, 120, fill=blend(v['screen'], v['body'], 0.3), r=6)
    p.circle(320, 360, 30, fill=v['part'])
    p.circle(258, 452, 9, fill=RED)
    for i in range(7):
        p.line([(248, 490 + i * 26), (392, 490 + i * 26)], blend(v['edge'], v['part'], 0.45), 5)
    # จอด้านขวา
    p.grad(460, 240, 480, 310, v['top'], v['body'], r=10)
    p.rect(460, 240, 480, 310, outline=v['edge'], width=3, r=10)
    p.grad(480, 260, 440, 250, blend(v['screen'], (255, 255, 255), 0.16), v['screen'], r=4)
    p.rect(676, 550, 50, 72, fill=v['body'])
    p.rect(600, 622, 202, 24, fill=v['body'], r=12)
    # คีย์บอร์ดวางหน้าจอ
    p.rect(468, 660, 320, 34, fill=v['part'], r=8)
    for i in range(9):
        p.line([(486 + i * 34, 670), (486 + i * 34, 684)], blend(v['part'], v['edge'], 0.5), 6)


def draw_mouse(p, v):
    p.ellipse(600, 462, 148, 228, fill=v['body'])
    p.ellipse(600, 462, 148, 228, outline=v['edge'], width=3)
    p.ellipse(556, 372, 84, 130, fill=blend(v['body'], v['top'], 0.75))
    p.line([(600, 240), (600, 448)], v['edge'], 4)
    p.line([(474, 452), (726, 452)], blend(v['body'], v['edge'], 0.45), 3)
    # ลูกกลิ้งเป็นจุดแดงจุดเดียวของภาพ
    p.rect(584, 286, 32, 66, fill=RED, r=16)
    p.rect(578, 280, 44, 78, outline=v['edge'], width=3, r=20)
    p.line([(600, 234), (612, 150), (588, 60), (604, 0)], v['edge'], 12)
    p.line([(600, 234), (612, 150), (588, 60), (604, 0)], v['part'], 6)


def draw_cpu(p, v):
    p.grad(392, 292, 416, 416, blend(v['body'], v['edge'], 0.35), v['edge'], r=12)
    p.rect(392, 292, 416, 416, outline=blend(v['edge'], (0, 0, 0), 0.3), width=3, r=12)
    p.grad(432, 332, 336, 336, v['metal'], blend(v['metal'], v['edge'], 0.6), r=8)
    p.rect(432, 332, 336, 336, outline=blend(v['edge'], (0, 0, 0), 0.2), width=3, r=8)
    p.rect(464, 364, 272, 272, outline=blend(v['metal'], (255, 255, 255), 0.35), width=3, r=4)
    # สามเหลี่ยมแดงมุมล่างซ้ายคือหมุดบอกทิศการวาง
    p.poly([(422, 676), (468, 676), (422, 630)], fill=RED)
    for i in range(6):
        p.rect(412 + i * 66, 300, 20, 20, fill=blend(v['edge'], v['metal'], 0.3), r=3)
        p.rect(412 + i * 66, 680, 20, 20, fill=blend(v['edge'], v['metal'], 0.3), r=3)


def draw_ram(p, v):
    p.grad(170, 320, 860, 220, v['top'], v['body'], r=10)
    p.rect(170, 320, 860, 220, outline=v['edge'], width=3, r=10)
    p.rect(170, 320, 860, 26, fill=RED, r=8)
    # ครีบระบายความร้อนเอียง
    for i in range(20):
        x = 200 + i * 42
        p.line([(x, 366), (x - 26, 528)], blend(v['part'], v['edge'], 0.35), 9)
    p.rect(170, 320, 860, 220, outline=v['edge'], width=3, r=10)
    p.rect(190, 540, 820, 52, fill=blend(v['edge'], (0, 0, 0), 0.2), r=3)
    gold_pins(p, 200, 556, 800, 36, notch_at=548)


def draw_network(p, v):
    # เสาสัญญาณ 3 ต้น
    for x1, y1, x2, y2 in ((430, 440, 320, 214), (600, 440, 600, 186), (770, 440, 880, 214)):
        p.line([(x1, y1), (x2, y2)], v['edge'], 26)
        p.line([(x1, y1), (x2, y2)], v['part'], 16)
        p.circle(x2, y2, 13, fill=v['edge'])
    p.grad(330, 420, 540, 200, v['top'], v['body'], r=18)
    p.rect(330, 420, 540, 200, outline=v['edge'], width=3, r=18)
    # ไฟสถานะ ดวงแรกเป็นสีแดง
    for i in range(5):
        cx = 396 + i * 74
        p.circle(cx, 486, 15, fill=RED if i == 0 else blend(v['part'], v['edge'], 0.35))
    for i in range(4):
        p.rect(374 + i * 126, 552, 92, 44, fill=v['edge'], r=6)
        p.rect(388 + i * 126, 564, 64, 22, fill=blend(v['metal'], v['edge'], 0.25), r=3)
    p.rect(370, 620, 460, 22, fill=v['edge'], r=11)


def draw_headset(p, v):
    p.arc(600, 452, 236, 256, 196, 344, v['edge'], 34)
    p.arc(600, 452, 236, 256, 196, 344, v['part'], 22)
    for cx in (368, 832):
        p.grad(cx - 76, 400, 152, 240, v['top'], v['body'], r=70)
        p.rect(cx - 76, 400, 152, 240, outline=v['edge'], width=3, r=70)
        p.ellipse(cx, 520, 52, 88, fill=blend(v['screen'], v['body'], 0.4))
        p.ellipse(cx, 520, 52, 88, outline=v['edge'], width=3)
    # ก้านไมโครโฟน ปลายไมค์เป็นจุดแดง
    p.line([(392, 626), (330, 712), (410, 756)], v['edge'], 20)
    p.line([(392, 626), (330, 712), (410, 756)], v['part'], 12)
    p.circle(414, 758, 24, fill=RED)


def draw_monitor(p, v):
    p.grad(220, 160, 760, 470, v['top'], v['body'], r=12)
    p.rect(220, 160, 760, 470, outline=v['edge'], width=3, r=12)
    p.grad(246, 186, 708, 396, blend(v['screen'], (255, 255, 255), 0.18), v['screen'], r=4)
    p.poly([(246, 582), (430, 186), (530, 186), (346, 582)],
           fill=blend(v['screen'], (255, 255, 255), 0.05))
    p.rect(586, 600, 28, 8, fill=RED, r=4)
    p.rect(560, 630, 80, 96, fill=v['body'])
    p.rect(560, 630, 80, 96, outline=v['edge'], width=3)
    p.rect(450, 726, 300, 26, fill=v['body'], r=13)
    p.rect(450, 726, 300, 26, outline=v['edge'], width=3, r=13)


def draw_generic(p, v):
    # กล่องสินค้ามุมมองไอโซเมตริก มีเทปแดงพาดด้านบน
    p.poly([(600, 200), (890, 330), (600, 460), (310, 330)], fill=v['top'])
    p.poly([(310, 330), (600, 460), (600, 730), (310, 600)], fill=v['body'])
    p.poly([(890, 330), (890, 600), (600, 730), (600, 460)], fill=v['edge'])
    p.line([(600, 200), (890, 330), (600, 460), (310, 330), (600, 200)], v['edge'], 4)
    p.line([(600, 460), (600, 730)], blend(v['edge'], (0, 0, 0), 0.25), 4)
    p.poly([(455, 265), (745, 395), (700, 417), (410, 287)], fill=RED)
    p.line([(340, 380), (600, 496)], blend(v['body'], v['top'], 0.5), 5)
    p.line([(860, 380), (600, 496)], blend(v['edge'], v['body'], 0.4), 5)


# หมวดหมู่ -> ฟังก์ชันวาด และตำแหน่งเงาบนพื้น (cx, cy, rx, ry)
SCENES = {
    'psu':       (draw_psu, (600, 638, 290, 34)),
    'laptop':    (draw_laptop, (620, 626, 350, 32)),
    'case':      (draw_case, (570, 762, 210, 30)),
    'mainboard': (draw_mainboard, (600, 726, 330, 30)),
    'keyboard':  (draw_keyboard, (600, 606, 450, 30)),
    'gpu':       (draw_gpu, (570, 608, 400, 30)),
    'ups':       (draw_ups, (600, 736, 230, 30)),
    'webcam':    (draw_webcam, (600, 706, 160, 26)),
    'storage':   (draw_storage, (600, 636, 290, 32)),
    'desktop':   (draw_desktop, (600, 706, 350, 30)),
    'mouse':     (draw_mouse, (600, 694, 150, 26)),
    'cpu':       (draw_cpu, (600, 722, 220, 30)),
    'ram':       (draw_ram, (600, 606, 420, 28)),
    'network':   (draw_network, (600, 654, 260, 28)),
    'headset':   (draw_headset, (600, 664, 280, 30)),
    'monitor':   (draw_monitor, (600, 764, 260, 28)),
    'generic':   (draw_generic, (600, 748, 300, 32)),
}


def render(icon, variant):
    """คืนภาพ 1 ใบตามหมวดหมู่และโทนสีที่ระบุ"""
    draw_fn, shadow = SCENES.get(icon, SCENES['generic'])
    v = VARIANTS[variant]

    img = _linear(OUT_W * SS, OUT_H * SS, BG_TOP, BG_BOTTOM)
    scale = OUT_W * SS / W

    # เงาบนพื้น: วาดวงรีลงหน้ากากแล้วเบลอ ให้ของดูวางอยู่บนพื้นจริง
    cx, cy, rx, ry = shadow
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse(
        [(cx - rx) * scale, (cy - ry) * scale, (cx + rx) * scale, (cy + ry) * scale],
        fill=92,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(14 * scale))
    img.paste(Image.new('RGB', img.size, (24, 24, 27)), (0, 0), mask)

    draw_fn(Pen(img, scale), v)
    return img.resize((OUT_W, OUT_H), Image.LANCZOS)


class Command(BaseCommand):
    help = 'สร้างภาพประกอบสินค้าลง shop/static/shop/img/products/ (รันซ้ำได้)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='วาดใหม่ทับไฟล์ที่มีอยู่แล้ว',
        )

    def handle(self, *args, **options):
        out_dir = Path(__file__).resolve().parents[2] / 'static' / 'shop' / 'img' / 'products'
        out_dir.mkdir(parents=True, exist_ok=True)

        # ทุกคีย์ที่ Product.icon คืนได้ รวม 'generic' ที่เป็นค่าสำรอง
        icons = sorted(set(CATEGORY_ICONS.values()) | {'generic'})
        made = skipped = 0

        for icon in icons:
            for variant in PHOTO_VARIANTS:
                path = out_dir / f'{icon}-{variant}.png'
                if path.exists() and not options['force']:
                    skipped += 1
                    continue
                render(icon, variant).save(path, optimize=True)
                made += 1
                self.stdout.write(f'  วาด {path.name}')

        self.stdout.write(self.style.SUCCESS(
            f'เสร็จสิ้น: วาดใหม่ {made} ไฟล์, ข้ามของเดิม {skipped} ไฟล์ '
            f'({len(icons)} หมวด x {len(PHOTO_VARIANTS)} สี) ที่ {out_dir}'
        ))

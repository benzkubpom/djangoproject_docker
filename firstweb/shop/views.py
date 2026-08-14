from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Brand, Category, Product

PER_PAGE = 24

# key ที่รับจาก ?sort=  ->  (ป้ายที่แสดงใน dropdown, ฟิลด์ที่ใช้ order_by)
SORT_OPTIONS = {
    'new': ('ใหม่ล่าสุด', '-created_at'),
    'price_asc': ('ราคาน้อยไปมาก', 'price'),
    'price_desc': ('ราคามากไปน้อย', '-price'),
    'name': ('ชื่อ ก-ฮ / A-Z', 'name'),
}
DEFAULT_SORT = 'new'


def product_list(request):
    """หน้ารวมสินค้า: ค้นหา + กรองหมวดหมู่/แบรนด์ + เรียงลำดับ + แบ่งหน้า"""
    keyword = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    brand_id = request.GET.get('brand', '').strip()
    sort = request.GET.get('sort', DEFAULT_SORT)
    if sort not in SORT_OPTIONS:
        sort = DEFAULT_SORT

    products = Product.objects.select_related('brand', 'category')

    if keyword:
        products = products.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )

    # กรองเฉพาะเมื่อค่าที่ส่งมาเป็นตัวเลข กัน ValueError จาก query string ที่ถูกแก้มือ
    selected_category = None
    if category_id.isdigit():
        selected_category = Category.objects.filter(pk=category_id).first()
        if selected_category:
            products = products.filter(category=selected_category)

    selected_brand = None
    if brand_id.isdigit():
        selected_brand = Brand.objects.filter(pk=brand_id).first()
        if selected_brand:
            products = products.filter(brand=selected_brand)

    # ใส่ 'id' ต่อท้ายกัน order ไม่นิ่งตอนแบ่งหน้า เมื่อค่าที่ใช้เรียงซ้ำกัน
    products = products.order_by(SORT_OPTIONS[sort][1], 'id')

    paginator = Paginator(products, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    # query string เดิมที่ตัด page ออก เอาไว้ต่อท้ายลิงก์แบ่งหน้า
    params = request.GET.copy()
    params.pop('page', None)
    base_query = params.urlencode()

    context = {
        'page_obj': page_obj,
        'total_count': paginator.count,
        'categories': Category.objects.order_by('name'),
        'brands': Brand.objects.order_by('name'),
        'keyword': keyword,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'sort': sort,
        'sort_options': [(key, label) for key, (label, _) in SORT_OPTIONS.items()],
        'base_query': base_query,
        'has_filter': bool(keyword or selected_category or selected_brand),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """หน้ารายละเอียดสินค้า พร้อมสินค้าหมวดเดียวกัน 4 รายการ"""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category'), pk=pk
    )
    related = (
        Product.objects.select_related('brand', 'category')
        .filter(category=product.category)
        .exclude(pk=product.pk)
        .order_by('-created_at', 'id')[:4]
    )
    return render(
        request,
        'shop/product_detail.html',
        {'product': product, 'related': related},
    )

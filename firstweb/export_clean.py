import os
import django
from django.core.management import call_command

# ตั้งค่า Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstweb.settings')
django.setup()

# บังคับบันทึกไฟล์เป็น UTF-8 โดยตรงผ่าน Python
with open('shop_clean.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'shop', indent=2, stdout=f)

print("=== EXPORT CLEAN UTF-8 SUCCESSFUL ===")
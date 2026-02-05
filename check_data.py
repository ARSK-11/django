import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_product.settings")
django.setup()

from products.models import Produk

print("Checking Produk Data...")
products = Produk.objects.all()[:5]
for p in products:
    print(f"ID: {p.id_produk}, Name: '{p.nama_produk}'")

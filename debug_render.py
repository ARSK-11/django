import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_product.settings")
django.setup()

from django.template.loader import render_to_string
from products.models import Produk

print("--- START RENDER DEBUG ---")
try:
    # Filter like the view does
    products = Produk.objects.filter(status__nama_status__icontains='bisa dijual')[:1]
    if not products:
        print("No products found matching query.")
    else:
        # Render the template
        html = render_to_string('products/product_list.html', {'products': products})
        
        # Check specifically for the product name rendering
        p = products[0]
        print(f"Product Name in DB: {p.nama_produk}")
        
        if p.nama_produk in html:
            print("SUCCESS: Product name found in rendered HTML.")
        else:
            print("FAILURE: Product name NOT found in rendered HTML.")
            
        # Find the line in HTML corresponding to name
        for line in html.split('\n'):
            if "field-nama_produk" in line:
                print(f"Rendered Line: {line.strip()}")
                
except Exception as e:
    print(f"Error: {e}")

print("--- END RENDER DEBUG ---")

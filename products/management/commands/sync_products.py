import hashlib
import requests
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from products.models import Kategori, Status, Produk

class Command(BaseCommand):
    help = 'Sync products from FastPrint API'

    def handle(self, *args, **kwargs):
        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        # 1. Mengambil waktu sekarang secara otomatis
        now = datetime.now()
        date_str = now.strftime("%d%m%y")      # Format: 050226
        date_hyphen = now.strftime("%d-%m-%y") # Format: 05-02-26
        hour_str = now.strftime("%H")          # Format: 15 (jam sekarang)

        # 2. Menyusun Username & Password secara dinamis sesuai ketentuan
        # Tanpa underscore, ditambah kode C + Jam
        # NOTE: logic user: username = f"tesprogrammer{date_str}C{hour_str}"
        username = f"tesprogrammer{date_str}C{hour_str}" 
        password_raw = f"bisacoding-{date_hyphen}"
        password_md5 = hashlib.md5(password_raw.encode()).hexdigest()

        payload = {
            'username': username,
            'password': password_md5
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        self.stdout.write(f"Sending request to {url} with username: {username}...")
        try:
            response = requests.post(url, data=payload, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Log raw response for debugging if needed
                    # self.stdout.write(f"Response: {data}")

                    if isinstance(data, dict) and 'data' in data:
                         items = data['data']
                    elif isinstance(data, list):
                         items = data
                    else:
                         self.stdout.write(self.style.ERROR(f"Unexpected JSON format. Keys: {data.keys()}"))
                         return

                    self.stdout.write(f"Fetched {len(items)} items. Processing...")
                    
                    count_created = 0
                    count_updated = 0
                    
                    for item in items:
                        k_val = item.get('kategori') or item.get('nama_kategori') or "Uncategorized"
                        s_val = item.get('status') or item.get('nama_status') or "Unknown"
                        
                        cat_id = abs(hash(k_val)) % 100000 
                        stat_id = abs(hash(s_val)) % 100000
                        
                        prod_id = item.get('id_produk')
                        
                        if prod_id:
                            # Kategori
                            cat_obj, _ = Kategori.objects.get_or_create(
                                id_kategori=cat_id,
                                defaults={'nama_kategori': k_val}
                            )
                            if cat_obj.nama_kategori != k_val:
                                cat_obj.nama_kategori = k_val
                                cat_obj.save()

                            # Status
                            stat_obj, _ = Status.objects.get_or_create(
                                id_status=stat_id,
                                defaults={'nama_status': s_val}
                            )
                            if stat_obj.nama_status != s_val:
                                stat_obj.nama_status = s_val
                                stat_obj.save()
                            
                            # Produk
                            price = item.get('harga')
                            if isinstance(price, str):
                                price = ''.join(filter(str.isdigit, price))
                            
                            obj, created = Produk.objects.update_or_create(
                                id_produk=int(prod_id),
                                defaults={
                                    'nama_produk': item.get('nama_produk'),
                                    'harga': int(price) if price else 0,
                                    'kategori': cat_obj,
                                    'status': stat_obj
                                }
                            )
                            if created:
                                count_created += 1
                            else:
                                count_updated += 1
                            
                    self.stdout.write(self.style.SUCCESS(f'Sync completed. Created: {count_created}, Updated: {count_updated}'))
                    
                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR(f"Invalid JSON response: {response.text}"))
            else:
                 self.stdout.write(self.style.ERROR(f"API Error {response.status_code}: {response.text}"))
                 
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error connecting: {e}"))

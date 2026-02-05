from django.contrib import admin
from django.db.models import Max
from .models import Kategori, Status, Produk

class AutoIdAdmin(admin.ModelAdmin):
    # This abstract-like logic helps re-use ID generation
    def save_model(self, request, obj, form, change):
        if not change:  # Only when creating a new object
            # Determine the primary key field name
            pk_name = obj._meta.pk.name
            # Find the max value of the current PK
            max_id = obj.__class__.objects.aggregate(Max(pk_name))[f'{pk_name}__max']
            # Set the new ID
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1
            setattr(obj, pk_name, new_id)
        
        super().save_model(request, obj, form, change)

@admin.register(Kategori)
class KategoriAdmin(AutoIdAdmin):
    list_display = ('id_kategori', 'nama_kategori')
    exclude = ('id_kategori',)  # Hide from Add Form
    readonly_fields = ('id_kategori',) # Show as readonly in Edit Form

@admin.register(Status)
class StatusAdmin(AutoIdAdmin):
    list_display = ('id_status', 'nama_status')
    exclude = ('id_status',)
    readonly_fields = ('id_status',)

@admin.register(Produk)
class ProdukAdmin(AutoIdAdmin):
    list_display = ('id_produk', 'nama_produk', 'harga', 'kategori', 'status')
    list_filter = ('status', 'kategori')
    search_fields = ('nama_produk',)
    exclude = ('id_produk',)
    readonly_fields = ('id_produk',)

from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produk, Kategori, Status
from .serializers import ProdukSerializer, KategoriSerializer, StatusSerializer
from .forms import ProductForm

# API ViewSets
class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.select_related('kategori', 'status').all()
    serializer_class = ProdukSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# UI Views
def product_list(request):
    # Requirement: "Tampilkan data yang hanya memiliki status 'bisa dijual'"
    # We filter by status name containing "bisa dijual" (case insensitive)
    products = Produk.objects.filter(status__nama_status__icontains='bisa dijual').select_related('kategori', 'status')
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Handle Manual ID Generation
            new_product = form.save(commit=False)
            
            # Find max ID
            from django.db.models import Max
            max_id = Produk.objects.aggregate(Max('id_produk'))['id_produk__max']
            if max_id is None:
                new_product.id_produk = 1
            else:
                new_product.id_produk = max_id + 1
            
            new_product.save()
            messages.success(request, 'Produk berhasil ditambahkan')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Tambah Produk'})

def product_edit(request, pk):
    product = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diupdate')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Produk'})

def product_delete(request, pk):
    product = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produk berhasil dihapus')
    return redirect('product_list')

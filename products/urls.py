from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'produk', views.ProdukViewSet)
router.register(r'kategori', views.KategoriViewSet)
router.register(r'status', views.StatusViewSet)

urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    
    # UI Routes
    path('', views.product_list, name='product_list'),
    path('tambah/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('hapus/<int:pk>/', views.product_delete, name='product_delete'),
]

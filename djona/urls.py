from hashlib import sha256
import hashlib
from django.contrib import admin
from django.urls import path
from djona_admin import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

def hash_url(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexPage, name='index'),
    path(f'landing/{hash_url("produit")}/', views.Produit, name='product'),
    path(f'findDetaiProdHash/secure-area/{hash_url("product")}/<str:id>/', views.ProductDetailPage, name='product_detail'),
    path(f'find/{hash_url("recherche-vehicule")}/', views.searchCar, name='recherche'),
    path(f'purchase/{hash_url("accueil/achat")}/', views.AchatPage, name='achat'),
    path(f'showcase/{hash_url("slide")}/', views.common_view, name='slide'),
    path(f'repair/{hash_url("carrosseriePlus")}/', views.carrosseriePage, name='carrosseriePlus'),
    path(f'get-in-touch/{hash_url("contact")}/', views.ContactConsPage, name='contactCons'),
    
    # path(f'carreuFindtact/{hash_url("contactVehi")}/<int:product_id>/', views.ContactPage, name='contact'),
    path('contact/<int:product_id>/', views.ContactPage, name='contact'),
    
    path(f'AboFindtUs/{hash_url("accueil/djona/about-us")}/', views.AboutPage, name='about'),
    path(f'joinFindUs/{hash_url("accueil/djona/join-us")}/', views.RejoindrePage, name='rejoindre'),
    path(f'locFindServ/{hash_url("accueil/location-service")}/', views.LocationPage, name='location'),
    path(f'squaFindPar/{hash_url("accueil/spare-parts")}/', views.piece_detache, name='piece-detache'),
    
    
    path(f'condactvfFindPar/{hash_url("accueil/contacts")}/''contacts/', views.ContactPage_View, name='contacts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




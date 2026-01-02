from django.contrib import admin
from django.utils.html import mark_safe
from djona_admin.models import A_propos_de_nou, Advertisement, ClientInformation, Concessionnaire, Config_Site, Fidelisation, Image, Information, Nos_service, Particulier, Produit, EtatVehicule, PieceDetache, LogoPartenaire, Service_Adapte, Valeur

# Register your models here.
    
class AdminProduit(admin.ModelAdmin):
    list_display = (
        'id', 'is_published', 'first_image', 'marque', 'modele', 'carburant', 'type', 'ville', 'annee', 'nom_entreprise', 'contact', 'date_ajout', 'statut'
    )
    search_fields = ('marque', 'modele', 'ville', 'nom_entreprise', 'contact', 'annee')
    list_filter = ('carburant', 'type', 'ville', 'date_ajout')
    actions = ['make_published', 'make_unpublished'] 
    
    def first_image(self, obj):
        image = obj.images.first()
        if image and hasattr(image, 'image') and image.image:
            return mark_safe(f'<img src="{image.image.url}" width="50" height="50" style="border-radius: 5px;" />')
        return 'Aucune image'

    first_image.short_description = 'Image'

    ordering = ('-date_ajout',)
    

class AdminImage(admin.ModelAdmin):
    list_display = ('image', 'date_ajout')
    
    
class AdminLogoPartenaire(admin.ModelAdmin):
    list_display = ('image', 'nom')
    

class AdminA_propos_de_nou(admin.ModelAdmin):
    list_display = ('titre', 'is_published', 'date_ajout')
    list_filter = ('is_published', 'date_ajout')
    search_fields = ('titre', 'description')
    actions = ['make_published', 'make_unpublished'] 
    
    # Actions pour publier/dépublier
    @admin.action(description="Publier les éléments sélectionnés")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Dépublier les éléments sélectionnés")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        

class AdminNos_service(admin.ModelAdmin):
    list_display = ('titre', 'is_published', 'date_ajout')
    list_filter = ('is_published', 'date_ajout')
    search_fields = ('titre', 'description')
    actions = ['make_published', 'make_unpublished'] 
    
    # Actions pour publier/dépublier
    @admin.action(description="Publier les éléments sélectionnés")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Dépublier les éléments sélectionnés")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        
        

class AdminService_Adapte(admin.ModelAdmin):
    list_display = ('titre', 'is_published', 'date_ajout')
    list_filter = ('is_published', 'date_ajout')
    search_fields = ('titre', 'description')
    actions = ['make_published', 'make_unpublished'] 
    
    # Actions pour publier/dépublier
    @admin.action(description="Publier les éléments sélectionnés")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Dépublier les éléments sélectionnés")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        
        
    
        
class AdminEtatVehicule(admin.ModelAdmin):
    list_display = ('nom', 'date_ajout')
        
        
class AdminReservation(admin.ModelAdmin):
    list_display = (
        'id','produit'
    )

class AdminFidelisation(admin.ModelAdmin):
    list_display = ('svg_code', 'title', 'description')
    
    
class AdminInformation(admin.ModelAdmin):
    list_display = ('description', 'date_ajout')
    

class AdminValeur(admin.ModelAdmin):
    list_display = ('svg_code', 'title', 'description')


class AdminPieceDetache(admin.ModelAdmin):
    list_display = ('images', 'nom', 'prix_normal', 'prix_reduit', 'date_ajout')
    
class AdminConfig_Site(admin.ModelAdmin):
    list_display = ('nom', 'couleur', 'image') 

class AdminClientInformation(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'marque', 'modele', 'numero', 'ville', 'email', 'description', 'created_at')


class AdminAdvertisement(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    
    
class AdminConcessionnaire(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'numero', 'ville', 'localisation', 'nombre_vehicule')


class AdminParticulier(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'numero', 'ville', 'localisation', 'nombre_vehicule')

    
    
# Enregistrer les modèles dans l'admin
admin.site.register(Produit, AdminProduit)
admin.site.register(LogoPartenaire, AdminLogoPartenaire)
admin.site.register(Fidelisation, AdminFidelisation)
admin.site.register(Valeur, AdminValeur)
admin.site.register(Image, AdminImage)
admin.site.register(Information, AdminInformation)
admin.site.register(EtatVehicule, AdminEtatVehicule)
admin.site.register(PieceDetache, AdminPieceDetache)
admin.site.register(Config_Site, AdminConfig_Site)
admin.site.register(ClientInformation, AdminClientInformation)
admin.site.register(A_propos_de_nou, AdminA_propos_de_nou)
admin.site.register(Nos_service, AdminNos_service)
admin.site.register(Service_Adapte, AdminService_Adapte)
admin.site.register(Advertisement, AdminAdvertisement)
admin.site.register(Particulier, AdminParticulier)
admin.site.register(Concessionnaire, AdminConcessionnaire)









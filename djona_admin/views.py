from datetime import datetime
from glob import escape
from itertools import cycle
from warnings import filters
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
import hashlib
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from djona_admin.models import A_propos_de_nou, Advertisement, CarouselImage, ClientInformation, Concessionnaire, Config_Site, EtatVehicule, Fidelisation, Image, Information, LogoPartenaire, Nos_service, Particulier, PieceDetache, Produit, Service_Adapte, Valeur
from django.db.models import Q
from collections import Counter
from collections import defaultdict
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Min
from django.utils.timezone import now
from django.template.loader import render_to_string



def filter_products(base_queryset, filters):
    return base_queryset.filter(filters) if filters else base_queryset


# def IndexPage(request):
#     list_products = Produit.objects.all()
    
#     whatsapp_message = None
#     if list_products.exists():
#         whatsapp_message = list_products.first().whatsapp_message()

#     vente_statut = EtatVehicule.objects.filter(nom='vente').first()
#     location_statut = EtatVehicule.objects.filter(nom='location').first()
    
#     all_filtered_products = list_products.filter(
#         Q(statut=vente_statut) | Q(statut=location_statut)
#     )

#     filtered_products = filter_products(all_filtered_products, filters)
#     vente_products = filtered_products.filter(statut=vente_statut)
#     location_products = filtered_products.filter(statut=location_statut)

#     if not error_message and not filtered_products.exists():
#         error_message = "Aucun véhicule ne correspond aux critères de recherche."

#     unique_marques = (
#         list_products.values('marque')
#         .annotate(product_count=Count('id'))
#         .order_by('-product_count')[:6]
#     )
#     unique_marques_recherche = (
#         list_products.values('marque')
#         .annotate(product_count=Count('id'))
#         .order_by('-product_count')[:6]
#     )
#     unique_type = (
#         list_products.values('type')
#         .annotate(product_count=Count('id'))
#         .order_by('-product_count')[:6]
#     )
#     unique_transmission = (
#         list_products.values('transmission')
#         .annotate(product_count=Count('id'))
#         .order_by('-product_count')[:6]
#     )
#     unique_carburants = (
#         list_products.values('carburant')
#         .annotate(product_count=Count('id'))
#         .order_by('-product_count')[:6]
#     )
#     selected_marques = [marque['marque'] for marque in unique_marques]
#     unique_marques_recherche = [marque['marque'] for marque in unique_marques_recherche]
#     unique_transmission = [transmission['transmission'] for transmission in unique_transmission]
#     unique_carburants = [carburant['carburant'] for carburant in unique_carburants]
    

#     products_by_marque = {
#         marque: list_products.filter(marque=marque)[:4]
#         for marque in selected_marques
#     }
#     products_by_marque_list = [
#         (marque, products) for marque, products in products_by_marque.items()
#     ]
#     vente_marques = (
#         vente_products.values_list('marque', flat=True)
#         .distinct()
#         .order_by('marque')
#     )
#     location_marques = (
#         location_products.values_list('marque', flat=True)
#         .distinct()
#         .order_by('marque')
#     )

#     marque_filtered_products = filtered_products.filter(marque__in=selected_marques)

#     def get_image_count_and_first_url(product):
#         return product.image_count(), product.first_image_url()
    
#     type_counts = Counter(product.
#     type.lower() for product in vente_products if product.type)
    
#     carrosserie_by_marque = defaultdict(set)
#     transmission_by_marque_and_carrosserie = defaultdict(lambda: defaultdict(set))
    
#     carburant_by_marque_and_carrosserie_and_transmission = defaultdict(
#         lambda: defaultdict(lambda: defaultdict(set))
#     )
    
#     produits = Produit.objects.all()
    
#     for produit in produits:
#         carrosserie_by_marque[produit.marque].add(produit.type)
#     for produit in produits:
#         transmission_by_marque_and_carrosserie[produit.marque][produit.type].add(produit.transmission)
#     for produit in produits:
#         carburant_by_marque_and_carrosserie_and_transmission[produit.marque][produit.type][produit.transmission].add(produit.carburant)

#     carrosserie_by_marque = {marque: list(types) for marque, types in carrosserie_by_marque.items()}
#     transmission_by_marque_and_carrosserie = {
#         marque: {carrosserie: list(transmissions) for carrosserie, transmissions in carross_dict.items()}
#         for marque, carross_dict in transmission_by_marque_and_carrosserie.items()
#     }
#     carburant_by_marque_and_carrosserie_and_transmission = {
#         marque: {
#             carrosserie: {
#                 transmission: list(carburants)
#                 for transmission, carburants in trans_dict.items()
#             }
#             for carrosserie, trans_dict in carross_dict.items()
#         }
#         for marque, carross_dict in carburant_by_marque_and_carrosserie_and_transmission.items()
#     }
        
#     context = {
#         "list_products": marque_filtered_products,
#         "products_by_marque": products_by_marque,
#         "message": error_message,
#         "type_counts": list(type_counts.items()),
#         "unique_marques": unique_marques,
#         "unique_marques_recherche": unique_marques_recherche,
#         "unique_transmission": unique_transmission,
#         "unique_carburants": unique_carburants,
#         "first_image_urls": [get_image_count_and_first_url(product)[1] for product in filtered_products],
#         "image_counts": [get_image_count_and_first_url(product)[0] for product in filtered_products],
#         "whatsapp_message": whatsapp_message,        
#         "selected_marques": selected_marques,
#         "vente_marques": vente_marques,
#         "location_marques": location_marques,
#         "products_by_marque_list": products_by_marque_list,
#         "carrosserie_by_marque": carrosserie_by_marque,
#         "unique_marques": list(carrosserie_by_marque.keys()),
#         "transmission_by_marque_and_carrosserie": transmission_by_marque_and_carrosserie,
#         "unique_marques": list(transmission_by_marque_and_carrosserie.keys()),
#         "carburant_by_marque_and_carrosserie_and_transmission": carburant_by_marque_and_carrosserie_and_transmission,
#     }

#     return render(request, "index.html", context)





# IndexPage: Vue principale pour afficher les produits
# Optimisée, structurée et commentée
def IndexPage(request):
    # Récupérer tous les produits
    list_products = Produit.objects.filter(is_published=True)
    config_site = Config_Site.objects.filter(is_published=True)
    logos = LogoPartenaire.objects.filter(is_published=True)
                
    serv = Service_Adapte.objects.filter(is_published=True)

    # Initialiser le message WhatsApp s'il existe des produits
    whatsapp_message = list_products.first().whatsapp_message() if list_products.exists() else None

    # Récupération des statuts
    vente_statut = EtatVehicule.objects.filter(nom='vente').first()
    location_statut = EtatVehicule.objects.filter(nom='location').first()

    # Filtrer les produits selon les statuts "vente" et "location"
    vente_products = list_products.filter(statut=vente_statut).order_by('-id')[:8]
    location_products = list_products.filter(statut=location_statut).order_by('-id')[:8]

    # Appliquer les filtres supplémentaires fournis par l'utilisateur
    filters = build_filters(request)
    all_filtered_products = list_products.filter(
        Q(statut=vente_statut) | Q(statut=location_statut)
    )
    filtered_products = filter_products(all_filtered_products, filters)
    
    # Séparer les produits en fonction du statut
    vente_products = filtered_products.filter(statut=vente_statut)
    location_products = filtered_products.filter(statut=location_statut)

    # Gérer le message d'erreur si aucun produit ne correspond
    error_message = None
    if not filters and not filtered_products.exists():
        error_message = "Aucun véhicule ne correspond aux critères de recherche."

    # Récupérer les marques, types, transmissions et carburants uniques (Top 6 par popularité)
    unique_marques = get_unique_values(vente_products, 'marque')
    unique_type = get_unique_values(vente_products, 'type')
    unique_transmission = get_unique_values(vente_products, 'transmission')
    unique_carburants = get_unique_values(vente_products, 'carburant')

    selected_marques = [marque['marque'] for marque in unique_marques]

    # Construire les produits par marque
    products_by_marque = {
        marque: list_products.filter(marque=marque)[:4]
        for marque in selected_marques
    }
    products_by_marque_list = [
        (marque, products) for marque, products in products_by_marque.items()
    ]

    # Extraire les marques spécifiques aux produits en vente et en location
    # vente_marques = vente_products.values_list('marque', flat=True).distinct().order_by('marque')
    # location_marques = location_products.values_list('marque', flat=True).distinct().order_by('marque')
    vente_marques = vente_products.values_list('marque', flat=True).distinct().order_by('marque')[:6]
    location_marques = location_products.values_list('marque', flat=True).distinct().order_by('marque')[:6]


    # Filtrer les produits selon les marques sélectionnées
    marque_filtered_products = filtered_products.filter(marque__in=selected_marques)

    type_data = defaultdict(lambda: {"count": 0, "image": None})

    for product in vente_products:
        if product.type:
            product_type = product.type.lower()
            type_data[product_type]["count"] += 1
            if not type_data[product_type]["image"]:
                type_data[product_type]["image"] = product.first_image_url() or "/static/images/default.jpg"

    type_data = [
        {"type": key, "count": value["count"], "image": value["image"]}
        for key, value in type_data.items()
    ]

    # Organiser les carrosseries, transmissions et carburants par marque
    carrosserie_by_marque, transmission_by_marque_and_carrosserie, carburant_by_marque_and_carrosserie_and_transmission = organize_by_attributes(list_products, vente_statut)

    # Préparer le contexte pour le rendu du template
    context = {
        "list_products": marque_filtered_products,
        "products_by_marque": products_by_marque,
        "message": error_message,
        # "type_counts": list(type_counts.items()),
        "type_data": type_data,
        "unique_marques": unique_marques,
        "unique_type": unique_type,
        "unique_transmission": unique_transmission,
        "unique_carburants": unique_carburants,
        "first_image_urls": [get_image_info(product)[1] for product in filtered_products],
        "image_counts": [get_image_info(product)[0] for product in filtered_products],
        "whatsapp_message": whatsapp_message,
        "selected_marques": selected_marques,
        "vente_marques": vente_marques,
        "location_marques": location_marques,
        "products_by_marque_list": products_by_marque_list,
        "carrosserie_by_marque": carrosserie_by_marque,
        "transmission_by_marque_and_carrosserie": transmission_by_marque_and_carrosserie,
        "carburant_by_marque_and_carrosserie_and_transmission": carburant_by_marque_and_carrosserie_and_transmission,
        "vente_products": vente_products,
        "location_products": location_products,
        'logos': logos,
        'config_site': config_site,
        'serv': serv,
    }

    return render(request, "index.html", context)


# Fonction utilitaire : Construire les filtres selon les paramètres de la requête
def build_filters(request):
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    selected_type = request.GET.get('type', '').strip().lower()

    filters = Q()
    if min_price.isdigit():
        filters &= Q(prix__gte=int(min_price))
    if max_price.isdigit():
        filters &= Q(prix__lte=int(max_price))
    if selected_type in ["occasion", "neuve"]:
        filters &= Q(type__iexact=selected_type)

    return filters

# Fonction utilitaire : Obtenir les valeurs uniques pour un champ donné
def get_unique_values(queryset, field):
    """
    Retourne les valeurs uniques d'un champ avec un décompte.
    """
    return (
        queryset.values(field)
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )

# Fonction utilitaire : Obtenir les informations d'image d'un produit
def get_image_info(product):
    return product.image_count(), product.first_image_url()

# Fonction utilitaire : Organiser les produits par carrosserie, transmission et carburant
def organize_by_attributes(products, vente_statut):
    """
    Organise les produits par marque, carrosserie, transmission et carburant,
    en se limitant aux produits associés au statut "vente".
    """
    # Filtrer les produits en fonction du statut "vente"
    vente_products = products.filter(statut=vente_statut)

    # Initialiser les structures de données pour l'organisation
    carrosserie_by_marque = defaultdict(set)
    transmission_by_marque_and_carrosserie = defaultdict(lambda: defaultdict(set))
    carburant_by_marque_and_carrosserie_and_transmission = defaultdict(
        lambda: defaultdict(lambda: defaultdict(set))
    )

    # Parcourir les produits filtrés
    for produit in vente_products:
        marque = produit.marque
        carrosserie = produit.type  # Supposons que "type" correspond à la carrosserie
        transmission = produit.transmission
        carburant = produit.carburant

        # Organiser les carrosseries par marque
        carrosserie_by_marque[marque].add(carrosserie)

        # Organiser les transmissions par marque et carrosserie
        transmission_by_marque_and_carrosserie[marque][carrosserie].add(transmission)

        # Organiser les carburants par marque, carrosserie et transmission
        carburant_by_marque_and_carrosserie_and_transmission[marque][carrosserie][transmission].add(carburant)

    # Convertir les sets en listes pour une meilleure utilisation dans le template
    carrosserie_by_marque = {marque: list(types) for marque, types in carrosserie_by_marque.items()}
    transmission_by_marque_and_carrosserie = {
        marque: {carrosserie: list(transmissions) for carrosserie, transmissions in carross_dict.items()}
        for marque, carross_dict in transmission_by_marque_and_carrosserie.items()
    }
    carburant_by_marque_and_carrosserie_and_transmission = {
        marque: {
            carrosserie: {
                transmission: list(carburants)
                for transmission, carburants in trans_dict.items()
            }
            for carrosserie, trans_dict in carross_dict.items()
        }
        for marque, carross_dict in carburant_by_marque_and_carrosserie_and_transmission.items()
    }

    return carrosserie_by_marque, transmission_by_marque_and_carrosserie, carburant_by_marque_and_carrosserie_and_transmission
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""






# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de recherche de véhicules
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def searchCar(request):
    """
    Vue pour rechercher des voitures en fonction de plusieurs critères.
    La recherche est limitée aux voitures en vente uniquement.
    """
    # Récupération des paramètres de recherche
    marque = request.GET.get('marque', '').strip()
    carrosserie = request.GET.get('type', '').strip()
    boite = request.GET.get('transmission', '').strip()
    carburant = request.GET.get('carburant', '').strip()
    
    config_site = Config_Site.objects.filter(is_published=True)


    # Messages d'erreur par critère
    messages_erreur = {
        'marque': None,
        'type': None,
        'transmission': None,
        'carburant': None,
    }

    # Filtrage des véhicules en vente uniquement
    filtres = Q(statut__nom='vente')

    # Application des filtres basés sur les paramètres utilisateur
    if marque:
        filtres &= Q(marque__iexact=marque)
        if not Produit.objects.filter(marque__iexact=marque, statut__nom='vente').exists():
            messages_erreur['marque'] = f"Aucune marque ne correspond à '{marque}'."

    if carrosserie:
        filtres &= Q(type__iexact=carrosserie)
        if not Produit.objects.filter(type__iexact=carrosserie, statut__nom='vente').exists():
            messages_erreur['type'] = f"Aucun type de carrosserie ne correspond à '{carrosserie}'."

    if boite:
        filtres &= Q(transmission__iexact=boite)
        if not Produit.objects.filter(transmission__iexact=boite, statut__nom='vente').exists():
            messages_erreur['transmission'] = f"Aucune transmission ne correspond à '{boite}'."

    if carburant:
        filtres &= Q(carburant__iexact=carburant)
        if not Produit.objects.filter(carburant__iexact=carburant, statut__nom='vente').exists():
            messages_erreur['carburant'] = f"Aucun carburant ne correspond à '{carburant}'."

    # Filtrage des produits en fonction des critères
    produits = Produit.objects.filter(filtres)

    # Gestion du message général si aucun produit trouvé
    message = None
    if not produits.exists():
        message = "Aucun véhicule en vente ne correspond à vos critères."

    # Pagination des résultats
    paginator = Paginator(produits, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Récupération des valeurs uniques pour les filtres dynamiques
    unique_marques = Produit.objects.filter(statut__nom='vente').values_list('marque', flat=True).distinct()
    unique_carrosseries = Produit.objects.filter(statut__nom='vente').values_list('type', flat=True).distinct()
    unique_boites = Produit.objects.filter(statut__nom='vente').values_list('transmission', flat=True).distinct()
    unique_carburants = Produit.objects.filter(statut__nom='vente').values_list('carburant', flat=True).distinct()

    # Construction du contexte pour le rendu du template
    contexte = {
        'produits': page_obj.object_list,
        'message': message,
        'messages_erreur': messages_erreur,
        "is_location_page": False,
        "is_piece_detache_page": False,
        'is_recherche_vehicule_page': True,
        "list_products": page_obj.object_list,
        "page_obj": page_obj,
        "unique_marques": unique_marques,
        "unique_carrosseries": unique_carrosseries,
        "unique_boites": unique_boites,
        "unique_carburants": unique_carburants,
        'config_site': config_site,
    }

    return render(request, 'recherchevehicule.html', contexte)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# def AchatPage(request):
#     list_products = Produit.objects.filter(statut__nom__iexact='vente')
#     images = CarouselImage.objects.all()
    
#     message = "Aucun véhicule en vente pour l'instant." if not list_products.exists() else ""
    
#     paginator = Paginator(list_products, 6) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     for product in page_obj.object_list:
#         product.hashed_id = hashlib.sha256(str(product.id).encode('utf-8')).hexdigest()

#     context = {
#         "list_products": page_obj.object_list,
#         "message": message,
#         "page_obj": page_obj,
#         'images': images,
#     }
#     return render(request, "achat.html", context)





# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de achat de véhicules
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def AchatPage(request):
    """
    Vue pour la page d'achat, affichant les véhicules disponibles à la vente avec pagination.
    """

    # Récupération des produits en vente uniquement
    list_products = Produit.objects.filter(statut__nom__in=['vente', 'vendu'], is_published=True)
    config_site = Config_Site.objects.filter(is_published=True)
    
    # Récupération des publicités actives et non expirées
    ads = Advertisement.objects.filter(is_active=True, expires_at__gt=now())

    # Récupération des informations et des images du carrousel
    informations = Information.objects.filter(is_published=True)    
    images = CarouselImage.objects.all()

    # Message par défaut si aucun produit n'est disponible
    message = "Aucun véhicule en vente pour l'instant." if not list_products.exists() else ""

    # Pagination (16 produits par page)
    paginator = Paginator(list_products, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Itérateur cyclique pour les publicités
    ads_cycle = cycle(ads)
    combined_list = []
    
    # Organiser les produits et les publicités
    for i, product in enumerate(page_obj.object_list, start=1):
        combined_list.append({'type': 'product', 'data': product})
        # Insérer une publicité après le 2e produit de chaque ligne (logique utilisateur)
        if i % 3 == 0:
            ad = next(ads_cycle, None)
            if ad:
                combined_list.append({'type': 'advertisement', 'data': ad})

    # Génération d'un identifiant haché pour chaque produit (sécurisé pour les URL)
    for product in page_obj.object_list:
        product.hashed_id = hashlib.sha256(str(product.id).encode('utf-8')).hexdigest()

    # Statistiques et données complémentaires
    unique_marques = list_products.values_list('marque', flat=True).distinct()

    # Contexte à passer au template
    context = {
        "list_products": page_obj.object_list,
        "message": message,
        "page_obj": page_obj,
        "images": images,
        "unique_marques": unique_marques,     
        'informations': informations,
        'config_site': config_site,
        'ads': ads,
        'combined_list': combined_list,
    }

    return render(request, "achat.html", context)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# def LocationPage(request):
#     list_products = Produit.objects.filter(statut__nom__iexact='location') 
#     images = CarouselImage.objects.all()
   
#     if list_products.count() < 1:
#         message = "Aucun véhicule en location pour l'instant."
#     else:
#         message = ""

#     paginator = Paginator(list_products, 8) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     for product in page_obj.object_list:
#         product.hashed_id = hashlib.sha256(str(product.id).encode('utf-8')).hexdigest()

#     context = {
#         "message": message,
#         "page_obj": page_obj,
#         "is_location_page": True,
#         "is_piece_detache_page": False, 
#         'is_recherche_vehicule_page': False,
#         'images': images,
#     }
#     return render(request, "location.html", context)



# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de location de véhicules
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def LocationPage(request):
    """
    Vue pour afficher les véhicules disponibles à la location, avec informations sur les réservations.
    """
    # Filtrer les véhicules en location ou réservés
    list_products = Produit.objects.filter(statut__nom__in=['location', 'réservé'], is_published=True)
    config_site = Config_Site.objects.filter(is_published=True)

    informations = Information.objects.filter(is_published=True)
    images = CarouselImage.objects.all()

    # Vérifier s'il y a des produits disponibles
    if list_products.count() < 1:
        message = "Aucun véhicule en location pour l'instant."
    else:
        message = ""

    # Pagination
    paginator = Paginator(list_products, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexte à passer au template
    context = {
        "message": message,
        "page_obj": page_obj,
        "is_location_page": True,
        "is_piece_detache_page": False,
        'is_recherche_vehicule_page': False,
        'images': images,
        'informations': informations,
        'config_site': config_site
    }
    return render(request, "location.html", context)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# def piece_detache(request):
#     images = PieceDetache.objects.all()    

#     if not images.exists():
#         message = "Aucune pièce détachée disponible pour le moment."
#     else:
#         message = None

#     context = {
#         'message': message, 
#     }
    
#     return render(request, "piece-detache.html", context)




# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de piece de véhicules
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def piece_detache(request):
    images = PieceDetache.objects.all() 
    config_site = Config_Site.objects.filter(is_published=True)

    if not images.exists():
        message = "Aucune pièce détachée disponible pour le moment."
    else:
        message = None

    context = {
        'message': message, 
        'config_site': config_site
    }
    
    return render(request, "piece-detache.html", context)


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""








# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de logo des partenaires
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# def logo_partenaire_view(request):
#     logos = LogoPartenaire.objects.all()
#     return render(request, 'show_logos.html', {'logos': logos})


# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""











# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        # Fonction de produit détail de véhicules
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def ProductDetailPage(request, id):
    product = get_object_or_404(Produit, id=id)
    config_site = Config_Site.objects.filter(is_published=True)   
    
    valeurs = Valeur.objects.filter(is_published=True)
    fidelisation = Fidelisation.objects.filter(is_published=True)   

    if not product:
        raise Http404("Produit non trouvé")

    whatsapp_message = product.whatsapp_message()
    image_urls = [image.image.url for image in product.images.all()]
    images = product.images.all()

    statut = product.statut
    ville = product.ville

    # Trouver des produits similaires
    similar_products = Produit.objects.filter(
        prix=product.prix,
        statut=statut,
        ville=ville
    ).exclude(id=id) 

    similar_products = similar_products[:8]

    # Comptage des véhicules disponibles par marque et modèle pour le produit sélectionné
    vehicule_counts = (
        Produit.objects.filter(marque=product.marque, modele=product.modele, statut__nom='vente')
        .values('marque', 'modele') 
        .annotate(total=Count('id')) 
    )
    
    vehiculesLoc_counts = (
        Produit.objects.filter(marque=product.marque, modele=product.modele, statut__nom='location')
        .values('marque', 'modele') 
        .annotate(total=Count('id')) 
    )
    
    # Préparer le contexte pour le template
    context = {
        "product": product,
        "whatsapp_message": whatsapp_message,
        "image_urls": image_urls,
        "images": images,
        'similar_products': similar_products,
        'statut': statut, 
        'ville': ville, 
        'valeurs': valeurs,
        'fidelisation': fidelisation,
        "vehicule_counts": vehicule_counts,
        "vehiculesLoc_counts": vehiculesLoc_counts,
        'config_site': config_site
    }
    
    return render(request, "product_detail.html", context)

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""





def AboutPage(request):
    elements = A_propos_de_nou.objects.filter(is_published=True)
    config_site = Config_Site.objects.filter(is_published=True)   
    
    service = Nos_service.objects.filter(is_published=True)
    
    context = {
        'elements': elements, 
        'service': service,
        'config_site': config_site 
    }
    
    return render(request, "about.html", context)






def RejoindrePage(request):
    config_site = Config_Site.objects.filter(is_published=True)      
    
    context = {
        'config_site': config_site 
    }
    return render(request, "rejoindre.html", context)




def ContactConsPage(request):
    config_site = Config_Site.objects.filter(is_published=True)   
    
    context = {
        'config_site': config_site 
    }
    return render(request, "contactCons.html", context)


def carrosseriePage(request):
    config_site = Config_Site.objects.filter(is_published=True)   
    
    type_counts = (
        Produit.objects.values('type')
        .annotate(count=Count('id'))
        .order_by('type')
    )

    first_images = {
        item['type']: Produit.objects.filter(type=item['type'])
        .values_list('images', flat=True)
        .first() or '/static/images/default-car.png'
        for item in type_counts
    }

    context = {
        'type_counts': type_counts,
        'first_images': first_images, 
        'config_site': config_site 
    }
    return render(request, 'carrosseriePlus.html', context)






def common_view(request):
    images = CarouselImage.objects.all()
    config_site = Config_Site.objects.filter(is_published=True)      

    return render(request, 'slide.html', {'images': images, 'config_site': config_site})









def ContactPage(request, product_id):
    config_site = Config_Site.objects.filter(is_published=True)
    product = get_object_or_404(Produit, id=product_id)
    
    subject = "Demande d'information sur un véhicule"
    admin_email = settings.EMAIL_HOST_USER  # L'email de l'admin pour l'envoi
    message = ""
    
    if request.method == "POST":
        # Récupération des données du formulaire
        marque = request.POST.get("marque")
        modele = request.POST.get("modele")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        numero = request.POST.get("numero")
        ville = request.POST.get("ville")
        user_email = request.POST.get("email")
        description = request.POST.get("description")
        
        # Préparation du message HTML pour l'utilisateur
        user_html_message = render_to_string('emails/contact_email.html', {
            'marque': marque,
            'modele': modele,
            'nom': nom,
            'prenom': prenom,
            'numero': numero,
            'ville': ville,
            'user_email': user_email,  
            'description': description, 
        })
        
        # Préparation du message HTML pour l'admin
        admin_html_message = render_to_string('emails/admin_contact_email.html', {
            'marque': marque,
            'modele': modele,
            'nom': nom,
            'prenom': prenom,
            'numero': numero,
            'ville': ville,
            'user_email': user_email,  # Email de l'utilisateur (pas admin_email ici)
            'description': description,
            'product_id': product_id,  # L'ID du produit
        })
        
        # Envoi du mail à l'utilisateur
        send_mail(
            subject="Merci de nous avoir contacté !",  # Un titre plus orienté vers le client
            message='',  # Pas de message texte, uniquement le HTML
            from_email=admin_email,  # L'admin en tant qu'expéditeur
            recipient_list=[user_email],  # L'email du client
            fail_silently=False,
            html_message=user_html_message,
        )
        
        # Envoi du mail à l'administrateur
        send_mail(
            subject=f"{subject} - ID Produit: {product_id}",
            message='',  # Pas de message texte
            from_email=admin_email,
            recipient_list=[admin_email],  # Email de l'admin
            fail_silently=False,
            html_message=admin_html_message,
        )
    
    context = {
        'product': product,
        'config_site': config_site,
    }
    
    return render(request, 'contactVehi.html', context)








def ContactPage_View(request):
    config_site = Config_Site.objects.filter(is_published=True)      

    return render(request, 'contacts.html', {'config_site': config_site})







def contact_form_submission(request):
    if request.method == "POST":
        statut = request.POST.get("statut")
        
        # Données communes
        civilite = request.POST.get("civilite")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        ville = request.POST.get("ville")
        localisation = request.POST.get("localisation")
        nombre_vehicule = request.POST.get("nombre_vehicule")

        # Gestion des statuts
        if statut == "concessionnaire":
            nom_entreprise = request.POST.get("nom_entreprise")
            numero = request.POST.get("numero")
            email = request.POST.get("email")
            
            # Enregistrement dans la table Concessionnaire
            Concessionnaire.objects.create(
                civilite=civilite,
                nom=nom,
                prenom=prenom,
                nom_entreprise=nom_entreprise,
                numero=numero,
                email=email,
                ville=ville,
                localisation=localisation,
                nombre_vehicule=nombre_vehicule,
            )
        elif statut == "particulier":
            numero_particulier = request.POST.get("numero_particulier")
            email = request.POST.get("email")

            # Enregistrement dans la table Particulier
            Particulier.objects.create(
                civilite=civilite,
                nom=nom,
                prenom=prenom,
                numero=numero_particulier,
                email=email,
                ville=ville,
                localisation=localisation,
                nombre_vehicule=nombre_vehicule,
            )
        else:
            return JsonResponse({"error": "Statut invalide"}, status=400)

        # Redirection ou message de succès
        return JsonResponse({"success": "Les informations ont été enregistrées avec succès."})
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
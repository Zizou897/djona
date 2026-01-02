import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
import time
import uuid
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator



# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name if self.image else "Image sans fichier"
    
    


class CarouselImage(models.Model):
    image_url = models.ImageField(upload_to='carousel_images/')

    def __str__(self):
        return self.image_url.name



    
    
class Produit(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=64, editable=False, unique=True)

    # Relations
    images = models.ManyToManyField('Image', related_name='produits')

    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    annee = models.CharField(max_length=4)
    CARBURANT_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]
    carburant = models.CharField(max_length=50, choices=CARBURANT_CHOICES)
    type = models.CharField(max_length=255)
    kilometrage = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    TRANSMISSION_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('auto', 'Auto'),
    ]
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    description = models.TextField()
    ville = models.CharField(max_length=255)
    occasion_neuve = models.CharField(max_length=255, help_text="Indiquez si le véhicule est neuf ou d'occasion.")
    immatriculation = models.CharField(max_length=255, unique=True)
    nom_entreprise = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    
    moteur = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    place = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    couleur_interieur = models.CharField(max_length=255, default='No Color')
    couleur_exterieur = models.CharField(max_length=255, default='No Color')
    cylindre = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    puissance_fiscale = models.PositiveIntegerField(validators=[MinValueValidator(0)])  # Correction ici
    nbre_proprio = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    condition = models.CharField(max_length=255)

    prix_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    limite_assurance = models.DateField()
    date_ajout = models.DateTimeField(auto_now=True)

    statut = models.ForeignKey(
        'EtatVehicule',
        on_delete=models.CASCADE,
        related_name='produits'
    )
    
    is_published = models.BooleanField("Publié", default=True)

    # Méthodes
    def first_image_url(self):
        first_image = self.images.first()
        if first_image and hasattr(first_image, 'image') and first_image.image:
            return first_image.image.url
        return None

    first_image_url.short_description = 'Image'

    def image_count(self):
        return self.images.count()
    
    def whatsapp_message(self):
        occasion_neuve = "Neuve" if self.type.lower() == "neuve" else "Occasion"
        image_url = self.first_image_url() if self.first_image_url() else "Image non disponible"
        
        return (
            f"Bonjour, je suis intéressé par le véhicule\n"
            f"Marque: {self.marque}\n" 
            f"Modèle: {self.modele}\n" 
            f"Transmission: {self.transmission}\n"
            f"Prix: {self.prix} FCFA \n"
            f"Kilométrage: {self.kilometrage} km\n"
            f"Année: {self.annee}.\n"
            f"Image du produit: {image_url}\n"
            "Pouvez-vous m'en dire plus ?"
        )
        

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            unique_string = f"{uuid.uuid4()}"
            self.hashed_id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"
      


class EtatVehicule(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.nom


class LogoPartenaire(models.Model):
    image = models.ImageField(upload_to='Image/')
    nom = models.CharField(max_length=100)
    is_published = models.BooleanField("Publié", default=True)

    def __str__(self):
        return self.nom  
    

class Information(models.Model):
    description = models.TextField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.description  


class A_propos_de_nou(models.Model):
    titre = models.CharField("Titre", max_length=100)
    description = models.TextField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre  
    

class Nos_service(models.Model):
    svg_code = models.TextField("Code SVG", help_text="Collez le code SVG ici")
    titre = models.CharField("Titre", max_length=100)
    description = models.TextField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre  
    

class Service_Adapte(models.Model):
    svg_code = models.TextField("Code SVG", help_text="Collez le code SVG ici")
    titre = models.CharField("Titre", max_length=100)
    description = models.TextField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre  


class Valeur(models.Model):
    svg_code = models.TextField("Code SVG", help_text="Collez le code SVG ici")
    title = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)
    is_published = models.BooleanField("Publié", default=True)

    def __str__(self):
        return self.title
    
    
class Fidelisation(models.Model):
    svg_code = models.TextField("Code SVG", help_text="Collez le code SVG ici")
    title = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)
    is_published = models.BooleanField("Publié", default=True)

    def __str__(self):
        return self.title
    
 


class Config_Site(models.Model):
    nom = models.CharField(max_length=255)
    couleur = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Image/')
    is_published = models.BooleanField("Publié", default=True)

    def __str__(self):
        return self.nom
    


class PieceDetache(models.Model):
    id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to='pieces_detachees/')
    nom = models.CharField(max_length=255, verbose_name="Nom de la pièce")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    prix_normal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix normal")
    prix_reduit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix réduit") 
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Pièce détachée"
        verbose_name_plural = "Pièces détachées"

    def __str__(self):
        return self.nom


class ClientInformation(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero = models.CharField(max_length=15)
    ville = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.marque} {self.modele}"


class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_expired(self):
        from django.utils.timezone import now
        return now() > self.expires_at




class Concessionnaire(models.Model):
    civilite = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nom_entreprise = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    email = models.EmailField()
    ville = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    nombre_vehicule = models.IntegerField()
    
    def __str__(self):
        return self.nom
    
    

class Particulier(models.Model):
    civilite = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    email = models.EmailField()
    ville = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    nombre_vehicule = models.IntegerField()
    
    def __str__(self):
        return self.nom
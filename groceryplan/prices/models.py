import datetime
from django.db import models
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from collections import defaultdict
from django.template.defaultfilters import slugify
from decimal import Decimal

CONVENTIONAL = 'CON'
ORGANIC = 'ORG'
LOW_SPRAY = 'LOW'
CHEMICAL_FREE = 'CMF'

PRODUCTION_CHOICES = (
    (CONVENTIONAL, 'Conventional'),
    (ORGANIC, 'Organic'),
    (LOW_SPRAY, 'Low Spray'),
    (CHEMICAL_FREE, 'Chemical Free')
)

# Generate dictionary PC from tuple PRODUCTION_CHOICES.

PC = {}
for v, k in PRODUCTION_CHOICES:
    PC[v] = k

CANNED = 'CAN'
FROZEN = 'FRO'
PRODUCE = 'PRO'
CLEANING = 'CLE'
GROCERY = 'GRO'    
SECTION_CHOICES = (
    (CANNED, 'Canned'),
    (FROZEN, 'Frozen'),
    (PRODUCE, 'Produce'),
    (CLEANING, 'Cleaning'),
    (GROCERY, 'Grocery')        
)

LOCAL = 'LOC'
FAIR_TRADE = 'FAT'
NO_PRESERVATIVES = 'NOP'
FEATURE_CHOICES = (
    (LOCAL, 'Local'),
    (FAIR_TRADE, 'Fair Trade'),
    (NO_PRESERVATIVES, 'No Preservatives')        
)

FLUID_OZ = 'FOZ'
FLUID_LITER = 'LIT'
WEIGHT_OZ = 'WOZ'
WEIGHT_LBS = 'LBS'
UNIT_CHOICES = (
    (FLUID_OZ, 'fl. oz.'),
    (FLUID_LITER, 'lit'),
    (WEIGHT_OZ, 'oz.'),
    (WEIGHT_LBS, 'lbs'),
)

UNIT_CONVERSIONS = {
    (FLUID_OZ, FLUID_LITER): 0.0295735,
    (FLUID_LITER, FLUID_OZ): 33.814,
    (WEIGHT_OZ, WEIGHT_LBS): 0.0625,
    (WEIGHT_LBS, WEIGHT_OZ): 16
}

class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    
    def __unicode__(self):

        return self.name    


class Feature(models.Model):
    name = models.CharField(max_length=200)


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    section = models.CharField(max_length=3, choices=SECTION_CHOICES)   

    def __unicode__(self):

        return self.name


class Product(models.Model):
    name = models.ForeignKey(Food, to_field='slug')
    store = models.ForeignKey(Store)        
    date = models.DateTimeField(auto_now_add=True)    
    price = models.DecimalField(decimal_places=2, max_digits=6)    
    amount = models.DecimalField(decimal_places=2, max_digits=6)      
    unit = models.CharField(max_length=3,
                                      choices=UNIT_CHOICES)        
    production = models.CharField(max_length=3,
                                      choices=PRODUCTION_CHOICES)
    ppo = models.DecimalField(decimal_places=4, max_digits=6, editable=False)
    extras = models.ManyToManyField(Feature, blank=True, null=True)    

    class Meta:
        ordering = ["-name"]    

    def isOz( self, unit ):
        if unit == "WOZ" or unit == "FOZ":
            return True

    def isVolumeorWeight( self, unit ):
        if unit == "LIT" or unit == "FOZ":
            return "V"
        elif unit == "LBS" or "WOZ":
            return "W"

    def toOz( self, price, amount, unit ):
        if self.isOz(unit): 
            return price / amount
        elif self.isVolumeorWeight(unit) == "V":
            return float(price) / (float(amount) * UNIT_CONVERSIONS[(unit, FLUID_OZ)])
        elif self.isVolumeorWeight(unit) == "W":
            return float(price) / (float(amount) * UNIT_CONVERSIONS[(unit, WEIGHT_OZ)])

    def save(self, *args, **kwargs):
        unit = self.toOz(self.price, self.amount, self.unit)
        self.ppo = unit
        super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s at %s" % (PC[self.production], self.name.name, self.store.name)
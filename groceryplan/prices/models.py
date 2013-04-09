from django.db import models

CONVENTIONAL = 'CON'
ORGANIC = 'ORG'
#LOW_SPRAY = 'LOW'
#CHEMICAL_FREE = 'CMF'

PRODUCTION_CHOICES = (
    (CONVENTIONAL, 'Conven.'),
    (ORGANIC, 'Organic')
    #(LOW_SPRAY, 'Low Spray'),
    #(CHEMICAL_FREE, 'Chemical Free')
)

# Generate dictionary PC from tuple PRODUCTION_CHOICES.

PC = {}
for v, k in PRODUCTION_CHOICES:
    PC[v] = k

CANNED = 'CAN'
DRY = 'DRY'
PRODUCE = 'PRO'
MISC = 'MIS'
COOKING = 'COO'
REFRIGERATED = 'REF'
SECTION_CHOICES = (
    (CANNED, 'Cans & Jars'),
    (DRY, 'Dry/Baking'),
    (PRODUCE, 'Produce'),
    (MISC, 'Miscellaneous'),
    (COOKING, 'Cooking'),
    (REFRIGERATED, 'Refrigerated')
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
    (FLUID_OZ, 'fl oz'),
    (FLUID_LITER, 'lit'),
    (WEIGHT_OZ, 'oz'),
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

    def __unicode__(self):

        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    section = models.CharField(max_length=3, choices=SECTION_CHOICES)

    class Meta:
        ordering = ["name"]

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
    ppo = models.DecimalField(decimal_places=2, max_digits=6, editable=False)
    extras = models.ManyToManyField(Feature, blank=True, null=True)

    class Meta:
        ordering = ["-production", "ppo"]

    def is_oz(self, unit):
        if unit == "WOZ" or unit == "FOZ":
            return True

    def is_volume_or_weight(self, unit):
        if unit == "LIT" or unit == "FOZ":
            return "V"
        elif unit == "LBS" or "WOZ":
            return "W"

    def to_oz(self):
        if self.is_oz(self.unit):
            return float(self.price) / float(self.amount)
        elif self.is_volume_or_weight(self.unit) == "V":
            return float(self.price) / (float(self.amount) * UNIT_CONVERSIONS[(self.unit, FLUID_OZ)])
        elif self.is_volume_or_weight(self.unit) == "W":
            return float(self.price) / (float(self.amount) * UNIT_CONVERSIONS[(self.unit, WEIGHT_OZ)])

    def save(self, *args, **kwargs):
        unit = self.to_oz()
        self.ppo = unit
        super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s at %s" % (PC[self.production],
                                self.name.name, self.store.name)

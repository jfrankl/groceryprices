from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)


class Choice(models.Model):

    food = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2)      
    price = models.DecimalField(decimal_places=2)    

    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)


    date_added = models.DateTimeField('date published')    

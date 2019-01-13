from django.db import models

class Survivor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    infected = models.BooleanField(default=False)
    

class LastLocation(models.Model):
    survivor = models.OneToOneField('Survivor',on_delete="CASCATE",default = None,null = True, related_name="last_location")
    latitude = models.DecimalField(decimal_places=15,max_digits=20)
    longitude = models.DecimalField(decimal_places=15,max_digits=20)

class Item(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="inventory")
    ITEMS_TYPE_CHOICES = (
        (4, 'Water'),
        (3, 'Food'),
        (2, 'Medication'),
        (1, 'Ammunition'),
    )
    item_type = models.CharField(
        max_length = 15,
        choices=ITEMS_TYPE_CHOICES,
        default=0,
    )


    

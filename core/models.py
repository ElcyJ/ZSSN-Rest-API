from django.db import models
from datetime import datetime

class Survivor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    infected = models.BooleanField(default=False)

    @property
    def infected_flags(self):
        return len(self.flag_counter.all())

    def __str__(self):
        return self.name + " - " + str(self.age) + "years"

class LastLocation(models.Model):
    survivor = models.OneToOneField(Survivor, on_delete="CASCATE", related_name="last_location")
    longitude = models.FloatField()
    latitude = models.FloatField()

class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="inventory", null=False, blank=True)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)

    @property
    def value(self):
        return self.water*4 + self.food*3 + self.medication*2 + self.ammunition

class FlagSurivor(models.Model):
    target = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="flag_counter")
    author = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="flagging_counter")
    date = models.DateTimeField(default=datetime.now, blank=True)

    def save(self):
        if (self.target != self.author):
            flags = FlagSurivor.objects.filter(author = self.author, target = self.target).all()
            if (len(flags)<=0):
                super().save()
            if(self.target.infected_flags >= 3):
                self.target.infected = True
                self.target.save()

    def __str__(self):
        return self.author.name + "flagged" + self.target.name + str(self.date)



    

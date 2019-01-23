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
    survivor = models.OneToOneField(Survivor, on_delete="CASCATE", null=True, related_name="last_location")
    longitude = models.FloatField()
    latitude = models.FloatField()

class Inventory(models.Model):
    survivor = models.OneToOneField(Survivor, on_delete="CASCATE", related_name="inventory", null=False, blank=True)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)

    @property
    def value(self):
        return self.water*4 + self.food*3 + self.medication*2 + self.ammunition

class FlagSurvivor(models.Model):
    target = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="flag_counter")
    author = models.ForeignKey(Survivor, on_delete="CASCATE", related_name="flagging_counter")
    date = models.DateTimeField(default=datetime.now, blank=True)

    def save(self):
        if(self.target != self.author):
            flags = FlagSurvivor.objects.filter(author = self.author, target = self.target).all()
            if (len(flags)<=0):
                super().save()
            if(self.target.infected_flags >= 3):
                self.target.infected = True
                self.target.save()

    def __str__(self):
        return self.author.name + "flagged" + self.target.name + str(self.date)

class Util():
    def generate_infected_report():
         
        survivors = Survivor.objects.all()
        survivors_infected = Survivor.objects.filter(infected = True)
        report = {"description":"Percentage of infected survivors.","value": (100.0 /float(len(survivors))) * float(len(survivors_infected))}
        
        return report
    
    def generate_non_infected_report():
         
        survivors = Survivor.objects.all()
        survivors_non_infected = Survivor.objects.filter(infected = False)
        report = {"description":"Percentage of non-infected survivors.","value": (100/float(len(survivors))) * float(len(survivors_non_infected))}

        return report
    
    def generate_resource_report():

        survivors = Survivor.objects.filter(infected = False).all()
        inventorys = []
        for s in survivors:
            try:
                inventorys.append(s.inventory)
            except:
                pass
                            
        water = 0
        food = 0
        med = 0
        ammo = 0
         
        for item in inventorys:
            water += item.water
            food += item.food
            med += item.medication
            ammo += item.ammunition
        
        report = {
            "description":"Average amount of each kind of resource by survivor",
            "values":{
                "water_per_survivor": float(water)/float(len(survivors)),
                "food_per_survivor": float(food)/float(len(survivors)),
                "medication_per_survivor": float(med)/float(len(survivors)),
                "ammunition_per_survivor": float(ammo)/float(len(survivors))
            }
        }

        return report
    
    def generate_infected_lost_points_report():

        survivors_infected = Survivor.objects.filter(infected = True)
        points = 0
        for survivor in survivors_infected:
            try:
                points += survivor.inventory.value
            except:
                pass
                
        
        report = {"description":"Points lost because of infected survivor","value": points}
         
        return report




    

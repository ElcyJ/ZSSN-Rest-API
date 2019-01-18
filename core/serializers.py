from .models import *
from .serializers import *
from rest_framework import serializers

"""
class LastLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LastLocation
        fields = ('url','latitude', 'longitude', 'survivor')
"""
        
class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'item_type', 'quantity', 'survivor')

class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = ItemSerializer(many=True)
    # last_location = LastLocationSerializer()

    class Meta:
        model = Survivor
        fields = ('url', 'name', 'age', 'gender','latitude', 'longitude','inventory', 'infected', 'infected_counter')


    def create(self, validated_data):
        survivor = Survivor()
        survivor.name = validated_data["name"]
        survivor.age = validated_data["age"]
        survivor.gender = validated_data["gender"]
        survivor.latitude = validated_data["latitude"]
        survivor.longitude = validated_data["longitude"]
        survivor.infected = validated_data["infected"]
        survivor.infected_counter = validated_data["infected_counter"]
        survivor.save()
      
        for i in validated_data["inventory"]:
            item = Item()
            item.item_type = i["item_type"]
            item.quantity = i["quantity"]
            item.survivor = survivor
            item.save()
        survivor.save()

        return survivor
        
    '''
    def validate_inventory(self, value):
        return value'''



class SurvivorLastLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survivor
        fields = ('longitude', 'latitude')


class SurvivorFlagSurvivorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survivor
        fields = ('flag_survivor')


"""
class UpdateLocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Survivor
        fields = ('url', 'last_location')

    def update(self, instance, validated_data):
        instance.last_location.latitude = validated_data["last_location"]["latitude"]
        instance.last_location.longitude = validated_data["last_location"]["longitude"]
        instance.last_location.save()
"""

    
    
    

  


    
        





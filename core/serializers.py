from .models import *
from .serializers import *
from rest_framework import serializers

class LastLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LastLocation
        fields = ('url','latitude', 'longitude')
        
class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'item_type')

class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = ItemSerializer(many=True)
    last_location = LastLocationSerializer()

    class Meta:
        model = Survivor
        fields = ('url', 'name', 'age', 'gender', 'infected','inventory','last_location')

    def create(self, validated_data):
        survivor = Survivor()
        survivor.name = validated_data["name"]
        survivor.age = validated_data["age"]
        survivor.gender = validated_data["gender"]
        survivor.infected = validated_data["infected"]
        survivor.save()

        last_location = LastLocation(latitude=validated_data["last_location"]["latitude"],longitude=validated_data["last_location"]["longitude"])
        last_location.survivor = survivor
        last_location.save() 
      

        for i in validated_data["inventory"]:
            item = Item()
            item.item_type = i["item_type"]
            item.survivor = survivor
            item.save()
        survivor.save()

        return survivor
        





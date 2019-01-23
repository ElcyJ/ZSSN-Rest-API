from .models import *
from rest_framework import serializers


class LastLocationSerializer(serializers.Serializer):
    survivor_id = serializers.IntegerField()
    latitude = serializers.DecimalField(max_digits=20, decimal_places=10)
    longitude = serializers.DecimalField(max_digits=20, decimal_places=10)

class LastLocationSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = LastLocation
        fields = ('latitude', 'longitude')
        extra_kwargs = {'survivor': {'read_only' : True}}

class InventorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Inventory
        fields = ('url', 'survivor', 'water', 'food', 'medication', 'ammunition', 'value')
        extra_kwargs = {'value': {'read_only' : True}, 'survivor': {'read_only' : True}}

class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = InventorySerializer(many=False)
    last_location = LastLocationSerializerModel(many=False)

    class Meta:
        model = Survivor
        fields = ('url', 'name', 'age', 'gender', 'inventory', 'infected', 'infected_flags', 'last_location')
        extra_kwargs = {'flag_counter':{'read_only' : True}, 'infected': {'read_only' : True} }

    def create(self, validated_data):
        survivor = Survivor()
        survivor.name = validated_data["name"]
        survivor.age = validated_data["age"]
        survivor.gender = validated_data["gender"]
        survivor.save()
        last_location = LastLocation()
        last_location.survivor = survivor
        last_location.latitude = validated_data["last_location"]["latitude"] 
        last_location.longitude = validated_data["last_location"]["longitude"]
        last_location.save()
        
        inventory = Inventory()
        inventory.water = validated_data["inventory"]["water"]
        inventory.food = validated_data["inventory"]["food"]
        inventory.medication = validated_data["inventory"]["medication"]
        inventory.ammunition = validated_data["inventory"]["ammunition"]
        inventory.survivor = survivor
        inventory.save()
 
        return survivor

class FlagSurvivorSerializer(serializers.Serializer):
    target_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

class TradeSerializer(serializers.Serializer):
    sendder_id = serializers.IntegerField()
    reciever_id = serializers.IntegerField()
    send_water = serializers.IntegerField()
    send_food = serializers.IntegerField()
    send_medication = serializers.IntegerField()
    send_ammunition = serializers.IntegerField()
    recieve_water = serializers.IntegerField()
    recieve_food = serializers.IntegerField()
    recieve_medication = serializers.IntegerField()
    recieve_ammunition = serializers.IntegerField()



    
    
    

  


    
        





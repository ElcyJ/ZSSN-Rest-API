from django.shortcuts import render
from .models import Survivor, Inventory
from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


class SurvivorView(viewsets.ModelViewSet):

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer


class InventoryView(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class LastLocationView(viewsets.ModelViewSet):
    serializer_class = LastLocationSerializer

    def get_queryset(self):
        return None

    def list(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, pk=None):
        last_location_serializer = LastLocationSerializer(data=request.data)
        if last_location_serializer.is_valid():
            try:
                survivor = Survivor.objects.get(pk = last_location_serializer.data['survivor_id'])
                if(survivor):
                    last_location = LastLocation()
                    last_location.latitude = last_location_serializer.data['latitude']
                    last_location.longitude = last_location_serializer.data['longitude']
                    last_location.survivor = survivor
                    last_location.save()
                    return Response({'status': 'location_updated'})
            except:
                return Response({'error':'survivor not found'},
                    status=status.HTTP_400_BAD_REQUEST)
            
          
        return Response(last_location_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class FlagSurvivorView(viewsets.ModelViewSet):
    serializer_class = FlagSurvivorSerializer

    def get_queryset(self):
        return  FlagSurvivor.objects.all()

    def create(self, request, pk=None):
        flag_serializer = FlagSurvivorSerializer(data=request.data)
        if flag_serializer.is_valid():
            try:
                target = Survivor.objects.get(pk = flag_serializer.data['target_id'])
                author = Survivor.objects.get(pk = flag_serializer.data['author_id'])              
                flag = FlagSurvivor()
                flag.target = target
                flag.author = author
                flag.save()
                return Response({'status': 'survivor flagged as infected successfuly'})
            except:
                return Response({'error':'survivor not found'},
                    status=status.HTTP_400_BAD_REQUEST)

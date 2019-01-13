from django.shortcuts import render
from .models import Survivor, Item, LastLocation
from rest_framework import viewsets
from .serializers import SurvivorSerializer, ItemSerializer, LastLocationSerializer


class SurvivorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Survivor.objects.all()# .order_by('-date_joined')
    serializer_class = SurvivorSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class LastLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LastLocation.objects.all()
    serializer_class = LastLocationSerializer
from django.shortcuts import render
from .models import Survivor, Item
from rest_framework import viewsets
from .serializers import SurvivorSerializer, ItemSerializer, SurvivorLastLocationSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


class SurvivorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Survivor.objects.all()# .order_by('-date_joined')
    serializer_class = SurvivorSerializer

    """@csrf_exempt
    def survivor_update(self, request, pk):

            survivor = Survivor.objects.get(pk=pk)

            if request.method == 'PUT':
                data = JSONParser().parse(request)
                serializer = SurvivorLastLocationSerializer(survivor, data=data)

            if serializer.is_valid():
                serializer.save()
                s_serializer = SurvivorSerializer(survivor)

                return JsonResponse(s_serializer.data, status=200)

            return JsonResponse(serializer.errors, status=400)"""


class ItemViewSet(viewsets.ModelViewSet):
    
   
    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
"""
class LastLocationViewSet(viewsets.ModelViewSet):
    
    queryset = LastLocation.objects.all()
    serializer_class = LastLocationSerializer
"""

@api_view(['GET', 'PUT'])
def location_detail(request, pk, format=None):
    
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SurvivorLastLocationSerializer(survivor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SurvivorLastLocationSerializer(survivor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

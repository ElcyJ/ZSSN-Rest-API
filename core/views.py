from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *

from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


class SurvivorView(viewsets.ModelViewSet):

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    def update(self, request, pk):
        return Response({"Error":"Not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class InventoryView(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (ReadOnly,)

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

class TradeView(viewsets.ModelViewSet):
    serializer_class = TradeSerializer

    def get_queryset(self):
        return None
    
    def list(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, pk=None):
        trade_serializer = TradeSerializer(data=request.data)
        if trade_serializer.is_valid():
            sendder_trade_value = (int(trade_serializer.data['send_water']) * 4 +
                                  int(trade_serializer.data['send_food']) * 3 +
                                  int(trade_serializer.data['send_medication']) * 2 +
                                  int(trade_serializer.data['send_ammunition']) * 1)

            reciever_trade_value = (int(trade_serializer.data['recieve_water']) * 4 +
                                   int(trade_serializer.data['recieve_food']) * 3 +
                                   int(trade_serializer.data['recieve_medication']) * 2 +
                                   int(trade_serializer.data['recieve_ammunition']) * 1)

            if(sendder_trade_value == reciever_trade_value):
                if(not Survivor.objects.get(pk = trade_serializer.data['sendder_id']).infected and not Survivor.objects.get(pk = trade_serializer.data['reciever_id']).infected):
                    try:
                       
                        sendder_inventory = Survivor.objects.get(pk = trade_serializer.data['sendder_id']).inventory
                        reciever_inventory = Survivor.objects.get(pk = trade_serializer.data['reciever_id']).inventory            
                        
                        sendder_inventory.water -= trade_serializer.data['send_water']
                        sendder_inventory.food -= trade_serializer.data['send_food']
                        sendder_inventory.medication -= trade_serializer.data['send_medication']
                        sendder_inventory.ammunition -= trade_serializer.data['send_ammunition']
                        
                        sendder_has_itens = sendder_inventory.water >= 0 and sendder_inventory.food >= 0 and sendder_inventory.medication >= 0 and sendder_inventory.ammunition >= 0

                        reciever_inventory.water -= trade_serializer.data['recieve_water']
                        reciever_inventory.food -= trade_serializer.data['recieve_food']
                        reciever_inventory.medication -= trade_serializer.data['recieve_medication']
                        reciever_inventory.ammunition -= trade_serializer.data['recieve_ammunition']
                        
                        reciever_has_itens = reciever_inventory.water >= 0 and reciever_inventory.food >= 0 and reciever_inventory.medication >= 0 and reciever_inventory.ammunition >= 0
                        print('COnferencia dos itens')
                        if(reciever_has_itens and sendder_has_itens):

                            reciever_inventory.water += trade_serializer.data['send_water']
                            reciever_inventory.food += trade_serializer.data['send_food']
                            reciever_inventory.medication += trade_serializer.data['send_medication']
                            reciever_inventory.ammunition += trade_serializer.data['send_ammunition']
                    
                            sendder_inventory.water += trade_serializer.data['recieve_water']
                            sendder_inventory.food += trade_serializer.data['recieve_food']
                            sendder_inventory.medication += trade_serializer.data['recieve_medication']
                            sendder_inventory.ammunition += trade_serializer.data['recieve_ammunition']
                            
                            sendder_inventory.save()
                            reciever_inventory.save()
                            return Response({'status': 'The trade was successful'})
                        else:
                            return Response({'error': 'One of the tradding survivors does not have the itens to trade'})
                    except:
                        return Response({'error':'survivor not found'},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error':'There is a infected almost dead person in this transaction! God is looking!'},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'The total value of the traded itens does not match!'},
                    status=status.HTTP_400_BAD_REQUEST) 
           
        
          
        return Response(trade_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class ReportView(viewsets.ViewSet):
    def list(self, request):
        reports = []
        reports.append(Util.generate_infected_report())
        reports.append(Util.generate_non_infected_report())
        reports.append(Util.generate_resource_report())
        reports.append(Util.generate_infected_lost_points_report())

        return Response(reports)

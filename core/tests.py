from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *

class SurvivorTests(APITestCase):

    def setUp(self):
        s = Survivor(name="Survivor01", age=18, gender="F")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll
        s.inventory = i
        s.save()
        s = Survivor(name="Survivor02", age=20, gender="F")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll 
        s.inventory = i
        s.save()
        s = Survivor(name="Survivor03", age=25, gender="M")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll 
        s.inventory = i
        s.save()
        s = Survivor(name="Survivor04", age=29, gender="M")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll 
        s.inventory = i
        s.save()
        
       
  
    def test_create_survivor(self):
        url = reverse('survivor-list')
        data = {"name": "Survivor05",
                "age": 45,
                "gender": "M",
                "inventory": {
                    "water": 1,
                    "food": 1,
                    "medication": 1,
                    "ammunition": 1
                },
                 "last_location": {
                    "latitude": 123213.456456,
                    "longitude": -567567.123123
                }
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survivor.objects.count(), 5)
        self.assertEqual(Survivor.objects.get(id=5).name, 'Survivor05')
        self.assertEqual(Survivor.objects.get(id=5).last_location.latitude, 123213.456456)


    
    def test_create_survivor_without_inventory(self):
        url = reverse('survivor-list')
        data = {"name": "Survivor04",
                "age": 45,
                "gender": "M",
                "latitude": 123213.456456,
                "longitude": -567567.123123,
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_survivor_last_location(self):
        url = reverse('survivor_last_location-list')
        data = {"survivor_id": 3,
                "latitude": 2222222.45555555,
                "longitude": -3444445555.78888888
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survivor.objects.get(id=3).last_location.latitude, 2222222.45555555)
        self.assertEqual(Survivor.objects.get(id=3).last_location.longitude, -3444445555.78888888)
    
    def test_flag_survivor_infected(self):
        url = reverse('flag_survivor-list')
        data = {"target_id": 1,
                "author_id": 2
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_triple_flag_survivor_infected(self):
        url = reverse('flag_survivor-list')
        data = {"target_id": 1,
                "author_id": 2
                }
        response = self.client.post(url, data, format='json')
        data = {"target_id": 1,
                "author_id": 3
                }
        response = self.client.post(url, data, format='json')
        data = {"target_id": 1,
                "author_id": 4
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(Survivor.objects.get(id=1).infected, True)

class InventoryTests(APITestCase):

    def setUp(self):
        s = Survivor(name="Survivor01", age=18, gender="F")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll
        s.save()
        i.survivor = s
        i.save()
        s = Survivor(name="Survivor02", age=18, gender="M")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll
        s.save()
        i.survivor = s
        i.save()
        s = Survivor(name="Survivor03", age=18, gender="M")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll
        s.save()
        i.survivor = s
        i.save()
        s = Survivor(name="Survivor04", age=18, gender="M")
        i = Inventory(water = 1, food = 2, medication = 3, ammunition = 4)
        ll = LastLocation(latitude = 112312.12312, longitude = 123123.12321321) 
        s.last_location = ll
        s.save()
        i.survivor = s
        i.save()
  
        
    def test_change_inventory(self):
        url = reverse('inventory-list')
        data = {
                    "water": 2,
                    "food": 2,
                    "medication": 1,
                    "ammunition": 1
                }
        response = self.client.put(url+"1/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trade_items(self):
        url = reverse('trade-list')
        data = {
            "sendder_id": 1,
            "reciever_id": 2,
            "send_water": 1,
            "send_food": 0,
            "send_medication": 0,
            "send_ammunition": 0,
            "recieve_water": 0,
            "recieve_food": 0,
            "recieve_medication": 0,
            "recieve_ammunition": 4
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trade_infected(self):
        url = reverse('flag_survivor-list')
        data = {"target_id": 1,
                "author_id": 2
                }
        response = self.client.post(url, data, format='json')
        data = {"target_id": 1,
                "author_id": 3
                }
        response = self.client.post(url, data, format='json')
        data = {"target_id": 1,
                "author_id": 4
                }
        response = self.client.post(url, data, format='json')

        url = reverse('trade-list')
        data = {
            "sendder_id": 1,
            "reciever_id": 2,
            "send_water": 1,
            "send_food": 0,
            "send_medication": 0,
            "send_ammunition": 0,
            "recieve_water": 0,
            "recieve_food": 0,
            "recieve_medication": 0,
            "recieve_ammunition": 4
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
   



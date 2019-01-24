# ZSSN-Rest-API

Even at an zombie apocalipse, it is important to keep track of what's happening.
With ZSSN you can trade fairly resources betwen survivors. 
Keep track of the last location of your fellow survivors.
Be aware of infected people.
Have a overview of the situation of humanity trough ZSSN reports.

## Used tecnologies:

* Python 3.7
* Django (https://www.djangoproject.com/download/)
* DjangoRestFramework (https://www.django-rest-framework.org/)

## How to run the project

1. Create a virtual environment to run and install the projects dependencies(https://virtualenv.pypa.io/en/latest/installation/)
2. Activate the virtual envioriment
3. Clone de project into the destined folder 
> git clone https://github.com/ElcyJ/ZSSN-Rest-API.git
4. Inside the projects root folder "ZSSN" install the dependencies using:
> pip install -r requirements.txt
5. to run te project at http://localhost:8000 use:
> python manage.py runserver
6. Now the project is runing and you can make requests to it.
7. On the browser if you access http://localhost:8000 you will have access to a API interface provided by the DRF.

## How to consume this API

### Enpoints:

* **Survivors** - http://localhost:8000/survivors/
> * Register survivors with an inventory
> * You cannot change the inventory later, only through trades.
* **Inventory** - http://localhost:8000/inventory/
> * Can see stored inventories
> * Can not change any inventory.
* **Trade** - http://localhost:8000/trade/
> You may trade your resources with other survivors as long as is a equivalent trade. 
* **Reports** - http://localhost:8000/reports/
> * Percentage of infected survivors.
> * Percentage of non-infected survivors.
> * Average amount of each kind of resource by survivor.
> * Points lost because of infected survivor.
* **Flag_survivor** - http://localhost:8000/flag_survivor/,
> * Flag a survivor as infected
> * After 3 flags the survivor will be considered infected.
* **Survivor_last_location** - http://localhost:8000/survivor_last_location/
> * Change a survivors last location


### Survivors
#### Allowed methods = [GET][POST]
[GET]http://localhost:8000/survivors/
[GET]http://localhost:8000/survivors/{id}
Sample response:
```json
[
    {
        "url": "http://localhost:8000/survivors/1/",
        "name": "Elcy James",
        "age": 20,
        "gender": "F",
        "inventory": {
            "url": "http://localhost:8000/inventory/5/",
            "survivor": "http://localhost:8000/survivors/9/",
            "water": 3,
            "food": 2,
            "medication": 5,
            "ammunition": 1,
            "value": 29
        },
        "infected_flags": 3,
        "infected": true,
        "last_location": {
            "latitude": 12312.123123,
            "longitude": 123123.123123
        }
    }
]

```
[POST]http://localhost:8000/survivors/{id}
```json
data = {
    "name": "Survivor",
    "age": 14,
    "gender": "F",
    "inventory": {
        "water": 2,
        "food": 1,
        "medication": 2,
        "ammunition": 2
    },
    "last_location": {
        "latitude": 1234567.123345,
        "longitude": 1234567.123345
    }
}
```
### Inventory
#### Allowed methods = [GET]
[GET]http://localhost:8000/inventory/
[GET]http://localhost:8000/inventory/{id}
Sample response:
```json

[
    {
        "url": "http://localhost:8000/inventory/1/",
        "survivor": "http://localhost:8000/survivors/5/",
        "water": 3,
        "food": 2,
        "medication": 1,
        "ammunition": 0,
        "value": 20
    }
]

```
### Trade
#### Allowed methods = [POST]
[POST]http://localhost:8000/trade/
Sample request:
```json

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
    "recieve_ammunition": 1
}
```
### Reports
#### Allowed methods = [GET]
[GET]http://localhost:8000/reports/
Sample response:
```json
[
    {
        "description": "Percentage of infected survivors.",
        "value": 33.33333333333333
    },
    {
        "description": "Percentage of non-infected survivors.",
        "value": 66.66666666666666
    },
    {
        "description": "Average amount of each kind of resource by survivor",
        "values": {
            "water_per_survivor": 1.3333333333333333,
            "food_per_survivor": 1.0,
            "medication_per_survivor": 1.6666666666666667,
            "ammunition_per_survivor": 0.5
        }
    },
    {
        "description": "Points lost because of infected survivor",
        "value": 20
    }
]
```
### Flag_survivor
#### Allowed methods = [GET,POST]
[GET]http://localhost:8000/flag_survivor/
Sample response:
```json
[
    {
        "target_id": 1,
        "author_id": 2
    },
    {
        "target_id": 1,
        "author_id": 3
    }
]
```
[POST]http://localhost:8000/flag_survivor/
Sample request:
```json

data = {
    "target_id": 1,
    "author_id": 2
}
```
### Survivor_last_location
#### Allowed methods = [POST]
[POST]http://localhost:8000/survivor_last_location/
Sample request:
```json

data = {
    "survivor_id": null,
    "latitude": null,
    "longitude": null
}
```

## Testing

### How to test

Were created 9 automated tests to check if the API is working properly.
To test this api run do the following:

1. Activate your virtual enviorment
2. In the folder ZSSN run the following command:
> python mange.py test core.tests
3. See the result of the test and check if the final result was **OK**

## I am not NEGAN!

Any question reach out to the following e-mail:
* elcy_james@hotmail.com

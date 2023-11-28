from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential
import random

from celery import shared_task

# DefaultAzureCredential supports different authentication mechanisms and determines the appropriate credential type based of the environment it is executing in.
# It attempts to use multiple credential types in an order until it finds a working credential.

# - AZURE_URL: The URL to the ADT in Azure
url = "https://IoT-1.api.wcus.digitaltwins.azure.net"

# DefaultAzureCredential expects the following three environment variables:
# - AZURE_TENANT_ID: The tenant ID in Azure Active Directory
# - AZURE_CLIENT_ID: The application (client) ID registered in the AAD tenant
# - AZURE_CLIENT_SECRET: The client secret for the registered application
credential = DefaultAzureCredential()
service_client = DigitalTwinsClient(url, credential)


@shared_task
def start_sim_park():
    query_expression = 'SELECT * FROM digitaltwins'
    query_result = service_client.query_twins(query_expression)
    # print('DigitalTwins:')
    random_number = random.randint(1, 20)
    number_of_cars = []
    # print("Random Number:", random_number)
    spotStatus = ['Reserved', 'Occupied', 'Vacant']
    carType = ['EV', 'ICE']
    vacant = []
    reserved = []
    occupied = []
    incompatible = []
    digital_twin_id = 'ParkingCar'
    patch = [{
        "op": "replace",
        "path": "/isEv",
        "value": random.choice(list(carType))
    }
    ]

    updated_twin = service_client.update_digital_twin(digital_twin_id, patch)
    # print('Updated Digital Twin')
    for i in range(1, 11):
        digital_twin_id = f'ParkingSpot{i}'
        patch = [{
            "op": "replace",
            "path": "/status",
            "value": random.choice(list(spotStatus)),
        }
        ]

        updated_twin = service_client.update_digital_twin(digital_twin_id, patch)
        # print(f'Updated Digital Twin {i}:')
    get_twin = service_client.get_digital_twin('ParkingCar')
    # print(get_twin)
    for key, twin in enumerate(query_result):
        # print("hi")
        if "ParkingSpot" in twin["$dtId"]:
            if (get_twin["isEv"] == twin["Type"]):
                if (twin["status"] == "Vacant"):
                    vacant.append(twin)
                elif (twin["status"] == "Occupied"):
                    occupied.append(twin)
                elif (twin["status"] == "Reserved"):
                    reserved.append(twin)
            else:
                incompatible.append(twin)
    return {"vacant": vacant, "reserved": reserved, "occupied": occupied, "incompatible": incompatible}

import random

from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential
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


def simulate():
    query_expression = 'SELECT * FROM digitaltwins'
    query_result = service_client.query_twins(query_expression)
    # print('DigitalTwins:')
    random_number = random.randint(1, 20)
    number_of_cars = []
    # print("Random Number:", random_number)

    # delete all existing vehicle Twins
    for key, twin in enumerate(query_result):
        relationships = service_client.list_relationships(twin["$dtId"])
        # print(twin["$dtId"])
        for relationship in relationships:
            # print(relationship)
            service_client.delete_relationship(twin["$dtId"],
                                               relationship["$relationshipId"])  # print("Vehicle" in twin["$dtId"])
        if "Vehicle" in twin["$dtId"]:
            service_client.delete_digital_twin(twin["$dtId"])

    for i in range(1, random_number + 1):
        digital_twin_id = f'Vehicle{i}'
        temporary_twin = {"$metadata": {"$model": "dtmi:com:adt:dtsample:vehicle;1"}, "id": digital_twin_id,
                          "name": f"Vehicle {i}"}
        # create new vehicle twins
        service_client.upsert_digital_twin(digital_twin_id, temporary_twin)
        roads = ['RoadA', 'RoadB', 'RoadC']

        # associate vehicles to roads randomly
        random_road = random.choice(roads)
        # print("Random Road:", random_road)
        myRelationship = {"$relationshipId": f"RoadVehicle {i}", "$sourceId": random_road, "$relationshipName": "is_on",
                          "$targetId": f"Vehicle{i}"}
        # print(myRelationship)
        service_client.upsert_relationship(myRelationship["$sourceId"], myRelationship["$relationshipId"],
                                           myRelationship)

    # check number of vehicles on each road
    for road in roads:
        relationships = service_client.list_relationships(road)
        relationships_list = list(relationships)
        print("Number of Relationships:", len(relationships_list))
        number_of_cars.append(len(relationships_list))
    max_value = max(number_of_cars)
    max_indices = [i for i, value in enumerate(number_of_cars) if value == max_value]
    print(number_of_cars)
    if len(max_indices) > 1:
        selected_road = random.choice(max_indices)
        print(f"Traffic light for road {chr(ord('A') + selected_road)} has turned green")
    else:
        max_index = number_of_cars.index(max_value)
        print(f"Traffic light for road {chr(ord('A') + max_index)} has turned green")


# simulate()


@shared_task
def clear_data():
    query_expression = 'SELECT * FROM digitaltwins'
    query_result = service_client.query_twins(query_expression)
    # delete all existing vehicle Twins
    for key, twin in enumerate(query_result):
        relationships = service_client.list_relationships(twin["$dtId"])
        # print(twin["$dtId"])
        for relationship in relationships:
            # print(relationship)
            service_client.delete_relationship(twin["$dtId"],
                                               relationship["$relationshipId"])  # print("Vehicle" in twin["$dtId"])
        if "Vehicle" in twin["$dtId"]:
            service_client.delete_digital_twin(twin["$dtId"])
    return "cleared data"


@shared_task
def generate_data():
    random_number = random.randint(1, 20)
    for i in range(1, random_number + 1):
        digital_twin_id = f'Vehicle{i}'
        temporary_twin = {"$metadata": {"$model": "dtmi:com:adt:dtsample:vehicle;1"}, "id": digital_twin_id,
                          "name": f"Vehicle {i}"}
        # create new vehicle twins
        service_client.upsert_digital_twin(digital_twin_id, temporary_twin)
        roads = ['RoadA', 'RoadB', 'RoadC']

        # associate vehicles to roads randomly
        random_road = random.choice(roads)
        # print("Random Road:", random_road)
        myRelationship = {"$relationshipId": f"RoadVehicle {i}", "$sourceId": random_road, "$relationshipName": "is_on",
                          "$targetId": f"Vehicle{i}"}
        # print(myRelationship)
        service_client.upsert_relationship(myRelationship["$sourceId"], myRelationship["$relationshipId"],
                                           myRelationship)
        return "generated data"


@shared_task
def get_simulation_result():
    # check number of vehicles on each road
    number_of_cars = []
    roads = ['RoadA', 'RoadB', 'RoadC']
    for road in roads:
        relationships = service_client.list_relationships(road)
        relationships_list = list(relationships)
        print("Number of Relationships:", len(relationships_list))
        number_of_cars.append(len(relationships_list))
    max_value = max(number_of_cars)
    max_indices = [i for i, value in enumerate(number_of_cars) if value == max_value]
    print(number_of_cars)
    if len(max_indices) > 1:
        selected_road = random.choice(max_indices)
        print(f"Traffic light for road {chr(ord('A') + selected_road)} has turned green")
        return {"cars": number_of_cars, "open_lane": chr(ord('A') + selected_road)}
    else:
        max_index = number_of_cars.index(max_value)
        print(f"Traffic light for road {chr(ord('A') + max_index)} has turned green")
        return {"cars": number_of_cars, "open_lane": chr(ord('A') + max_index)}

# start_time = time.time()
# clear_data()
# end_time = time.time()
# print(f"Execution time: {end_time-start_time} seconds")
#
# start_time = time.time()
# generate_data()
# end_time = time.time()
# print(f"Execution time: {end_time-start_time} seconds")
#
# start_time = time.time()
# get_simulation_result()
# end_time = time.time()
# print(f"Execution time: {end_time-start_time} seconds")

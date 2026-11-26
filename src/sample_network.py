
from src.graph import RoadGraph


def create_sample_network():
    """
    Create a sample emergency response road network
    using locations around Dublin.
    """

    graph = RoadGraph()

    # Hospitals
    graph.add_location("Mater Hospital", (53.3590, -6.2643))
    graph.add_location("St James's Hospital", (53.3395, -6.2920))

    # Emergency service bases
    graph.add_location("Dublin Fire Brigade HQ", (53.3498, -6.2671))
    graph.add_location("Ambulance Base North", (53.3700, -6.2500))

    # Incident locations
    graph.add_location("Incident 1 - Smithfield", (53.3490, -6.2780))
    graph.add_location("Incident 2 - O'Connell Street", (53.3500, -6.2600))
    graph.add_location("Incident 3 - Rathmines", (53.3250, -6.2650))

    # Roads and estimated travel times (minutes)

    # Connections around the city centre
    graph.add_road("Mater Hospital", "Ambulance Base North", 6)
    graph.add_road("Mater Hospital", "Incident 2 - O'Connell Street", 5)
    graph.add_road("Mater Hospital", "Incident 1 - Smithfield", 8)

    # Connections around Smithfield
    graph.add_road("Dublin Fire Brigade HQ", "Incident 1 - Smithfield", 5)
    graph.add_road("Dublin Fire Brigade HQ", "Incident 2 - O'Connell Street", 7)

    # Southern Dublin connections
    graph.add_road("St James's Hospital", "Dublin Fire Brigade HQ", 8)
    graph.add_road("St James's Hospital", "Incident 3 - Rathmines", 7)
    graph.add_road("Incident 3 - Rathmines", "Incident 2 - O'Connell Street", 9)

    # Additional connections
    graph.add_road("Ambulance Base North", "Incident 2 - O'Connell Street", 6)
    graph.add_road("Ambulance Base North", "Incident 1 - Smithfield", 7)

    return graph


def create_sample_responders():
    """
    Define emergency responders and their starting locations.
    """

    responders = {
        "Ambulance 1": "Mater Hospital",
        "Ambulance 2": "St James's Hospital",
        "Fire Engine 1": "Dublin Fire Brigade HQ",
        "Ambulance 3": "Ambulance Base North"
    }

    return responders


def create_sample_incidents():
    """
    Define emergency incidents and their locations.
    """

    incidents = {
        "Incident 1": "Incident 1 - Smithfield",
        "Incident 2": "Incident 2 - O'Connell Street",
        "Incident 3": "Incident 3 - Rathmines"
    }

    return incidents

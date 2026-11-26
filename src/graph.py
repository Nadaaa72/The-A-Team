class RoadGraph:
    """
    Represents road network as a weighted graph.
    
    Locations are nodes and roads are edges.
    Edge weights represent estimated travel time in minutes
    """

    def __init__(self):
        self.adjacency = {}
        self.coordinates = {}

    def add_location(self, name, coordinates=None):
        # Add a location to road network

        if name not in self.adjacency:
            self.adjacency[name] = {}

        if coordinates is not None:
            self.coordinates[name] = coordinates

    def add_road(self, start, end, travel_time, bidirectional=True):
        """
        Add a road between two locations. 
        Travel time is measured in mins.
        Roads are bidirectional by default.
        """

        if travel_time < 0:
            raise ValueError("Travel time cannot be negative")

        self.add_location(start)
        self.add_location(end)

        self.adjacency[start][end] = travel_time

        if bidirectional:
            self.adjacency[end][start] = travel_time

    def get_neighbours(self, location):
        # Return all directly connected locations and their travel times.

        if location not in self.adjacency:
            raise ValueError(f"Unknown location {location}")

        return self.adjacency[location]    

    def get_travel_time(self, start, end):
        # Return the direct travel time between two connected locations

        if start not in self.adjacency:
            raise ValueError(f"Unknown location {start}")

        if end not in self.adjacency[start]:
            raise ValueError(f"No direct road between {start} and {end}")

        return self.adjacency[start][end]

    def get_coordinates(self, location):
        # Return the geographical coordinates of a location

        return self.coordinates.get(location)

    def get_locations(self):
        # Return all locations in the network

        return list(self.adjacency.keys())

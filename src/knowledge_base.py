from src import ontology as O
from src.inference_engine import InferenceEngine, fmt_fact, explain_proof
from src.rules import build_rules


class IncidentReport:
    def __init__(self, incident_id, incident_type, casualties=0, symptoms=None,
                 trapped=0, hazards=None, building_type=None, occupied=False,
                 fire_size=None, road_blocked=False, vehicles_involved=1):

        self.incident_id = incident_id
        self.incident_type = incident_type
        self.casualties = casualties
        self.symptoms = set(symptoms) if symptoms is not None else set()
        self.trapped = trapped
        self.hazards = set(hazards) if hazards is not None else set()
        self.building_type = building_type
        self.occupied = occupied
        self.fire_size = fire_size
        self.road_blocked = road_blocked
        self.vehicles_involved = vehicles_involved

        self.validate()

    def validate(self):
        if self.incident_type not in O.INCIDENT_TYPES:
            raise ValueError("Unknown incident type: " + str(self.incident_type))

        if self.casualties < 0 or self.trapped < 0:
            raise ValueError("Casualties and trapped people cannot be negative")

        if self.vehicles_involved < 1:
            raise ValueError("At least one vehicle must be involved")

        if self.incident_type == "medical" and self.casualties < 1:
            raise ValueError("A medical incident needs at least one casualty")

        if not self.symptoms <= O.SYMPTOMS:
            raise ValueError("Unknown symptoms: " + str(sorted(self.symptoms - O.SYMPTOMS)))

        if not self.hazards <= O.HAZARDS:
            raise ValueError("Unknown hazards: " + str(sorted(self.hazards - O.HAZARDS)))

        if self.building_type is not None and self.building_type not in O.BUILDING_TYPES:
            raise ValueError("Unknown building type: " + str(self.building_type))

        if self.fire_size is not None and self.fire_size not in O.FIRE_SIZES:
            raise ValueError("Unknown fire size: " + str(self.fire_size))
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
        
    def to_facts(self):
        incident_id = self.incident_id

        facts = [
            ("incident", incident_id),
            ("incident_type", incident_id, self.incident_type),
            ("casualties", incident_id, self.casualties),
            ("trapped", incident_id, self.trapped),
            ("vehicles_involved", incident_id, self.vehicles_involved)
        ]

        for symptom in sorted(self.symptoms):
            facts.append(("symptom", incident_id, symptom))

        for hazard in sorted(self.hazards):
            facts.append(("hazard", incident_id, hazard))

        if self.building_type:
            facts.append(("building", incident_id, self.building_type))

        if self.fire_size:
            facts.append(("fire_size", incident_id, self.fire_size))

        if self.occupied:
            facts.append(("occupied", incident_id))

        if self.road_blocked:
            facts.append(("road_blocked", incident_id))

        return facts

class Requirement:
    def __init__(self, incident_id, capability, slot):
        if capability not in O.CAPABILITIES:
            raise ValueError("Unknown capability: " + str(capability))

        self.incident_id = incident_id
        self.capability = capability
        self.slot = slot
        self.role_id = incident_id + ":" + capability + "#" + str(slot)

class IncidentAssessment:
    def __init__(self, incident_id, report, priority, requirements,
                 target_minutes, engine, superseded):

        self.incident_id = incident_id
        self.report = report
        self.priority = priority
        self.requirements = requirements
        self.target_response_minutes = target_minutes
        self.engine = engine
        self.superseded = superseded
        self.priority_rank = O.PRIORITY_RANK[priority]

    def capability_counts(self):
        counts = {}

        for requirement in self.requirements:
            capability = requirement.capability
            counts[capability] = counts.get(capability, 0) + 1

        return counts

    def rules_fired(self):
        return self.engine.rules_fired()

    def prove(self, goal):
        node = self.engine.ask(goal)

        if node is None:
            return fmt_fact(goal) + " cannot be derived from the current facts and rules"

        return "\n".join(explain_proof(node))

    def explain_priority(self):
        fact = ("priority", self.incident_id, self.priority)
        lines = self.engine.explain(fact)
        levels = []

        for fact in self.engine.query(("priority_candidate", self.incident_id, "?l")):
            if fact[2] not in levels:
                levels.append(fact[2])

        levels.sort(key=O.PRIORITY_RANK.get, reverse=True)

        if not levels:
            lines.append("  candidates considered: none")
        else:
            lines.append("  candidates considered: " + ", ".join(levels))

        return "\n".join(lines)

    def explain_requirement(self, requirement):
        fact = (
            "need",
            requirement.incident_id,
            requirement.capability,
            requirement.slot
        )

        return "\n".join(self.engine.explain(fact))

    def explain(self):
        output = [
            "Incident " + self.incident_id + " (" + self.report.incident_type + ")",
            "Priority: " + self.priority,
            "Target response: " + str(self.target_response_minutes) + " minutes",
            self.explain_priority(),
            "Requirements:"
        ]

        if not self.requirements:
            output.append("(none)")

        for requirement in self.requirements:
            output.append(self.explain_requirement(requirement))

        for requirement in self.superseded:
            output.append(
                requirement.role_id + " replaced: an ALS unit also provides BLS capability"
            )

        return "\n".join(output)

    def to_dict(self):
        requirements = []

        for requirement in self.requirements:
            requirements.append({
                "role_id": requirement.role_id,
                "capability": requirement.capability,
                "slot": requirement.slot
            })

        rounds = []

        for round_facts in self.engine.rounds:
            rounds.append([fmt_fact(fact) for fact in round_facts])

        return {
            "incident_id": self.incident_id,
            "type": self.report.incident_type,
            "priority": self.priority,
            "target_response_minutes": self.target_response_minutes,
            "requirements": requirements,
            "forward_chaining_rounds": rounds,
            "rules_fired": self.rules_fired(),
            "explanation": self.explain()
        }

    def key(self):
        return (self.incident_id, self.capability, self.slot)
from src import ontology as O
from src.inference_engine import Rule


def incident_is(incident_type):
    return ("incident_type", "?i", incident_type)


def build_rules():
    rules = []

    def add(name, conditions, conclusions, description="", guards=None):
        rules.append(Rule(name, conditions, conclusions, description, guards))

    # Medical reasoning

    for symptom in sorted(O.LIFE_THREATENING_SYMPTOMS):
        add(
            "life_threat_symptom_" + symptom,
            [("symptom", "?i", symptom)],
            [("life_threat", "?i")],
            "Life-threatening symptom: " + symptom
        )

    add(
        "casualties_need_ambulance",
        [("casualties", "?i", "?n")],
        [("needs_ambulance", "?i")],
        "Incident has casualties",
        guards=[("?n", ">", 0)]
    )

    add(
        "medical_needs_ambulance",
        [incident_is("medical")],
        [("needs_ambulance", "?i")],
        "Medical incident requires an ambulance"
    )

    add(
        "life_threat_needs_advanced_care",
        [("life_threat", "?i")],
        [("advanced_care", "?i")],
        "Life-threatening incident requires advanced care"
    )

    for symptom in sorted(O.URGENT_SYMPTOMS):
        add(
            "urgent_symptom_" + symptom,
            [("symptom", "?i", symptom)],
            [("advanced_care", "?i")],
            "Urgent symptom requires advanced care"
        )

    add(
        "multiple_casualties",
        [("casualties", "?i", "?n")],
        [("multi_casualty", "?i")],
        "Incident involves multiple casualties",
        guards=[("?n", ">=", 3)]
    )

    add(
        "mass_casualties",
        [("casualties", "?i", "?n")],
        [("mass_casualty", "?i")],
        "Incident involves a large number of casualties",
        guards=[("?n", ">=", 5)]
    )

    # Fire and collision reasoning

    add(
        "entrapment_detected",
        [("trapped", "?i", "?n")],
        [("entrapment", "?i")],
        "People are trapped at the incident",
        guards=[("?n", ">", 0)]
    )

    add(
        "life_threat_trapped_in_fire",
        [
            incident_is("fire"),
            ("entrapment", "?i")
        ],
        [("life_threat", "?i")],
        "People trapped inside a fire"
    )

    add(
        "life_threat_trapped_in_collision",
        [
            incident_is("collision"),
            ("entrapment", "?i")
        ],
        [("life_threat", "?i")],
        "People trapped in a collision"
    )

    add(
        "occupied_high_rise",
        [
            incident_is("fire"),
            ("building", "?i", "high_rise"),
            ("occupied", "?i")
        ],
        [("high_occupancy_risk", "?i")],
        "Occupied high-rise building involved in a fire"
    )

    add(
        "multiple_vehicles",
        [
            incident_is("collision"),
            ("vehicles_involved", "?i", "?n")
        ],
        [("multi_vehicle", "?i")],
        "Multiple vehicles involved in collision",
        guards=[("?n", ">=", 3)]
    )

    for hazard in sorted(O.ESCALATING_HAZARDS):
        add(
            "escalating_hazard_" + hazard,
            [("hazard", "?i", hazard)],
            [("escalation", "?i")],
            "Incident may escalate due to " + hazard
        )

    add(
        "entrapment_needs_ambulance",
        [("entrapment", "?i")],
        [("needs_ambulance", "?i")],
        "Trapped people may require medical assistance"
    )

    # Critical priority

    add(
        "cand_critical_life_threat",
        [("life_threat", "?i")],
        [("priority_candidate", "?i", "Critical")],
        "Immediate threat to life"
    )

    add(
        "cand_critical_mass_casualty",
        [("mass_casualty", "?i")],
        [("priority_candidate", "?i", "Critical")],
        "Large number of casualties"
    )

    add(
        "cand_critical_occupied_fire",
        [
            incident_is("fire"),
            ("high_occupancy_risk", "?i"),
            ("escalation", "?i")
        ],
        [("priority_candidate", "?i", "Critical")],
        "Occupied high-rise fire with escalating hazards"
    )

    # High priority

    for symptom in sorted(O.URGENT_SYMPTOMS):
        add(
            "cand_high_symptom_" + symptom,
            [("symptom", "?i", symptom)],
            [("priority_candidate", "?i", "High")],
            "Urgent medical symptom"
        )

    add(
        "cand_high_multi_casualty",
        [("multi_casualty", "?i")],
        [("priority_candidate", "?i", "High")],
        "Multiple casualties"
    )

    add(
        "cand_high_escalation",
        [("escalation", "?i")],
        [("priority_candidate", "?i", "High")],
        "Risk of incident escalation"
    )

    add(
        "cand_high_large_fire",
        [
            incident_is("fire"),
            ("fire_size", "?i", "large")
        ],
        [("priority_candidate", "?i", "High")],
        "Large fire"
    )

    add(
        "cand_high_occupancy",
        [("high_occupancy_risk", "?i")],
        [("priority_candidate", "?i", "High")],
        "High occupancy risk"
    )

    # Medium priority

    for symptom in sorted(O.MODERATE_SYMPTOMS):
        add(
            "cand_medium_symptom_" + symptom,
            [("symptom", "?i", symptom)],
            [("priority_candidate", "?i", "Medium")],
            "Moderate medical symptom"
        )

    add(
        "cand_medium_collision",
        [
            incident_is("collision"),
            ("casualties", "?i", "?n")
        ],
        [("priority_candidate", "?i", "Medium")],
        "Collision involving casualties",
        guards=[("?n", ">", 0)]
    )

    add(
        "cand_medium_fire",
        [incident_is("fire")],
        [("priority_candidate", "?i", "Medium")],
        "Reported fire incident"
    )

    add(
        "cand_medium_road_blocked",
        [("road_blocked", "?i")],
        [("priority_candidate", "?i", "Medium")],
        "Incident is blocking the road"
    )

    add(
        "cand_medium_multi_vehicle",
        [("multi_vehicle", "?i")],
        [("priority_candidate", "?i", "Medium")],
        "Collision involving multiple vehicles"
    )

    # Low priority

    for symptom in sorted(O.MINOR_SYMPTOMS):
        add(
            "cand_low_symptom_" + symptom,
            [("symptom", "?i", symptom)],
            [("priority_candidate", "?i", "Low")],
            "Minor medical symptom"
        )

    # Ambulance requirements

    add(
        "need_bls",
        [("needs_ambulance", "?i")],
        [("need", "?i", "bls", 1)],
        "Basic life support ambulance required"
    )

    add(
        "need_als",
        [("advanced_care", "?i")],
        [("need", "?i", "als", 1)],
        "Advanced life support ambulance required"
    )

    add(
        "need_second_ambulance",
        [("multi_casualty", "?i")],
        [("need", "?i", "bls", 2)],
        "Additional ambulance required for multiple casualties"
    )

    add(
        "need_third_ambulance",
        [("mass_casualty", "?i")],
        [("need", "?i", "bls", 3)],
        "Additional ambulance required for mass casualty incident"
    )

    # Fire service requirements

    add(
        "need_fire_engine",
        [incident_is("fire")],
        [("need", "?i", "fire_suppression", 1)],
        "Fire suppression required"
    )

    add(
        "need_second_fire_engine",
        [
            incident_is("fire"),
            ("fire_size", "?i", "large")
        ],
        [("need", "?i", "fire_suppression", 2)],
        "Large fire requires additional fire suppression"
    )

    add(
        "need_aerial_ladder",
        [
            incident_is("fire"),
            ("building", "?i", "high_rise")
        ],
        [("need", "?i", "aerial", 1)],
        "High-rise fire requires aerial capability"
    )

    # Rescue and hazard requirements

    add(
        "need_rescue_tools",
        [("entrapment", "?i")],
        [("need", "?i", "rescue_tools", 1)],
        "Rescue equipment required for trapped people"
    )

    for hazard in sorted(O.FIRE_COVER_HAZARDS):
        add(
            "need_fire_cover_" + hazard,
            [("hazard", "?i", hazard)],
            [("need", "?i", "fire_suppression", 1)],
            "Fire suppression required due to " + hazard
        )

    add(
        "need_hazmat",
        [("hazard", "?i", "hazmat")],
        [("need", "?i", "hazmat", 1)],
        "Hazardous material response required"
    )

    # Priority-based requirements

    add(
        "critical_needs_advanced_care",
        [
            ("priority", "?i", "Critical"),
            ("needs_ambulance", "?i")
        ],
        [("need", "?i", "als", 1)],
        "Critical incident requires advanced medical care"
    )

    add(
        "critical_fire_additional_engine",
        [
            incident_is("fire"),
            ("priority", "?i", "Critical")
        ],
        [("need", "?i", "fire_suppression", 2)],
        "Critical fire requires additional fire suppression"
    )

    # Target response times

    for priority, minutes in O.TARGET_RESPONSE_MINUTES.items():
        add(
            "target_response_" + priority.lower(),
            [("priority", "?i", priority)],
            [("target_response", "?i", minutes)],
            "Target response time for " + priority + " priority"
        )

    return rules
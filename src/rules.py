from src import ontology as O
from src.inference_engine import Rule


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
        [("incident_type", "?i", "medical")],
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

    return rules
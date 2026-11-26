# Emergency dispatch vocab

# Priority levels and response targets (minutes)
PRIORITY_RANK = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

TARGET_RESPONSE_MINUTES = {
    "Critical": 8,
    "High": 15,
    "Medium": 30,
    "Low": 60
}


# Types of incidents supported by the system
INCIDENT_TYPES = ["medical", "fire", "collision"]


# Symptoms grouped by severity
LIFE_THREATENING_SYMPTOMS = {
    "cardiac_arrest",
    "severe_bleeding",
    "unconscious",
    "stroke_signs",
    "breathing_difficulty",
    "anaphylaxis"
}

URGENT_SYMPTOMS = {
    "chest_pain"
}

MODERATE_SYMPTOMS = {
    "fracture",
    "burns",
    "head_injury"
}

MINOR_SYMPTOMS = {
    "minor_injury",
    "minor_illness"
}

# All recognised symptoms
SYMPTOMS = (
    LIFE_THREATENING_SYMPTOMS
    | URGENT_SYMPTOMS
    | MODERATE_SYMPTOMS
    | MINOR_SYMPTOMS
)


# Hazards that can be reported at an incident
HAZARDS = {
    "fire_spread",
    "fuel_leak",
    "hazmat",
    "structural_collapse",
    "gas_leak",
    "electrical",
    "smoke"
}

# Hazards that may increase the severity of an incident
ESCALATING_HAZARDS = {
    "fire_spread",
    "fuel_leak",
    "hazmat",
    "structural_collapse",
    "gas_leak"
}

# Hazards that may require fire service support
FIRE_COVER_HAZARDS = {
    "fire_spread",
    "fuel_leak",
    "gas_leak"
}


# Building types and fire sizes
BUILDING_TYPES = {
    "residential",
    "commercial",
    "high_rise",
    "industrial"
}

FIRE_SIZES = ["small", "medium", "large"]


# Capabilities that emergency responders can provide.
CAPABILITIES = {
    "bls",
    "als",
    "fire_suppression",
    "aerial",
    "rescue_tools",
    "hazmat"
}

"""
Bush-Francis Catatonia Rating Scale Models

Request and response models for Bush-Francis Catatonia Rating Scale calculation.

References (Vancouver style):
1. Bush G, Fink M, Petrides G, Dowling F, Francis A. Catatonia. I. Rating scale and 
   standardized examination. Acta Psychiatr Scand. 1996 Feb;93(2):129-36. 
   doi: 10.1111/j.1600-0447.1996.tb09814.x.
2. Bush G, Fink M, Petrides G, Dowling F, Francis A. Catatonia. II. Treatment with 
   lorazepam and electroconvulsive therapy. Acta Psychiatr Scand. 1996 Feb;93(2):137-43. 
   doi: 10.1111/j.1600-0447.1996.tb09815.x.
3. Francis A. Catatonia: diagnosis, classification, and treatment. Curr Psychiatry Rep. 
   2010 Jun;12(3):180-5. doi: 10.1007/s11920-010-0113-y.
4. Sienaert P, Dhossche DM, Vancampfort D, De Hert M, Gazdag G. A clinical review of 
   the treatment of catatonia. Front Psychiatry. 2014 Dec 9;5:181. 
   doi: 10.3389/fpsyt.2014.00181.

The Bush-Francis Catatonia Rating Scale (BFCRS) is considered the gold standard for 
clinical and research purposes for catatonia screening and diagnosis. It consists of 
23 items: the first 14 items comprise the Bush-Francis Catatonia Screening Instrument 
(BFCSI), and if 2 or more items are positive, the full 23-item scale should be completed.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any


class BushFrancisCatatoniaRatingScaleRequest(BaseModel):
    """
    Request model for Bush-Francis Catatonia Rating Scale
    
    The BFCRS evaluates 23 catatonic signs with specific scoring:
    
    Screening Items (1-14) - Must all be provided:
    1. Excitement: Extreme hyperactivity, constant motor unrest
    2. Immobility/Stupor: Extreme hypoactivity, minimally responsive
    3. Mutism: Verbally unresponsive or minimally responsive
    4. Staring: Fixed gaze, decreased blinking
    5. Posturing/Catalepsy: Spontaneous maintenance of postures
    6. Grimacing: Maintenance of odd facial expressions
    7. Echopraxia/Echolalia: Mimicking movements/speech
    8. Stereotypy: Repetitive, non-goal-directed motor activity
    9. Mannerisms: Odd, purposeful movements
    10. Verbigeration: Repetition of phrases/sentences
    11. Rigidity: Maintenance of rigid position
    12. Negativism: Motiveless resistance to instructions
    13. Waxy Flexibility: Initial resistance before repositioning
    14. Withdrawal: Refusal to eat/drink/make eye contact (0 or 3 only)
    
    Additional Items (15-23) - Optional, complete if screening positive:
    15. Impulsivity: Sudden inappropriate behavior
    16. Automatic Obedience: Exaggerated cooperation
    17. Passive Obedience (Mitgehen): 'Anglepoise lamp' movement (0 or 3 only)
    18. Muscle Resistance (Gegenhalten): Proportional resistance (0 or 3 only)
    19. Motorically Stuck (Ambitendency): Indecisive movement (0 or 3 only)
    20. Grasp Reflex: Per neurological exam (0 or 3 only)
    21. Perseveration: Returns to same topic/movements (0 or 3 only)
    22. Combativeness: Usually undirected
    23. Autonomic Abnormality: Vital sign abnormalities, diaphoresis
    
    Scoring:
    - Items 14, 17-21: Binary (0=absent or 3=present)
    - All other items: 0=absent, 1=occasional, 2=frequent, 3=constant
    - Total score range: 0-69
    - Screening positive if ≥2 of first 14 items score ≥1
    
    References (Vancouver style):
    1. Bush G, Fink M, Petrides G, Dowling F, Francis A. Catatonia. I. Rating scale and 
    standardized examination. Acta Psychiatr Scand. 1996 Feb;93(2):129-36.
    """
    
    # Screening items (1-14) - All required
    excitement: int = Field(
        ...,
        ge=0, le=3,
        description="Extreme hyperactivity, constant motor unrest which is apparently non-purposeful. Score 0=absent, 1=excessive motion/intermittent, 2=constant motion/hyperkinetic without rest, 3=full-blown catatonic excitement",
        example=0
    )
    
    immobility_stupor: int = Field(
        ...,
        ge=0, le=3,
        description="Extreme hypoactivity, immobile, minimally responsive to stimuli. Score 0=absent, 1=sits abnormally still/may interact briefly, 2=virtually no interaction with external world, 3=stuporous/non-reactive to painful stimuli",
        example=0
    )
    
    mutism: int = Field(
        ...,
        ge=0, le=3,
        description="Verbally unresponsive or minimally responsive. Score 0=absent, 1=verbally unresponsive to majority of questions, 2=speaks <20 words per 5 min, 3=no speech",
        example=0
    )
    
    staring: int = Field(
        ...,
        ge=0, le=3,
        description="Fixed gaze, little or no visual scanning of environment, decreased blinking. Score 0=absent, 1=poor eye contact/gazes <20 sec, 2=gaze held >20 sec, 3=fixed gaze/non-reactive",
        example=0
    )
    
    posturing_catalepsy: int = Field(
        ...,
        ge=0, le=3,
        description="Spontaneous maintenance of posture(s), including mundane (e.g., sitting or standing for long periods without reacting). Score 0=absent, 1=<1 min, 2=>1 min to <15 min, 3=bizarre posture or mundane >15 min",
        example=0
    )
    
    grimacing: int = Field(
        ...,
        ge=0, le=3,
        description="Maintenance of odd facial expressions. Score 0=absent, 1=<10 sec, 2=<1 min, 3=bizarre expression(s) or maintained >1 min",
        example=0
    )
    
    echopraxia_echolalia: int = Field(
        ...,
        ge=0, le=3,
        description="Mimicking of examiner's movements/speech. Score 0=absent, 1=occasional, 2=frequent, 3=constant",
        example=0
    )
    
    stereotypy: int = Field(
        ...,
        ge=0, le=3,
        description="Repetitive, non-goal-directed motor activity (e.g., finger-play, repeatedly touching, patting, or rubbing self). Score 0=absent, 1=occasional, 2=frequent, 3=constant",
        example=0
    )
    
    mannerisms: int = Field(
        ...,
        ge=0, le=3,
        description="Odd, purposeful movements (e.g., hopping or walking tiptoe, saluting passers-by, or exaggerated caricatures of mundane movements). Score 0=absent, 1=occasional, 2=frequent, 3=constant",
        example=0
    )
    
    verbigeration: int = Field(
        ...,
        ge=0, le=3,
        description="Repetition of phrases or sentences (like a scratched record). Score 0=absent, 1=occasional, 2=frequent, 3=constant",
        example=0
    )
    
    rigidity: int = Field(
        ...,
        ge=0, le=3,
        description="Maintenance of a rigid position despite efforts to be moved, exclude if cogwheel rigidity or tremor present. Score 0=absent, 1=mild resistance, 2=moderate, 3=severe/cannot be repositioned",
        example=0
    )
    
    negativism: int = Field(
        ...,
        ge=0, le=3,
        description="Apparently motiveless resistance to instructions or attempts to move/examine patient. Contrary behavior, does exact opposite of instruction. Score 0=absent, 1=mild resistance/occasionally contrary, 2=moderate resistance/frequently contrary, 3=severe resistance/continually contrary",
        example=0
    )
    
    waxy_flexibility: int = Field(
        ...,
        ge=0, le=3,
        description="During reposturing of patient, patient offers initial resistance before allowing themselves to be repositioned, similar to that of a bending candle. Score 0=absent, 1=mild/slight resistance, 2=moderate, 3=severe/pronounced resistance",
        example=0
    )
    
    withdrawal: int = Field(
        ...,
        description="Refusal to eat, drink, and/or make eye contact. BINARY SCORING: 0=absent or 3=present (no intermediate scores)",
        example=0
    )
    
    # Additional items (15-23) - Optional
    impulsivity: int = Field(
        None,
        ge=0, le=3,
        description="Patient suddenly engages in inappropriate behavior without provocation. Afterwards can give no, or only a facile explanation. Score 0=absent, 1=occasional, 2=frequent, 3=constant or severe",
        example=0
    )
    
    automatic_obedience: int = Field(
        None,
        ge=0, le=3,
        description="Exaggerated cooperation with examiner's request or spontaneous continuation of movement requested. Score 0=absent, 1=occasional, 2=frequent, 3=constant",
        example=0
    )
    
    passive_obedience: int = Field(
        None,
        description="Mitgehen - 'Anglepoise lamp' arm raising in response to light pressure of finger, despite instruction to resist. BINARY SCORING: 0=absent or 3=present",
        example=0
    )
    
    muscle_resistance: int = Field(
        None,
        description="Gegenhalten - Resistance to passive movement which is proportional to strength of the stimulus; appears automatic rather than willful. BINARY SCORING: 0=absent or 3=present",
        example=0
    )
    
    motorically_stuck: int = Field(
        None,
        description="Ambitendency - Patient appears motorically 'stuck' in indecisive, hesitant movement. BINARY SCORING: 0=absent or 3=present",
        example=0
    )
    
    grasp_reflex: int = Field(
        None,
        description="Per neurological exam. BINARY SCORING: 0=absent or 3=present",
        example=0
    )
    
    perseveration: int = Field(
        None,
        description="Repeatedly returns to same topic or persists with same movements. BINARY SCORING: 0=absent or 3=present",
        example=0
    )
    
    combativeness: int = Field(
        None,
        ge=0, le=3,
        description="Usually in an undirected manner, with no, or only a facile explanation afterwards. Score 0=absent, 1=occasional, 2=frequent, 3=constant or severe",
        example=0
    )
    
    autonomic_abnormality: int = Field(
        None,
        ge=0, le=3,
        description="Temperature, BP, pulse, or respiratory rate abnormality; diaphoresis. Score 0=absent, 1=one abnormality, 2=two abnormalities, 3=three or more abnormalities. Critical for identifying malignant catatonia",
        example=0
    )
    
    @field_validator('withdrawal', 'passive_obedience', 'muscle_resistance', 
                     'motorically_stuck', 'grasp_reflex', 'perseveration')
    def validate_binary_items(cls, v, info):
        """Validates that binary items are scored as 0 or 3 only"""
        if v is not None and v not in [0, 3]:
            raise ValueError(f"{info.field_name} must be either 0 (absent) or 3 (present)")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "excitement": 0,
                "immobility_stupor": 2,
                "mutism": 3,
                "staring": 2,
                "posturing_catalepsy": 1,
                "grimacing": 0,
                "echopraxia_echolalia": 0,
                "stereotypy": 1,
                "mannerisms": 0,
                "verbigeration": 0,
                "rigidity": 2,
                "negativism": 1,
                "waxy_flexibility": 1,
                "withdrawal": 3,
                "impulsivity": 0,
                "automatic_obedience": 0,
                "passive_obedience": 0,
                "muscle_resistance": 3,
                "motorically_stuck": 0,
                "grasp_reflex": 0,
                "perseveration": 0,
                "combativeness": 0,
                "autonomic_abnormality": 1
            }
        }


class BushFrancisCatatoniaRatingScaleResponse(BaseModel):
    """
    Response model for Bush-Francis Catatonia Rating Scale
    
    The BFCRS provides comprehensive assessment of catatonia severity:
    
    Screening Results:
    - Positive if ≥2 of first 14 items score ≥1
    - Indicates need for full 23-item assessment
    - Suggests immediate evaluation for catatonia treatment
    
    Total Score Interpretation:
    - 0-9: Mild catatonia
    - 10-19: Moderate catatonia
    - 20-29: Severe catatonia
    - ≥30: Very severe catatonia
    
    Clinical Significance:
    - Catatonia is a neuropsychiatric syndrome with motor, behavioral, and autonomic features
    - Can occur in psychiatric, neurological, and medical conditions
    - Benzodiazepine trial (lorazepam) is both diagnostic and therapeutic
    - Malignant catatonia (with autonomic instability) is a medical emergency
    - ECT is highly effective for benzodiazepine-resistant cases
    
    Reference: Bush G, et al. Acta Psychiatr Scand. 1996;93(2):129-36.
    """
    
    result: int = Field(
        ...,
        description="Total Bush-Francis Catatonia Rating Scale score (range: 0-69 points)",
        example=19
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on screening result and total score",
        example="Two or more items positive in screening instrument indicates positive screening for catatonia. Total score: 19/69. Moderate severity. Complete full 23-item assessment if not already done. Consider immediate treatment, particularly if autonomic instability is present. Benzodiazepine trial (lorazepam) is both diagnostic and therapeutic."
    )
    
    stage: str = Field(
        ...,
        description="Screening result (Positive Screen or Negative Screen)",
        example="Positive Screen"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of catatonia likelihood and severity",
        example="Catatonia likely present - Moderate severity"
    )
    
    screening_score: int = Field(
        ...,
        description="Score from the 14-item screening instrument",
        example=15
    )
    
    screening_positive: bool = Field(
        ...,
        description="Whether screening is positive (≥2 items with score ≥1)",
        example=True
    )
    
    positive_screening_items: int = Field(
        ...,
        description="Number of screening items with positive scores (≥1)",
        example=7
    )
    
    item_breakdown: Dict[str, List[Dict[str, Any]]] = Field(
        ...,
        description="Breakdown of scores by screening and additional items",
        example={
            "screening_items": [
                {"item": "Immobility Stupor", "score": 2, "binary": False},
                {"item": "Mutism", "score": 3, "binary": False},
                {"item": "Withdrawal", "score": 3, "binary": True}
            ],
            "additional_items": [
                {"item": "Muscle Resistance", "score": 3, "binary": True},
                {"item": "Autonomic Abnormality", "score": 1, "binary": False}
            ]
        }
    )
    
    clinical_recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Categorized clinical recommendations based on results",
        example={
            "immediate_actions": [
                "Complete full 23-item BFCRS assessment if not already done",
                "Medical workup to identify underlying causes",
                "Assess for malignant catatonia (fever, autonomic instability)"
            ],
            "diagnostic": [
                "Lorazepam challenge test (1-2mg IV/IM) - diagnostic and therapeutic",
                "CBC, CMP, TSH, B12, folate, urinalysis",
                "Consider brain imaging (CT/MRI) if first episode or focal findings"
            ],
            "treatment": [
                "Lorazepam 1-2mg PO/IM/IV TID, titrate to response",
                "Monitor response within 24-48 hours",
                "Consider ECT if no response to adequate benzodiazepine trial"
            ],
            "monitoring": [
                "Re-assess with BFCRS daily during acute treatment",
                "Monitor vital signs closely, especially if autonomic symptoms present",
                "Watch for complications: aspiration, dehydration, rhabdomyolysis"
            ]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 19,
                "unit": "points",
                "interpretation": "Two or more items positive in screening instrument indicates positive screening for catatonia. Total score: 19/69. Moderate severity. Complete full 23-item assessment if not already done. Consider immediate treatment, particularly if autonomic instability is present. Benzodiazepine trial (lorazepam) is both diagnostic and therapeutic.",
                "stage": "Positive Screen",
                "stage_description": "Catatonia likely present - Moderate severity",
                "screening_score": 15,
                "screening_positive": True,
                "positive_screening_items": 7,
                "item_breakdown": {
                    "screening_items": [
                        {"item": "Excitement", "score": 0, "binary": False},
                        {"item": "Immobility Stupor", "score": 2, "binary": False},
                        {"item": "Mutism", "score": 3, "binary": False},
                        {"item": "Staring", "score": 2, "binary": False},
                        {"item": "Posturing Catalepsy", "score": 1, "binary": False},
                        {"item": "Grimacing", "score": 0, "binary": False},
                        {"item": "Echopraxia Echolalia", "score": 0, "binary": False},
                        {"item": "Stereotypy", "score": 1, "binary": False},
                        {"item": "Mannerisms", "score": 0, "binary": False},
                        {"item": "Verbigeration", "score": 0, "binary": False},
                        {"item": "Rigidity", "score": 2, "binary": False},
                        {"item": "Negativism", "score": 1, "binary": False},
                        {"item": "Waxy Flexibility", "score": 1, "binary": False},
                        {"item": "Withdrawal", "score": 3, "binary": True}
                    ],
                    "additional_items": [
                        {"item": "Impulsivity", "score": 0, "binary": False},
                        {"item": "Automatic Obedience", "score": 0, "binary": False},
                        {"item": "Passive Obedience", "score": 0, "binary": True},
                        {"item": "Muscle Resistance", "score": 3, "binary": True},
                        {"item": "Motorically Stuck", "score": 0, "binary": True},
                        {"item": "Grasp Reflex", "score": 0, "binary": True},
                        {"item": "Perseveration", "score": 0, "binary": True},
                        {"item": "Combativeness", "score": 0, "binary": False},
                        {"item": "Autonomic Abnormality", "score": 1, "binary": False}
                    ]
                },
                "clinical_recommendations": {
                    "immediate_actions": [
                        "Complete full 23-item BFCRS assessment if not already done",
                        "Medical workup to identify underlying causes",
                        "Assess for malignant catatonia (fever, autonomic instability)"
                    ],
                    "diagnostic": [
                        "Lorazepam challenge test (1-2mg IV/IM) - diagnostic and therapeutic",
                        "CBC, CMP, TSH, B12, folate, urinalysis",
                        "Consider brain imaging (CT/MRI) if first episode or focal findings",
                        "EEG if seizure activity suspected",
                        "Review medications for potential causative agents"
                    ],
                    "treatment": [
                        "Lorazepam 1-2mg PO/IM/IV TID, titrate to response",
                        "Monitor response within 24-48 hours",
                        "Consider ECT if no response to adequate benzodiazepine trial",
                        "Address underlying psychiatric or medical condition",
                        "Ensure adequate nutrition and hydration"
                    ],
                    "monitoring": [
                        "Re-assess with BFCRS daily during acute treatment",
                        "Monitor vital signs closely, especially if autonomic symptoms present",
                        "Watch for complications: aspiration, dehydration, rhabdomyolysis",
                        "Document response to lorazepam challenge",
                        "Consider continuous monitoring if malignant features present"
                    ]
                }
            }
        }
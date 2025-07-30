"""
Brugada Criteria for Ventricular Tachycardia Models

Request and response models for Brugada Criteria calculation.

References (Vancouver style):
1. Brugada P, Brugada J, Mont L, Smeets J, Andries EW. A new approach to the 
   differential diagnosis of a regular tachycardia with a wide QRS complex. 
   Circulation. 1991;83(5):1649-59. doi: 10.1161/01.cir.83.5.1649.
2. Isenhour JL, Craig S, Gibbs M, Littmann L, Rose G, Risch R. Wide-complex 
   tachycardia: continued evaluation of diagnostic criteria. Acad Emerg Med. 
   2000;7(7):769-73. doi: 10.1111/j.1553-2712.2000.tb02267.x.
3. Vereckei A, Duray G, Szénási G, Altemose GT, Miller JM. Application of a new 
   algorithm in the differential diagnosis of wide QRS complex tachycardia. 
   Eur Heart J. 2007;28(5):589-600. doi: 10.1093/eurheartj/ehl473.

The Brugada Criteria is a four-step sequential algorithm used to differentiate 
ventricular tachycardia (VT) from supraventricular tachycardia (SVT) with aberrancy 
in patients presenting with wide-complex tachycardia. This distinction is critical 
as treatments for SVT (adenosine, calcium channel blockers) can be detrimental to 
patients with VT. The algorithm has a reported sensitivity of 98.7% and specificity 
of 96.5% for VT detection in the original study, though validation studies have 
shown variable performance.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List, Optional


class BrugadaCriteriaVtRequest(BaseModel):
    """
    Request model for Brugada Criteria for Ventricular Tachycardia
    
    The Brugada Criteria uses a four-step sequential approach to differentiate VT from SVT with aberrancy:
    
    Step 1: Absence of RS complex in all precordial leads (V1-V6)
    - Examines whether there is complete absence of RS complexes in leads V1-V6
    - If yes, diagnosis is VT (stop algorithm)
    - This suggests ventricular origin of the arrhythmia
    
    Step 2: R to S interval >100 ms in any precordial lead (Brugada's sign)
    - Measures the time from beginning of R wave to nadir of S wave
    - If >100 milliseconds in any precordial lead, diagnosis is VT (stop algorithm)
    - Prolonged R-S interval suggests slow ventricular conduction
    
    Step 3: Atrioventricular dissociation
    - Looks for independent atrial and ventricular activity
    - P waves randomly dispersed throughout the rhythm
    - If present, diagnosis is VT (stop algorithm)
    - AV dissociation is pathognomonic for VT
    
    Step 4: Morphology criteria for VT in leads V1-V2 and V6
    - Specific morphological patterns in precordial leads
    - Includes QRS patterns characteristic of ventricular origin
    - If present, diagnosis is VT (stop algorithm)
    - Pattern recognition based on lead-specific criteria

    Clinical significance: Any positive step indicates VT. All steps must be negative 
    to suggest SVT with aberrancy. When in doubt, treat as VT.

    References (Vancouver style):
    1. Brugada P, Brugada J, Mont L, Smeets J, Andries EW. A new approach to the 
    differential diagnosis of a regular tachycardia with a wide QRS complex. 
    Circulation. 1991;83(5):1649-59. doi: 10.1161/01.cir.83.5.1649.
    2. Isenhour JL, Craig S, Gibbs M, Littmann L, Rose G, Risch R. Wide-complex 
    tachycardia: continued evaluation of diagnostic criteria. Acad Emerg Med. 
    2000;7(7):769-73. doi: 10.1111/j.1553-2712.2000.tb02267.x.
    3. Vereckei A, Duray G, Szénási G, Altemose GT, Miller JM. Application of a new 
    algorithm in the differential diagnosis of wide QRS complex tachycardia. 
    Eur Heart J. 2007;28(5):589-600. doi: 10.1093/eurheartj/ehl473.
    """
    
    absence_rs_precordial: Literal["yes", "no"] = Field(
        ...,
        description="Step 1: Is there absence of RS complex in all precordial leads (V1-V6)? If yes, this indicates VT.",
        example="no"
    )
    
    r_to_s_interval_100ms: Literal["yes", "no"] = Field(
        ...,
        description="Step 2: Is the R to S interval >100 ms in any precordial lead (Brugada's sign)? Measured from beginning of R wave to nadir of S wave. If yes, this indicates VT.",
        example="no"
    )
    
    av_dissociation: Literal["yes", "no"] = Field(
        ...,
        description="Step 3: Is there atrioventricular dissociation present? P waves randomly dispersed throughout rhythm, independent of QRS complexes. If yes, this indicates VT.",
        example="yes"
    )
    
    morphology_criteria_vt: Literal["yes", "no"] = Field(
        ...,
        description="Step 4: Are morphology criteria for VT present in leads V1-V2 and V6? Specific QRS patterns characteristic of ventricular origin. If yes, this indicates VT.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "absence_rs_precordial": "no",
                "r_to_s_interval_100ms": "no",
                "av_dissociation": "yes",
                "morphology_criteria_vt": "no"
            }
        }


class BrugadaCriteriaVtResponse(BaseModel):
    """
    Response model for Brugada Criteria for Ventricular Tachycardia
    
    The Brugada Criteria provides:
    - Sequential algorithm assessment (4 steps)
    - Diagnosis: VT or SVT with aberrancy
    - Step-by-step analysis showing which criterion was positive
    - Clinical recommendations for treatment
    
    Key clinical points:
    - Any positive step = VT diagnosis (algorithm stops)
    - All negative steps = SVT with aberrancy (but treat as VT when in doubt)
    - VT requires immediate cardioversion if unstable, antiarrhythmics if stable
    - SVT treatments (adenosine, CCBs) can worsen VT
    
    Reference: Brugada P, et al. Circulation. 1991;83(5):1649-59.
    """
    
    result: str = Field(
        ...,
        description="Final diagnosis based on Brugada Criteria (VT or SVT with Aberrancy)",
        example="VT"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for categorical diagnosis)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations",
        example="The ECG findings are consistent with ventricular tachycardia. This is a life-threatening arrhythmia requiring immediate cardioversion or antiarrhythmic therapy. Do not treat with medications intended for SVT (adenosine, calcium channel blockers) as they may worsen the condition."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage (VT or SVT with Aberrancy)",
        example="VT"
    )
    
    stage_description: str = Field(
        ...,
        description="Full description of the diagnosis",
        example="Ventricular Tachycardia"
    )
    
    positive_criterion: Optional[str] = Field(
        None,
        description="The first positive criterion that led to VT diagnosis (null if all negative)",
        example="Atrioventricular dissociation present"
    )
    
    positive_step: Optional[int] = Field(
        None,
        description="The step number (1-4) where positive criterion was found (null if all negative)",
        example=3
    )
    
    algorithm_summary: Dict[str, Dict[str, str]] = Field(
        ...,
        description="Step-by-step summary of each criterion and its result",
        example={
            "step_1": {
                "criterion": "Absence of RS complex in all precordial leads (V1-V6)",
                "result": "Negative",
                "interpretation": "Does not support VT diagnosis"
            },
            "step_2": {
                "criterion": "R to S interval >100 ms in any precordial lead",
                "result": "Negative", 
                "interpretation": "Does not support VT diagnosis"
            },
            "step_3": {
                "criterion": "Atrioventricular dissociation present",
                "result": "Positive",
                "interpretation": "AV dissociation with independent P waves suggests VT"
            },
            "step_4": {
                "criterion": "Morphology criteria for VT present in V1-V2 and V6",
                "result": "Negative",
                "interpretation": "Does not support VT diagnosis"
            }
        }
    )
    
    clinical_recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Clinical recommendations categorized by immediate actions, medications, monitoring, and precautions",
        example={
            "immediate_actions": [
                "Assess hemodynamic stability",
                "Prepare for immediate cardioversion if unstable",
                "Consider antiarrhythmic therapy if stable"
            ],
            "medications": [
                "Amiodarone 150mg IV over 10 minutes if stable VT",
                "Lidocaine 1-1.5mg/kg IV if amiodarone unavailable",
                "Avoid adenosine and calcium channel blockers"
            ],
            "monitoring": [
                "Continuous cardiac monitoring",
                "Blood pressure monitoring",
                "Prepare for defibrillation"
            ],
            "contraindications": [
                "Do not give adenosine",
                "Avoid calcium channel blockers",
                "Do not use beta-blockers acutely"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "VT",
                "unit": "",
                "interpretation": "The ECG findings are consistent with ventricular tachycardia. This is a life-threatening arrhythmia requiring immediate cardioversion or antiarrhythmic therapy. Do not treat with medications intended for SVT (adenosine, calcium channel blockers) as they may worsen the condition.",
                "stage": "VT",
                "stage_description": "Ventricular Tachycardia",
                "positive_criterion": "Atrioventricular dissociation present",
                "positive_step": 3,
                "algorithm_summary": {
                    "step_1": {
                        "criterion": "Absence of RS complex in all precordial leads (V1-V6)",
                        "result": "Negative",
                        "interpretation": "Does not support VT diagnosis"
                    },
                    "step_2": {
                        "criterion": "R to S interval >100 ms in any precordial lead",
                        "result": "Negative",
                        "interpretation": "Does not support VT diagnosis"
                    },
                    "step_3": {
                        "criterion": "Atrioventricular dissociation present",
                        "result": "Positive",
                        "interpretation": "AV dissociation with independent P waves suggests VT"
                    },
                    "step_4": {
                        "criterion": "Morphology criteria for VT present in V1-V2 and V6",
                        "result": "Negative",
                        "interpretation": "Does not support VT diagnosis"
                    }
                },
                "clinical_recommendations": {
                    "immediate_actions": [
                        "Assess hemodynamic stability",
                        "Prepare for immediate cardioversion if unstable",
                        "Consider antiarrhythmic therapy if stable"
                    ],
                    "medications": [
                        "Amiodarone 150mg IV over 10 minutes if stable VT",
                        "Lidocaine 1-1.5mg/kg IV if amiodarone unavailable",
                        "Avoid adenosine and calcium channel blockers"
                    ],
                    "monitoring": [
                        "Continuous cardiac monitoring",
                        "Blood pressure monitoring",
                        "Prepare for defibrillation"
                    ],
                    "contraindications": [
                        "Do not give adenosine",
                        "Avoid calcium channel blockers",
                        "Do not use beta-blockers acutely"
                    ]
                }
            }
        }
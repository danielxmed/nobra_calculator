"""
Canadian CT Head Injury/Trauma Rule Models

Request and response models for Canadian CT Head Rule calculation.

References (Vancouver style):
1. Stiell IG, Wells GA, Vandemheen K, Clement C, Lesiuk H, Laupacis A, et al. 
   The Canadian CT Head Rule for patients with minor head injury. Lancet. 
   2001 May 5;357(9266):1391-6. doi: 10.1016/s0140-6736(00)04561-x.
2. Stiell IG, Clement CM, Rowe BH, Schull MJ, Brison R, Cass D, et al. 
   Comparison of the Canadian CT Head Rule and the New Orleans Criteria in 
   patients with minor head injury. JAMA. 2005 Sep 28;294(12):1511-8. 
   doi: 10.1001/jama.294.12.1511.
3. Stiell IG, Clement CM, Grimshaw JM, Brison RJ, Rowe BH, Lee JS, et al. 
   A prospective cluster-randomized trial to implement the Canadian CT Head 
   Rule in emergency departments. CMAJ. 2010 Oct 5;182(14):1527-32. 
   doi: 10.1503/cmaj.091974.

The Canadian CT Head Rule is a validated clinical decision tool that identifies
which minor head injury patients require CT imaging. It is 100% sensitive for
detecting injuries requiring neurosurgical intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CanadianCtHeadRuleRequest(BaseModel):
    """
    Request model for Canadian CT Head Injury/Trauma Rule
    
    The Canadian CT Head Rule applies to minor head injury patients with:
    
    Inclusion criteria:
    - Glasgow Coma Scale (GCS) score 13-15
    - Witnessed loss of consciousness, definite amnesia, or witnessed disorientation
    - Injury within the past 24 hours
    
    Exclusion criteria:
    - Age <16 years
    - Minimal head injury (no loss of consciousness, amnesia, or disorientation)
    - Obvious penetrating skull injury or depressed fracture
    - Acute focal neurological deficit
    - Unstable vital signs associated with major trauma
    - Seizure before assessment in the emergency department
    - Bleeding disorder or on anticoagulation
    - Return for reassessment of same head injury
    - Pregnant
    
    High-risk criteria (100% sensitive for neurosurgical intervention):
    1. GCS <15 at 2 hours after injury
    2. Suspected open or depressed skull fracture
    3. Any sign of basilar skull fracture
    4. Vomiting ≥2 episodes
    5. Age ≥65 years
    
    Medium-risk criteria (identify clinically important brain injury):
    1. Amnesia before impact >30 minutes
    2. Dangerous mechanism (pedestrian struck, ejected from vehicle, fall >3 feet)
    
    References (Vancouver style):
    1. Stiell IG, Wells GA, Vandemheen K, Clement C, Lesiuk H, Laupacis A, et al. 
    The Canadian CT Head Rule for patients with minor head injury. Lancet. 
    2001 May 5;357(9266):1391-6.
    """
    
    gcs_less_than_15_at_2hrs: Literal["yes", "no"] = Field(
        ...,
        description="Is the Glasgow Coma Scale score less than 15 at 2 hours after injury? High-risk criterion if yes",
        example="no"
    )
    
    suspected_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Is there suspected open or depressed skull fracture? Look for palpable skull deformity, visible bone fragments, or penetrating injury. High-risk criterion if yes",
        example="no"
    )
    
    basilar_skull_fracture_signs: Literal["yes", "no"] = Field(
        ...,
        description="Any sign of basilar skull fracture? Including: hemotympanum, raccoon eyes (periorbital ecchymosis), CSF otorrhea/rhinorrhea, Battle's sign (retroauricular ecchymosis). High-risk criterion if yes",
        example="no"
    )
    
    vomiting_2_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Has the patient vomited 2 or more times? High-risk criterion if yes",
        example="no"
    )
    
    age_65_or_over: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient aged 65 years or older? High-risk criterion if yes",
        example="no"
    )
    
    amnesia_30_min_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have retrograde amnesia to the event of 30 minutes or more? (Before impact, not after). Medium-risk criterion if yes",
        example="no"
    )
    
    dangerous_mechanism: Literal["yes", "no"] = Field(
        ...,
        description="Was there a dangerous mechanism of injury? Including: pedestrian struck by motor vehicle, occupant ejected from motor vehicle, fall from elevation >3 feet or >5 stairs. Medium-risk criterion if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "gcs_less_than_15_at_2hrs": "no",
                "suspected_skull_fracture": "no",
                "basilar_skull_fracture_signs": "no",
                "vomiting_2_or_more": "no",
                "age_65_or_over": "no",
                "amnesia_30_min_or_more": "no",
                "dangerous_mechanism": "no"
            }
        }


class CanadianCtHeadRuleResponse(BaseModel):
    """
    Response model for Canadian CT Head Injury/Trauma Rule
    
    The rule provides clear recommendations for CT head imaging:
    - High Risk: CT required (100% sensitive for neurosurgical intervention)
    - Medium Risk: CT required (identifies clinically important brain injury)
    - Low Risk: No CT required (safe for discharge without imaging)
    
    Performance characteristics:
    - Sensitivity: 100% for injuries requiring neurosurgical intervention
    - Sensitivity: 98.4% for clinically important brain injury
    - Specificity: 49.6% for clinically important brain injury
    - Can reduce CT imaging by approximately 30-50%
    
    Clinically important brain injury defined as:
    - Any acute brain finding on CT that would normally require admission and
      neurological follow-up (includes epidural, subdural, subarachnoid hemorrhage,
      contusions, depressed skull fractures)
    
    Reference: Stiell IG, et al. Lancet. 2001;357(9266):1391-6.
    """
    
    result: str = Field(
        ...,
        description="CT imaging recommendation based on the Canadian CT Head Rule",
        example="CT Not Required"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (recommendation)",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and detailed explanation of the recommendation",
        example="The patient has no high-risk or medium-risk criteria. CT head imaging is not required based on the Canadian CT Head Rule. The patient can be safely discharged without imaging."
    )
    
    stage: str = Field(
        ...,
        description="Risk level (High Risk, Medium Risk, or Low Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the imaging requirement",
        example="No CT head required"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "CT Not Required",
                "unit": "recommendation",
                "interpretation": "The patient has no high-risk or medium-risk criteria. CT head imaging is not required based on the Canadian CT Head Rule. The patient can be safely discharged without imaging.",
                "stage": "Low Risk",
                "stage_description": "No CT head required"
            }
        }
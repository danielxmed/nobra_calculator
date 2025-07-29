"""
Antivenom Dosing Algorithm Models

Request and response models for Antivenom Dosing Algorithm calculation.

References (Vancouver style):
1. Lavonas EJ, Ruha AM, Banner W, et al. Unified treatment algorithm for the management 
   of crotaline snakebite in the United States: results of an evidence-informed consensus 
   workshop. BMC Emerg Med. 2011;11:2. doi: 10.1186/1471-227X-11-2.
2. Dart RC, Seifert SA, Boyer LV, et al. A randomized multicenter trial of crotalinae 
   polyvalent immune Fab (ovine) antivenom for the treatment for crotaline snakebite 
   in the United States. Arch Intern Med. 2001;161(16):2030-2036. 
   doi: 10.1001/archinternmed.2001.01080200068007.
3. Lavonas EJ, Gerardo CJ, O'Malley G, et al. Initial experience with Crotalidae 
   polyvalent immune Fab (ovine) antivenom in the treatment of copperhead snakebite. 
   Ann Emerg Med. 2004;43(2):200-206. doi: 10.1016/j.annemergmed.2003.08.008.

The Antivenom Dosing Algorithm is a unified treatment algorithm developed to assist 
with quick identification and management of patients who may benefit from treatment 
with Crotalidae Polyvalent Immune Fab (CroFab®). This algorithm is specifically for 
CroFab dosing in pit viper (crotaline) envenomations and should not be used for coral 
snakes or non-US indigenous snakes. The algorithm emphasizes achieving initial control 
through addressing all three components: arrest of local effects, resolution of systemic 
effects, and reduction of hematologic abnormalities.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class AntivenomDosingAlgorithmRequest(BaseModel):
    """
    Request model for Antivenom Dosing Algorithm
    
    This algorithm assists with CroFab dosing for pit viper (crotaline) snakebites including:
    - Rattlesnakes
    - Copperheads  
    - Cottonmouths/Water moccasins
    
    Clinical Assessment Parameters:
    
    Signs of Envenomation:
    - Local: Swelling, tenderness, redness, ecchymosis, or blebs at bite site
    - Hematologic: Elevated PT/INR, decreased fibrinogen or platelets
    - Systemic: Hypotension, bleeding beyond puncture site, refractory vomiting, 
      diarrhea, angioedema, neurotoxicity
    
    Severity Grades:
    - None: No signs of envenomation
    - Minimal: Local effects only, stable vital signs, normal coagulation
    - Moderate: Progressive local effects or mild systemic/hematologic effects
    - Severe: Severe local effects with tissue threat, significant systemic effects, 
      or severe coagulopathy
    
    Treatment Algorithm:
    - Initial dose: 4-6 vials (up to 12 for severe cases)
    - Additional dose: 4-6 vials if initial control not achieved in ~1 hour
    - Maintenance: 2 vials every 6 hours for 3 doses (at 6, 12, 18 hours)
    
    Contraindications/Exclusions:
    - Snakebites on head or neck
    - Snakebites causing rhabdomyolysis  
    - Anaphylaxis/anaphylactoid reactions to venom
    - Coral snake envenomation
    - Non-US indigenous snakes
    
    References (Vancouver style):
    1. Lavonas EJ, Ruha AM, Banner W, et al. Unified treatment algorithm for the management 
    of crotaline snakebite in the United States: results of an evidence-informed consensus 
    workshop. BMC Emerg Med. 2011;11:2. doi: 10.1186/1471-227X-11-2.
    2. Dart RC, Seifert SA, Boyer LV, et al. A randomized multicenter trial of crotalinae 
    polyvalent immune Fab (ovine) antivenom for the treatment for crotaline snakebite 
    in the United States. Arch Intern Med. 2001;161(16):2030-2036.
    3. Lavonas EJ, Gerardo CJ, O'Malley G, et al. Initial experience with Crotalidae 
    polyvalent immune Fab (ovine) antivenom in the treatment of copperhead snakebite. 
    Ann Emerg Med. 2004;43(2):200-206.
    """
    
    signs_of_envenomation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of any signs of envenomation including local effects (swelling, tenderness, redness, ecchymosis, blebs), hematologic effects (elevated PT/INR, decreased fibrinogen/platelets), or systemic effects (hypotension, bleeding, vomiting, neurotoxicity)",
        example="yes"
    )
    
    severity_grade: Literal["none", "minimal", "moderate", "severe"] = Field(
        ...,
        description="Clinical severity assessment: None (no signs), Minimal (local effects only, stable vitals, normal coagulation), Moderate (progressive local or mild systemic/hematologic effects), Severe (severe local effects, significant systemic effects, or severe coagulopathy)",
        example="moderate"
    )
    
    patient_weight_kg: float = Field(
        ...,
        description="Patient weight in kilograms. Note: CroFab dosing is the same for adult and pediatric patients based on clinical severity, not weight-based",
        ge=1.0,
        le=300.0,
        example=70.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "signs_of_envenomation": "yes",
                "severity_grade": "moderate", 
                "patient_weight_kg": 70.0
            }
        }


class AntivenomDosingAlgorithmResponse(BaseModel):
    """
    Response model for Antivenom Dosing Algorithm
    
    The algorithm provides initial CroFab dosing recommendations:
    - 0 vials: No treatment needed (no signs of envenomation)
    - 4-6 vials: Standard initial dose for minimal to moderate envenomation
    - 6-12 vials: Higher initial dose for severe envenomation
    
    Initial Control Definition (all three must be achieved):
    1. Arrest: Progression of local effects has stopped
    2. Resolve: Systemic effects are improving/resolving  
    3. Reduce: Hematologic abnormalities normalizing or trending toward normal
    
    Follow-up Care:
    - Monitor for recurrent coagulopathy up to 1-2 weeks
    - Bleeding precautions for 2 weeks (no contact sports, elective surgery, dental work)
    - Laboratory follow-up at 2-3 days and 5-7 days post-discharge
    - Return precautions for worsening swelling, abnormal bleeding, serum sickness symptoms
    
    Reference: Lavonas EJ, et al. BMC Emerg Med. 2011;11:2.
    """
    
    result: int = Field(
        ...,
        description="Initial dose of CroFab antivenom in vials (0 = no treatment needed, 4-6 = standard dose, 6-12 = higher dose for severe cases)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the dosing recommendation", 
        example="vials"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including administration instructions, monitoring requirements, and follow-up care",
        example="Administer 6 vials CroFab IV over 60 minutes. Monitor for initial control of envenomation: (1) arrest of local effects progression, (2) resolution of systemic effects, (3) reduction of hematologic abnormalities. If initial control not achieved in ~1 hour, administer additional 4-6 vials. Once initial control achieved, give maintenance doses of 2 vials every 6 hours for 3 doses (at 6, 12, and 18 hours). Contact poison control (1-800-222-1222)."
    )
    
    stage: str = Field(
        ...,
        description="Treatment category (No Treatment, Standard Initial Dose, Higher Initial Dose)",
        example="Standard Initial Dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the treatment category",
        example="Standard initial antivenom dose"
    )
    
    additional_info: Dict[str, Any] = Field(
        ...,
        description="Additional clinical information including maintenance dosing, poison control contact, and monitoring requirements",
        example={
            "maintenance_dose": "2 vials every 6 hours for 3 doses",
            "poison_control": "1-800-222-1222", 
            "monitoring_requirements": "Monitor for initial control in ~1 hour, may need additional 4-6 vials"
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 6,
                "unit": "vials",
                "interpretation": "Administer 6 vials CroFab IV over 60 minutes. Monitor for initial control of envenomation: (1) arrest of local effects progression, (2) resolution of systemic effects, (3) reduction of hematologic abnormalities. If initial control not achieved in ~1 hour, administer additional 4-6 vials. Once initial control achieved, give maintenance doses of 2 vials every 6 hours for 3 doses (at 6, 12, and 18 hours). Contact poison control (1-800-222-1222).",
                "stage": "Standard Initial Dose",
                "stage_description": "Standard initial antivenom dose",
                "additional_info": {
                    "maintenance_dose": "2 vials every 6 hours for 3 doses",
                    "poison_control": "1-800-222-1222",
                    "monitoring_requirements": "Monitor for initial control in ~1 hour, may need additional 4-6 vials"
                }
            }
        }
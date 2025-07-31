"""
Fomepizole Dosing Calculator Models

Request and response models for fomepizole dosing calculation.

References (Vancouver style):
1. Howland MA. Antidotes in Depth: Fomepizole. In: Nelson LS, Howland MA, Lewin NA, Smith SW, 
   Goldfrank LR, Hoffman RS, editors. Goldfrank's Toxicologic Emergencies. 11th ed. New York: 
   McGraw-Hill; 2019.
2. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of ethylene glycol poisoning. 
   N Engl J Med. 1999;340(11):832-838. doi: 10.1056/NEJM199903253401203.
3. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of methanol poisoning. 
   N Engl J Med. 2001;344(6):424-429. doi: 10.1056/NEJM200102083440605.
4. Antizol (fomepizole) package insert. Cumberland Pharmaceuticals Inc. Nashville, TN; 2020.

Fomepizole (4-methylpyrazole) is the antidote of choice for methanol and ethylene glycol poisoning. 
It competitively inhibits alcohol dehydrogenase, preventing the formation of toxic metabolites 
(formic acid from methanol, oxalic acid from ethylene glycol). This calculator provides dosing 
for different clinical scenarios including initial loading, maintenance, and hemodialysis considerations.

Clinical Indications:
- Methanol poisoning (blood level >20 mg/dL or suspected significant ingestion)
- Ethylene glycol poisoning (blood level >20 mg/dL or suspected significant ingestion)
- Diethylene glycol poisoning
- Prevention of toxic metabolite formation

NOT indicated for:
- Isopropyl alcohol poisoning (no toxic metabolites)
- Ethanol intoxication alone
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class FomepizoleDosingRequest(BaseModel):
    """
    Request model for Fomepizole Dosing Calculator
    
    Fomepizole dosing varies by clinical scenario:
    
    **Initial Loading Dose:**
    - 15 mg/kg IV over 30 minutes
    - Given as first dose for any suspected methanol/ethylene glycol poisoning
    
    **Maintenance Dosing (No Dialysis):**
    - First 4 doses (0-48 hours): 10 mg/kg IV q12h
    - After 48 hours: 15 mg/kg IV q12h
    - Continue until ethylene glycol/methanol undetectable or <20 mg/dL with normal pH
    
    **During Hemodialysis:**
    - 10 mg/kg IV q4h during dialysis sessions
    - OR continuous infusion 1.0-1.5 mg/kg/h during dialysis
    - Increased frequency needed due to drug removal by dialysis
    
    **Post-Hemodialysis Dosing:**
    - Depends on timing of last dose:
      * ≥6 hours since last dose: Give full dose at dialysis onset
      * 3-6 hours since last dose: Give scheduled dose at dialysis completion  
      * 1-3 hours since last dose: Give half dose at dialysis completion
      * <1 hour since last dose: No additional dose needed

    References (Vancouver style):
    1. Howland MA. Antidotes in Depth: Fomepizole. In: Nelson LS, Howland MA, Lewin NA, Smith SW, 
       Goldfrank LR, Hoffman RS, editors. Goldfrank's Toxicologic Emergencies. 11th ed. New York: 
       McGraw-Hill; 2019.
    2. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of ethylene glycol poisoning. 
       N Engl J Med. 1999;340(11):832-838. doi: 10.1056/NEJM199903253401203.
    3. Brent J, McMartin K, Phillips S, et al. Fomepizole for the treatment of methanol poisoning. 
       N Engl J Med. 2001;344(6):424-429. doi: 10.1056/NEJM200102083440605.
    """
    
    weight: float = Field(
        ...,
        description="Patient body weight in kilograms. Used for all dose calculations (doses are weight-based)",
        ge=1,
        le=300,
        example=70.0
    )
    
    clinical_scenario: Literal[
        "initial_loading", 
        "maintenance_no_dialysis", 
        "during_hemodialysis", 
        "post_hemodialysis"
    ] = Field(
        ...,
        description=(
            "Clinical scenario determining dosing protocol:\n"
            "• initial_loading: First dose (15 mg/kg)\n"
            "• maintenance_no_dialysis: Regular maintenance dosing\n"
            "• during_hemodialysis: Dosing during dialysis session\n"
            "• post_hemodialysis: Dosing after dialysis completion"
        ),
        example="initial_loading"
    )
    
    hours_since_last_dose: Optional[float] = Field(
        None,
        description=(  
            "Hours since last fomepizole dose. Required for hemodialysis scenarios to determine appropriate dosing:\n"
            "• ≥6 hours: Give full dose at dialysis onset\n"
            "• 3-6 hours: Give scheduled dose at completion\n"
            "• 1-3 hours: Give half dose at completion\n"
            "• <1 hour: No additional dose needed"
        ),
        ge=0,
        le=48,
        example=4.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight": 70.0,
                "clinical_scenario": "initial_loading",
                "hours_since_last_dose": None
            }
        }


class FomepizoleDosingResponse(BaseModel):
    """
    Response model for Fomepizole Dosing Calculator
    
    Provides calculated fomepizole dose with clinical guidance for administration.
    
    **Treatment Endpoints:**
    - Ethylene glycol or methanol concentrations undetectable
    - OR concentrations <20 mg/dL with patient asymptomatic and normal pH
    
    **Administration Details:**
    - All doses given IV over 30 minutes
    - Dilute in ≥100 mL of 0.9% saline or D5W
    - Monitor for side effects (nausea, dizziness, headache)
    
    **Contraindications:**
    - Known hypersensitivity to fomepizole or other pyrazoles
    
    Reference: Howland MA. Antidotes in Depth: Fomepizole. Goldfrank's Toxicologic Emergencies. 11th ed. 2019.
    """
    
    result: float = Field(
        ...,
        description="Calculated fomepizole dose in milligrams based on patient weight and clinical scenario",
        example=1050.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the calculated dose",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with administration guidance and dosing rationale",
        example="Fomepizole is the antidote of choice for methanol and ethylene glycol poisoning. It competitively inhibits alcohol dehydrogenase, preventing formation of toxic metabolites. Administer IV over 30 minutes in ≥100 mL diluent. Monitor for side effects and treatment endpoints. This is the initial loading dose of 15 mg/kg."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage or phase of treatment (Initial Loading Dose, Maintenance Dosing, etc.)",
        example="Initial Loading Dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the current treatment stage",
        example="First dose of fomepizole"
    )
    
    additional_info: str = Field(
        ...,
        description="Additional dosing information specific to the clinical scenario (maintenance schedules, dialysis considerations, etc.)",
        example="Initial loading dose. Administer IV over 30 minutes."
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1050.0,
                "unit": "mg",
                "interpretation": "Fomepizole is the antidote of choice for methanol and ethylene glycol poisoning. It competitively inhibits alcohol dehydrogenase, preventing formation of toxic metabolites. Administer IV over 30 minutes in ≥100 mL diluent. Monitor for side effects and treatment endpoints. This is the initial loading dose of 15 mg/kg.",
                "stage": "Initial Loading Dose",
                "stage_description": "First dose of fomepizole",
                "additional_info": "Initial loading dose. Administer IV over 30 minutes."
            }
        }
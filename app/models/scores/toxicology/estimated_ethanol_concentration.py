"""
Estimated Ethanol (and Toxic Alcohol) Serum Concentration Based on Ingestion Models

Request and response models for estimating serum concentration of alcohols based on ingestion.

References (Vancouver style):
1. Baselt RC. Disposition of toxic drugs and chemicals in man. 11th ed. 
   Seal Beach, CA: Biomedical Publications; 2017.
2. Barceloux DG, Bond GR, Krenzelok EP, Cooper H, Vale JA; American Academy of 
   Clinical Toxicology Ad Hoc Committee on the Treatment Guidelines for Methanol 
   Poisoning. American Academy of Clinical Toxicology practice guidelines on the 
   treatment of methanol poisoning. J Toxicol Clin Toxicol. 2002;40(4):415-46. 
   doi: 10.1081/clt-120006745.
3. Brent J, McMartin K, Phillips S, Aaron C, Kulig K; Methylpyrazole for Toxic 
   Alcohols Study Group. Fomepizole for the treatment of methanol poisoning. 
   N Engl J Med. 2001 Feb 8;344(6):424-9. doi: 10.1056/NEJM200102083440605.
4. Watson WA, Litovitz TL, Rodgers GC Jr, Klein-Schwartz W, Reid N, Youniss J, et al. 
   2004 annual report of the American Association of Poison Control Centers Toxic 
   Exposure Surveillance System. Am J Emerg Med. 2005 Sep;23(5):589-666. 
   doi: 10.1016/j.ajem.2005.05.001.

This calculator estimates serum concentration of ethanol and toxic alcohols based on 
the amount ingested and patient weight using volume of distribution principles. 
It provides critical information for toxicological assessment and treatment decisions 
in poisoning cases.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class EstimatedEthanolConcentrationRequest(BaseModel):
    """
    Request model for Estimated Ethanol (and Toxic Alcohol) Serum Concentration Calculator
    
    This calculator estimates serum concentration using the formula:
    [C] = Dose / (Vd × Weight)
    
    Where:
    - [C] = Serum concentration (mg/L)
    - Dose = Amount ingested (mg)
    - Vd = Volume of distribution (0.6 L/kg)
    - Weight = Patient body weight (kg)
    
    Supported Alcohol Types:
    1. Ethanol: Common alcoholic beverages, hand sanitizers
    2. Methanol: Windshield washer fluid, antifreeze, industrial solvents
    3. Ethylene Glycol: Automotive antifreeze, brake fluid
    4. Isopropanol: Rubbing alcohol, disinfectants
    
    Key Assumptions:
    - Complete alcohol absorption
    - Disregards metabolism/elimination
    - Standard volume of distribution (0.6 L/kg)
    - No volume contraction effects
    
    Treatment Thresholds:
    - Methanol: ≥20 mg/dL requires treatment
    - Ethylene glycol: ≥20 mg/dL requires treatment
    - Ethanol: >300 mg/dL potentially fatal
    
    References (Vancouver style):
    1. Baselt RC. Disposition of toxic drugs and chemicals in man. 11th ed. 
       Seal Beach, CA: Biomedical Publications; 2017.
    2. Barceloux DG, Bond GR, Krenzelok EP, Cooper H, Vale JA; American Academy of 
       Clinical Toxicology Ad Hoc Committee on the Treatment Guidelines for Methanol 
       Poisoning. American Academy of Clinical Toxicology practice guidelines on the 
       treatment of methanol poisoning. J Toxicol Clin Toxicol. 2002;40(4):415-46. 
       doi: 10.1081/clt-120006745.
    """
    
    alcohol_type: Literal["ethanol", "methanol", "ethylene_glycol", "isopropanol"] = Field(
        ...,
        description="Type of alcohol ingested. Ethanol (beverages, sanitizers), Methanol (windshield fluid), Ethylene glycol (antifreeze), Isopropanol (rubbing alcohol)",
        example="ethanol"
    )
    
    amount_ingested_ml: float = Field(
        ...,
        description="Amount of pure alcohol ingested in milliliters. If beverage alcohol, consider using alcohol_percentage parameter",
        ge=0,
        le=1000,
        example=50.0
    )
    
    weight_kg: float = Field(
        ...,
        description="Patient body weight in kilograms. Used to calculate volume of distribution (Vd = 0.6 L/kg × weight)",
        ge=1,
        le=300,
        example=70.0
    )
    
    alcohol_percentage: Optional[float] = Field(
        None,
        description="Percentage of alcohol in the consumed beverage (optional, defaults to 100% for pure alcohol). E.g., beer ~5%, wine ~12%, spirits ~40%",
        ge=0,
        le=100,
        example=40.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "alcohol_type": "ethanol",
                "amount_ingested_ml": 100.0,
                "weight_kg": 70.0,
                "alcohol_percentage": 40.0
            }
        }


class EstimatedEthanolConcentrationResponse(BaseModel):
    """
    Response model for Estimated Ethanol (and Toxic Alcohol) Serum Concentration Calculator
    
    Provides estimated serum concentrations and clinical interpretation based on alcohol type:
    
    Ethanol Interpretation:
    - <50 mg/dL: Mild intoxication (euphoria, mild impairment)
    - 50-100 mg/dL: Moderate intoxication (significant impairment, legal intoxication)
    - 100-300 mg/dL: Severe intoxication (risk of coma, respiratory depression)
    - >300 mg/dL: Life-threatening (high risk of death)
    
    Toxic Alcohol Interpretation:
    - Methanol/Ethylene Glycol ≥20 mg/dL: Requires immediate treatment with fomepizole and hemodialysis
    - Isopropanol: Monitor for CNS depression, supportive care usually sufficient
    
    Important Limitations:
    - Estimates are approximations only
    - Does not account for time since ingestion or metabolism
    - Actual concentrations may vary based on individual factors
    - Always obtain actual serum levels when possible
    - Use in conjunction with clinical assessment and osmolar gap
    
    Reference: Baselt RC. Disposition of toxic drugs and chemicals in man. 11th ed. 2017.
    """
    
    result: str = Field(
        ...,
        description="Calculation result status (calculated_concentration)",
        example="calculated_concentration"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for results (various units)",
        example="various"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including estimated concentration, toxicity assessment, and treatment recommendations",
        example="Estimated ethanol concentration: 112.6 mg/dL (24.5 mmol/L). Severe intoxication. Risk of respiratory depression, coma, and death. Requires immediate medical attention and intensive monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Clinical severity stage based on alcohol type and concentration",
        example="Severe Intoxication"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical stage",
        example="Severe effects"
    )
    
    concentration_mg_dl: float = Field(
        ...,
        description="Estimated serum concentration in mg/dL",
        example=112.6
    )
    
    concentration_mmol_l: float = Field(
        ...,
        description="Estimated serum concentration in mmol/L (converted using alcohol-specific factors)",
        example=24.5
    )
    
    alcohol_type: str = Field(
        ...,
        description="Type of alcohol for which concentration was calculated",
        example="ethanol"
    )
    
    amount_pure_alcohol_ml: float = Field(
        ...,
        description="Calculated amount of pure alcohol ingested in mL (accounting for alcohol percentage if provided)",
        example=40.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "calculated_concentration",
                "unit": "various",
                "interpretation": "Estimated ethanol concentration: 112.6 mg/dL (24.5 mmol/L). Severe intoxication. Risk of respiratory depression, coma, and death. Requires immediate medical attention and intensive monitoring.",
                "stage": "Severe Intoxication",
                "stage_description": "Severe effects",
                "concentration_mg_dl": 112.6,
                "concentration_mmol_l": 24.5,
                "alcohol_type": "ethanol",
                "amount_pure_alcohol_ml": 40.0
            }
        }
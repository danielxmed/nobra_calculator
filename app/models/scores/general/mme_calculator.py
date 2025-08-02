"""
Morphine Milligram Equivalents (MME) Calculator Models

Request and response models for MME calculation.

References (Vancouver style):
1. Dowell D, Haegerich TM, Chou R. CDC Guideline for Prescribing Opioids for Chronic 
   Pain--United States, 2016. JAMA. 2016;315(15):1624-45. doi: 10.1001/jama.2016.1464.
2. Centers for Disease Control and Prevention. CDC Clinical Practice Guideline for 
   Prescribing Opioids for Pain — United States, 2022. MMWR Recomm Rep. 2022;71(3):1-95. 
   doi: 10.15585/mmwr.rr7103a1.
3. Nielsen S, Degenhardt L, Hoban B, Gisev N. A synthesis of oral morphine equivalents 
   (OME) for opioid utilisation studies. Pharmacoepidemiol Drug Saf. 2016;25(6):733-7. 
   doi: 10.1002/pds.3945.

The MME Calculator converts multiple opioid medications to standardized morphine 
milligram equivalents for risk assessment and safe prescribing guidance. Based on 
CDC 2022 guidelines, it helps identify patients at increased risk for opioid overdose 
and guides clinical decision-making regarding opioid therapy management.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
import json


class OpioidMedication(BaseModel):
    """Individual opioid medication details"""
    
    medication: str = Field(
        ...,
        description="Opioid medication name (e.g., 'morphine', 'oxycodone', 'fentanyl_patch')",
        example="oxycodone"
    )
    
    dose: float = Field(
        ...,
        gt=0,
        description="Dose amount per administration (mg for most opioids, mcg/hr for patches)",
        example=15.0
    )
    
    frequency_per_day: float = Field(
        ...,
        gt=0,
        description="Number of doses per day (use 1 for continuous patches)",
        example=2.0
    )
    
    route: Optional[str] = Field(
        "oral",
        description="Route of administration (oral, iv, patch). Defaults to oral",
        example="oral"
    )


class MmeCalculatorRequest(BaseModel):
    """
    Request model for Morphine Milligram Equivalents (MME) Calculator
    
    The MME Calculator standardizes opioid dosing across different medications and routes 
    to assess overdose risk and guide safe prescribing practices. Based on CDC 2022 
    guidelines, it converts various opioids to oral morphine equivalents using established 
    conversion factors.
    
    Supported Opioids and Conversion Factors:
    - Morphine (oral): 1.0, (IV): 3.0
    - Oxycodone: 1.5
    - Hydrocodone: 1.0  
    - Codeine: 0.15
    - Fentanyl patch: 2.4 (mcg/hr to mg/day oral morphine)
    - Hydromorphone (oral): 4.0, (IV): 20.0
    - Oxymorphone (oral): 3.0, (IV): 10.0
    - Methadone: 4.0-12.0 (dose-dependent)
    - Tramadol: 0.1
    - Tapentadol: 0.4
    - Buprenorphine (patch): 12.6, (sublingual): 30.0
    
    Special Considerations:
    - Methadone has dose-dependent conversion factors (higher doses = higher factors)
    - Fentanyl and buprenorphine patches are dosed in mcg/hr
    - IV formulations have higher conversion factors than oral
    - Incomplete cross-tolerance may require dose reduction when rotating opioids
    
    Risk Interpretation:
    - <50 MME/day: Low risk, standard monitoring
    - 50-89 MME/day: Moderate risk, increased monitoring, consider naloxone
    - ≥90 MME/day: High risk, careful evaluation, naloxone essential
    
    Input Format:
    Provide medications as JSON string containing array of medication objects.
    Each medication must include: medication name, dose, frequency per day.
    Route is optional (defaults to oral).
    
    Example JSON:
    [
      {"medication": "oxycodone", "dose": 15, "frequency_per_day": 2, "route": "oral"},
      {"medication": "fentanyl_patch", "dose": 25, "frequency_per_day": 1, "route": "patch"}
    ]

    References (Vancouver style):
    1. Dowell D, Haegerich TM, Chou R. CDC Guideline for Prescribing Opioids for Chronic 
    Pain--United States, 2016. JAMA. 2016;315(15):1624-45. doi: 10.1001/jama.2016.1464.
    2. Centers for Disease Control and Prevention. CDC Clinical Practice Guideline for 
    Prescribing Opioids for Pain — United States, 2022. MMWR Recomm Rep. 2022;71(3):1-95. 
    doi: 10.15585/mmwr.rr7103a1.
    3. Nielsen S, Degenhardt L, Hoban B, Gisev N. A synthesis of oral morphine equivalents 
    (OME) for opioid utilisation studies. Pharmacoepidemiol Drug Saf. 2016;25(6):733-7. 
    doi: 10.1002/pds.3945.
    """
    
    opioid_medications: str = Field(
        ...,
        description="JSON array of opioid medications with dosing details. Format: [{\"medication\": \"oxycodone\", \"dose\": 15, \"frequency_per_day\": 2, \"route\": \"oral\"}]",
        example='[{"medication": "oxycodone", "dose": 15, "frequency_per_day": 2, "route": "oral"}, {"medication": "morphine", "dose": 30, "frequency_per_day": 1, "route": "oral"}]'
    )
    
    @validator('opioid_medications')
    def validate_medications_json(cls, v):
        """Validate that the medications string is valid JSON array"""
        try:
            medications = json.loads(v)
            if not isinstance(medications, list):
                raise ValueError("Medications must be a JSON array")
            if not medications:
                raise ValueError("At least one medication must be provided")
            
            # Validate each medication has required fields
            for i, med in enumerate(medications):
                if not isinstance(med, dict):
                    raise ValueError(f"Medication {i+1} must be an object")
                
                required_fields = ["medication", "dose", "frequency_per_day"]
                for field in required_fields:
                    if field not in med:
                        raise ValueError(f"Medication {i+1} missing required field: {field}")
                
                if not isinstance(med["dose"], (int, float)) or med["dose"] <= 0:
                    raise ValueError(f"Medication {i+1} dose must be a positive number")
                
                if not isinstance(med["frequency_per_day"], (int, float)) or med["frequency_per_day"] <= 0:
                    raise ValueError(f"Medication {i+1} frequency must be a positive number")
            
            return v
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for opioid medications")
    
    class Config:
        schema_extra = {
            "example": {
                "opioid_medications": '[{"medication": "oxycodone", "dose": 15, "frequency_per_day": 2, "route": "oral"}, {"medication": "morphine", "dose": 30, "frequency_per_day": 1, "route": "oral"}]'
            }
        }


class MmeCalculatorResponse(BaseModel):
    """
    Response model for Morphine Milligram Equivalents (MME) Calculator
    
    The MME Calculator provides total daily morphine milligram equivalents with risk-based 
    interpretation to guide opioid prescribing decisions and overdose prevention strategies.
    
    Risk Categories:
    - Low Risk (<50 MME/day): Standard monitoring and safety counseling recommended
    - Moderate Risk (50-89 MME/day): Increased monitoring, consider tapering, naloxone recommended  
    - High Risk (≥90 MME/day): Careful benefit-risk evaluation, naloxone essential, frequent monitoring
    
    Clinical Significance:
    - MME ≥50 mg/day associated with increased overdose risk
    - MME ≥90 mg/day associated with significantly increased overdose risk  
    - CDC recommends avoiding or carefully justifying doses ≥90 MME/day
    - Naloxone co-prescribing recommended for MME ≥50 mg/day
    - Consider tapering when MME ≥50 mg/day without clear benefit
    
    Important Considerations:
    - Conversion factors represent population averages, individual variation exists
    - Incomplete cross-tolerance may require dose reduction when rotating opioids
    - Use clinical judgment in addition to calculated MME
    - Monitor for signs of oversedation, respiratory depression, and opioid use disorder
    - Avoid concurrent benzodiazepines, alcohol, and other CNS depressants
    - Document rationale for high-dose opioid therapy
    
    Prescribing Guidelines:
    - Start with lowest effective dose and titrate carefully
    - Set realistic goals for pain and function
    - Reassess benefits and harms regularly
    - Consider non-opioid and non-pharmacologic therapies
    - Provide patient education on safe use, storage, and disposal
    - Use prescription drug monitoring programs
    
    Reference: CDC Clinical Practice Guideline for Prescribing Opioids for Pain — United States, 2022.
    """
    
    result: float = Field(
        ...,
        description="Total daily morphine milligram equivalents calculated from all opioid medications",
        example=60.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the MME calculation",
        example="mg/day morphine equivalents"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and risk-based recommendations for opioid therapy management",
        example="Total MME: 60.0 mg/day. Moderate-risk opioid dosing. Medications: oxycodone 30mg/day (MME: 45.0), morphine 30mg/day (MME: 30.0). Increased monitoring recommended. Consider tapering to lower doses if pain and function goals are not being met. Naloxone prescription strongly recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and monitoring recommendations",
        example="Increased monitoring recommended"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 60.0,
                "unit": "mg/day morphine equivalents",
                "interpretation": "Total MME: 60.0 mg/day. Moderate-risk opioid dosing. Medications: oxycodone 30mg/day (MME: 45.0), morphine 30mg/day (MME: 30.0). Increased monitoring recommended. Consider tapering to lower doses if pain and function goals are not being met. Naloxone prescription strongly recommended.",
                "stage": "Moderate Risk",
                "stage_description": "Increased monitoring recommended"
            }
        }
"""
Acetaminophen Overdose and NAC Dosing Models

Request and response models for calculating N-acetylcysteine (NAC) dosing 
for acetaminophen overdose and toxicity assessment using the Rumack-Matthew nomogram.

References (Vancouver style):
1. Rumack BH, Matthew H. Acetaminophen poisoning and toxicity. Pediatrics. 
   1975 Jun;55(6):871-6. PMID: 1134886.
2. Prescott LF, Illingworth RN, Critchley JA, Stewart MJ, Adam RD, Proudfoot AT. 
   Intravenous N-acetylcystine: the treatment of choice for paracetamol poisoning. 
   Br Med J. 1979 Nov 3;2(6198):1097-100. PMID: 519312.
3. Ershad M, Naji A, Patel P, Vearrier D. N-Acetylcysteine. [Updated 2024 Feb 29]. 
   In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2025 Jan-. 
   Available from: https://www.ncbi.nlm.nih.gov/books/NBK537183/
4. Hodgman MJ, Garrard AR. A review of acetaminophen poisoning. Crit Care Clin. 
   2012 Oct;28(4):499-516. doi: 10.1016/j.ccc.2012.07.006. PMID: 22998987.

NAC is the antidote for acetaminophen toxicity and is almost 100% effective when 
given within 8 hours of ingestion. The Rumack-Matthew nomogram helps determine 
the need for NAC treatment in single acute ingestions between 4-24 hours.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, Dict, Any


class AcetaminophenOverdoseNacRequest(BaseModel):
    """
    Request model for Acetaminophen Overdose and NAC Dosing Calculator
    
    This calculator provides NAC dosing for both IV (21-hour protocol) and oral 
    (72-hour protocol) routes. It can also assess toxicity risk using the 
    Rumack-Matthew nomogram when time of ingestion and acetaminophen level are provided.
    
    Route Selection:
    - IV: Preferred for established hepatic failure, intractable vomiting, or when rapid treatment needed
    - PO: Equally effective as IV, preferred when patient can tolerate oral medication
    
    Nomogram Assessment (optional):
    - Only valid for single acute ingestions
    - Requires both hours since ingestion (4-24h) and acetaminophen level
    - Treatment line at 4 hours = 150 mcg/mL, declining logarithmically
    
    Important Notes:
    - NAC should be started empirically if >8 hours post-ingestion while awaiting levels
    - Continue NAC until acetaminophen undetectable and transaminases normalizing
    - Monitor for anaphylactoid reactions with IV route (up to 18% incidence)
    
    References (Vancouver style):
    1. Rumack BH, Matthew H. Acetaminophen poisoning and toxicity. Pediatrics. 
       1975 Jun;55(6):871-6. PMID: 1134886.
    2. Ershad M, Naji A, Patel P, Vearrier D. N-Acetylcysteine. [Updated 2024 Feb 29]. 
       In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2025 Jan-.
    """
    
    route: Literal["IV", "PO"] = Field(
        ...,
        description="Route of N-acetylcysteine administration. IV uses 21-hour protocol, PO uses 72-hour protocol",
        example="IV"
    )
    
    weight: float = Field(
        ...,
        description="Patient weight in kilograms. Used to calculate NAC doses. Maximum doses apply for safety",
        example=70.0,
        ge=1,
        le=500
    )
    
    hours_since_ingestion: Optional[float] = Field(
        None,
        description="Hours since acetaminophen ingestion (4-24 hours). Required for nomogram assessment. Must be provided with acetaminophen_level",
        example=6.0,
        ge=4,
        le=24
    )
    
    acetaminophen_level: Optional[float] = Field(
        None,
        description="Serum acetaminophen level in mcg/mL. Required for nomogram assessment. Must be provided with hours_since_ingestion",
        example=180.0,
        ge=0,
        le=1000
    )
    
    @validator('acetaminophen_level')
    def validate_nomogram_parameters(cls, v, values):
        """Ensure both nomogram parameters are provided together"""
        hours = values.get('hours_since_ingestion')
        if (hours is None) != (v is None):
            raise ValueError("Both hours_since_ingestion and acetaminophen_level must be provided together for nomogram assessment")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "route": "IV",
                "weight": 70.0,
                "hours_since_ingestion": 6.0,
                "acetaminophen_level": 180.0
            }
        }


class DosingDetails(BaseModel):
    """Details for a specific dose in the protocol"""
    
    dose_mg: float = Field(..., description="Dose in milligrams")
    duration: Optional[str] = Field(None, description="Duration of infusion (IV only)")
    volume: Optional[str] = Field(None, description="Volume for dilution (IV only)")
    rate: Optional[str] = Field(None, description="Infusion rate (IV only)")
    timing: Optional[str] = Field(None, description="Timing of dose (PO only)")
    frequency: Optional[str] = Field(None, description="Frequency of doses (PO maintenance only)")
    number_of_doses: Optional[int] = Field(None, description="Number of doses (PO maintenance only)")
    start: Optional[str] = Field(None, description="When to start doses (PO maintenance only)")


class DosingRegimen(BaseModel):
    """Complete dosing regimen for NAC"""
    
    protocol: str = Field(..., description="Protocol name (21-hour IV or 72-hour oral)")
    loading_dose: DosingDetails = Field(..., description="Loading dose details")
    second_dose: Optional[DosingDetails] = Field(None, description="Second dose details (IV only)")
    third_dose: Optional[DosingDetails] = Field(None, description="Third dose details (IV only)")
    maintenance_dose: Optional[DosingDetails] = Field(None, description="Maintenance dose details (PO only)")
    total_dose_mg: float = Field(..., description="Total NAC dose over entire protocol")
    total_duration: str = Field(..., description="Total duration of protocol")
    administration_note: Optional[str] = Field(None, description="Special administration instructions")


class ToxicityAssessment(BaseModel):
    """Rumack-Matthew nomogram toxicity assessment"""
    
    hours_post_ingestion: float = Field(..., description="Hours since acetaminophen ingestion")
    acetaminophen_level: float = Field(..., description="Measured acetaminophen level in mcg/mL")
    treatment_line_level: float = Field(..., description="Treatment line level at given time in mcg/mL")
    above_treatment_line: bool = Field(..., description="Whether level is above treatment line")
    toxicity_risk: str = Field(..., description="Risk assessment based on nomogram")


class AcetaminophenOverdoseNacResponse(BaseModel):
    """
    Response model for Acetaminophen Overdose and NAC Dosing Calculator
    
    Provides complete NAC dosing regimen based on selected route and optional 
    toxicity assessment using the Rumack-Matthew nomogram.
    
    IV Protocol (21-hour):
    - Loading: 150 mg/kg over 60 min (max 15g)
    - Second: 50 mg/kg over 4 hours (max 5g)
    - Third: 100 mg/kg over 16 hours (max 10g)
    
    Oral Protocol (72-hour):
    - Loading: 140 mg/kg
    - Maintenance: 70 mg/kg every 4 hours × 17 doses
    
    Toxicity Assessment:
    - Above treatment line: Probable hepatotoxicity, NAC indicated
    - Below treatment line: Hepatotoxicity unlikely, NAC typically not needed
    
    Reference: Rumack BH, Matthew H. Pediatrics. 1975;55(6):871-6.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Complete NAC dosing regimen and optional toxicity assessment",
        example={
            "dosing_regimen": {
                "protocol": "21-hour IV protocol",
                "loading_dose": {"dose_mg": 10500.0, "duration": "60 minutes", "volume": "200 mL D5W", "rate": "10500.0 mg over 60 min"},
                "second_dose": {"dose_mg": 3500.0, "duration": "4 hours", "volume": "500 mL D5W", "rate": "875.0 mg/hr"},
                "third_dose": {"dose_mg": 7000.0, "duration": "16 hours", "volume": "1000 mL D5W", "rate": "437.5 mg/hr"},
                "total_dose_mg": 21000.0,
                "total_duration": "21 hours"
            },
            "toxicity_assessment": {
                "hours_post_ingestion": 6.0,
                "acetaminophen_level": 180.0,
                "treatment_line_level": 115.5,
                "above_treatment_line": True,
                "toxicity_risk": "Probable hepatotoxicity"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit type for this complex result",
        example="complex"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations",
        example="NAC dosing calculated for IV route. Use 21-hour protocol with careful monitoring for anaphylactoid reactions (up to 18% incidence). Patient's acetaminophen level (180.0 mcg/mL) is ABOVE the treatment line (115.5 mcg/mL) at 6.0 hours post-ingestion. Immediate NAC treatment is indicated. Continue NAC until acetaminophen undetectable and transaminases normalizing."
    )
    
    stage: str = Field(
        ...,
        description="Toxicity stage (Toxic, Non-toxic, or Dosing Only)",
        example="Toxic"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the toxicity assessment",
        example="Above treatment line - Probable hepatotoxicity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "dosing_regimen": {
                        "protocol": "21-hour IV protocol",
                        "loading_dose": {
                            "dose_mg": 10500.0,
                            "duration": "60 minutes",
                            "volume": "200 mL D5W",
                            "rate": "10500.0 mg over 60 min"
                        },
                        "second_dose": {
                            "dose_mg": 3500.0,
                            "duration": "4 hours",
                            "volume": "500 mL D5W",
                            "rate": "875.0 mg/hr"
                        },
                        "third_dose": {
                            "dose_mg": 7000.0,
                            "duration": "16 hours",
                            "volume": "1000 mL D5W",
                            "rate": "437.5 mg/hr"
                        },
                        "total_dose_mg": 21000.0,
                        "total_duration": "21 hours"
                    },
                    "toxicity_assessment": {
                        "hours_post_ingestion": 6.0,
                        "acetaminophen_level": 180.0,
                        "treatment_line_level": 115.5,
                        "above_treatment_line": True,
                        "toxicity_risk": "Probable hepatotoxicity"
                    }
                },
                "unit": "complex",
                "interpretation": "NAC dosing calculated for IV route. Use 21-hour protocol with careful monitoring for anaphylactoid reactions (up to 18% incidence). Patient's acetaminophen level (180.0 mcg/mL) is ABOVE the treatment line (115.5 mcg/mL) at 6.0 hours post-ingestion. Immediate NAC treatment is indicated. Continue NAC until acetaminophen undetectable and transaminases normalizing.",
                "stage": "Toxic",
                "stage_description": "Above treatment line - Probable hepatotoxicity"
            }
        }
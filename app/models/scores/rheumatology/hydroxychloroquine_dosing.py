"""
Hydroxychloroquine (Plaquenil) Dosing Calculator Models

Request and response models for Hydroxychloroquine dosing calculation.

References (Vancouver style):
1. Marmor MF, Kellner U, Lai TY, Melles RB, Mieler WF; American Academy of Ophthalmology. 
   Recommendations on Screening for Chloroquine and Hydroxychloroquine Retinopathy (2016 Revision). 
   Ophthalmology. 2016 Jun;123(6):1386-94. doi: 10.1016/j.ophtha.2016.01.058.
2. Melles RB, Marmor MF. The risk of toxic retinopathy in patients on long-term 
   hydroxychloroquine therapy. JAMA Ophthalmol. 2014 Dec;132(12):1453-60. 
   doi: 10.1001/jamaophthalmol.2014.3459.
3. Jorge AM, Melles RB, Zhang Y, Lu N, Rai SK, Young LH, Choi HK. Hydroxychloroquine 
   retinopathy--implications of research advances for rheumatology care. Nat Rev Rheumatol. 
   2018 Dec;14(12):693-703. doi: 10.1038/s41584-018-0111-8.

The Hydroxychloroquine Dosing Calculator determines safe daily dosing limits based on 
actual body weight to minimize retinopathy risk. The 2016 AAO guidelines recommend 
a maximum dose of 5 mg/kg/day (actual weight), reduced from the previous 6.5 mg/kg/day, 
after evidence showed significantly increased retinopathy risk at higher doses.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HydroxychloroquineDosingRequest(BaseModel):
    """
    Request model for Hydroxychloroquine (Plaquenil) Dosing Calculator
    
    The calculator uses three key parameters to determine safe dosing:
    
    1. Actual Body Weight: Used per 2016 AAO guidelines (preferred over ideal weight)
       - Maximum dose calculation: weight (kg) × 5 mg/kg = maximum daily dose (mg)
       - Actual weight provides better correlation with retinopathy risk
    
    2. Clinical Indication: Different conditions may require different dosing considerations
       - Rheumatoid Arthritis: Standard 200-400 mg daily for long-term use
       - Systemic Lupus Erythematosus: Standard 200-400 mg daily, monitor for flares
       - Malaria: Higher short-term doses acceptable (retinopathy risk minimal)
       - Other autoimmune conditions: Follow rheumatologic guidelines
    
    3. Risk Factors for Retinopathy:
       - Age >65 years
       - Renal disease (affects drug clearance)
       - Liver disease (affects drug metabolism)  
       - Previous retinal disease
       - Presence of any risk factor may warrant dose reduction
    
    Retinopathy Risk by Dosing:
    - ≤5 mg/kg/day: 2% risk at 10 years, 20% risk at 20 years
    - >5 mg/kg/day: 10% risk at 10 years, 40% risk at 20 years
    
    References (Vancouver style):
    1. Marmor MF, Kellner U, Lai TY, Melles RB, Mieler WF; American Academy of Ophthalmology. 
       Recommendations on Screening for Chloroquine and Hydroxychloroquine Retinopathy (2016 Revision). 
       Ophthalmology. 2016 Jun;123(6):1386-94. doi: 10.1016/j.ophtha.2016.01.058.
    2. Melles RB, Marmor MF. The risk of toxic retinopathy in patients on long-term 
       hydroxychloroquine therapy. JAMA Ophthalmol. 2014 Dec;132(12):1453-60. 
       doi: 10.1001/jamaophthalmol.2014.3459.
    """
    
    weight_kg: float = Field(
        ...,
        gt=20,
        le=300,
        description="Patient's actual body weight in kilograms. Used per 2016 AAO guidelines "
                   "(actual weight preferred over ideal weight). Range: 20-300 kg for practical "
                   "clinical use. Maximum dose = weight × 5 mg/kg/day.",
        example=70.0
    )
    
    indication: Literal[
        "rheumatoid_arthritis",
        "systemic_lupus_erythematosus",
        "malaria_prophylaxis", 
        "malaria_treatment",
        "other_autoimmune"
    ] = Field(
        ...,
        description="Clinical indication for hydroxychloroquine therapy. "
                   "rheumatoid_arthritis: Standard 200-400 mg daily for long-term use. "
                   "systemic_lupus_erythematosus: Standard 200-400 mg daily, monitor for disease flares. "
                   "malaria_prophylaxis: Short-term use, retinopathy risk minimal. "
                   "malaria_treatment: Short-term high-dose treatment, retinopathy risk minimal. "
                   "other_autoimmune: Follow rheumatologic dosing guidelines, consider specialist consultation.",
        example="rheumatoid_arthritis"
    )
    
    risk_factors: Literal["none", "one_or_more"] = Field(
        ...,
        description="Presence of risk factors for hydroxychloroquine retinopathy. Risk factors include: "
                   "age >65 years, renal disease, liver disease, previous retinal disease. "
                   "none: No risk factors present, standard dosing applies. "
                   "one_or_more: At least one risk factor present, consider dose reduction (15% reduction recommended).",
        example="none"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight_kg": 70.0,
                "indication": "rheumatoid_arthritis",
                "risk_factors": "none"
            }
        }


class HydroxychloroquineDosingResponse(BaseModel):
    """
    Response model for Hydroxychloroquine (Plaquenil) Dosing Calculator
    
    The calculator provides maximum safe daily dosing recommendations based on:
    - 2016 AAO guidelines: ≤5 mg/kg/day (actual weight)
    - Risk factor adjustments: 15% dose reduction if risk factors present
    - Practical tablet combinations: Rounded to achievable doses
    
    Retinopathy Risk Stratification:
    - Low risk (≤5 mg/kg): 2% at 10 years, 20% at 20 years
    - High risk (>5 mg/kg): 10% at 10 years, 40% at 20 years
    
    Monitoring Requirements:
    - Baseline ophthalmologic exam before starting therapy
    - Annual screening after 5 years of use (earlier if risk factors)
    - More frequent monitoring if dose >5 mg/kg or risk factors present
    
    Reference: Marmor MF, et al. Ophthalmology. 2016;123(6):1386-94.
    """
    
    result: float = Field(
        ...,
        ge=100,
        le=800,
        description="Maximum recommended daily dose of hydroxychloroquine in mg, "
                   "rounded to practical tablet combinations",
        example=350.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the dose",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with dose assessment, retinopathy risk, "
                   "and monitoring recommendations based on calculated dose and risk factors",
        example="Standard therapeutic dose within safety guidelines. Dose: 5.0 mg/kg/day. "
                "Annual eye exams after 5 years of use."
    )
    
    stage: str = Field(
        ...,
        description="Dose category (Low Dose, Standard Dose, or High Dose)",
        example="Standard Dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Dose range description for the calculated dose",
        example="201-400 mg daily"
    )
    
    dose_per_kg: float = Field(
        ...,
        ge=0.5,
        le=15.0,
        description="Calculated dose per kilogram of body weight (mg/kg/day). "
                   "Target: ≤5.0 mg/kg/day per 2016 AAO guidelines",
        example=5.0
    )
    
    retinopathy_risk_10_year: int = Field(
        ...,
        ge=0,
        le=100,
        description="Estimated 10-year retinopathy risk percentage based on dose per kg. "
                   "2% if ≤5 mg/kg/day, 10% if >5 mg/kg/day",
        example=2
    )
    
    retinopathy_risk_20_year: int = Field(
        ...,
        ge=0,
        le=100,
        description="Estimated 20-year retinopathy risk percentage based on dose per kg. "
                   "20% if ≤5 mg/kg/day, 40% if >5 mg/kg/day",
        example=20
    )
    
    dosing_schedule: str = Field(
        ...,
        description="Practical dosing schedule recommendation using standard tablet strengths "
                   "(200 mg, 300 mg, 400 mg tablets)",
        example="200 mg twice daily, or 400 mg once daily (single dose preferred)"
    )
    
    indication_notes: str = Field(
        ...,
        description="Indication-specific dosing considerations and recommendations",
        example="Standard dose 200-400 mg daily. Consider lower dose for long-term use."
    )
    
    requires_eye_exam: bool = Field(
        ...,
        description="Boolean indicating whether ophthalmologic monitoring is required (always true)",
        example=True
    )
    
    risk_adjusted: bool = Field(
        ...,
        description="Boolean indicating whether dose was adjusted downward due to risk factors",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 350.0,
                "unit": "mg",
                "interpretation": "Standard therapeutic dose within safety guidelines. "
                                "Dose: 5.0 mg/kg/day. Annual eye exams after 5 years of use.",
                "stage": "Standard Dose",
                "stage_description": "201-400 mg daily",
                "dose_per_kg": 5.0,
                "retinopathy_risk_10_year": 2,
                "retinopathy_risk_20_year": 20,
                "dosing_schedule": "200 mg twice daily, or 400 mg once daily (single dose preferred)",
                "indication_notes": "Standard dose 200-400 mg daily. Consider lower dose for long-term use.",
                "requires_eye_exam": True,
                "risk_adjusted": False
            }
        }
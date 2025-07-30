"""
Cryoprecipitate Dosing for Fibrinogen Replacement Models

Request and response models for cryoprecipitate dosing calculation.

References (Vancouver style):
1. American Association of Blood Banks (AABB). Technical Manual, 20th Edition. 
   Bethesda, MD: AABB Press; 2020.
2. British Committee for Standards in Haematology, Stainsby D, MacLennan S, 
   Thomas D, Isaac J, Hamilton PJ. Guidelines for the use of fresh-frozen plasma, 
   cryoprecipitate and cryosupernatant. Br J Haematol. 2004;126(1):11-28. 
   doi: 10.1111/j.1365-2141.2004.04972.x.
3. American Red Cross. Circular of Information for the Use of Human Blood and 
   Blood Components. American Red Cross, America's Blood Centers, and American 
   Association of Blood Banks; 2017.
4. Stanworth SJ, Brunskill SJ, Hyde CJ, McClelland DB, Murphy MF. Is fresh 
   frozen plasma clinically effective? A systematic review of randomized 
   controlled trials. Br J Haematol. 2004;126(1):139-152. 
   doi: 10.1111/j.1365-2141.2004.04973.x.

The cryoprecipitate dosing calculator determines the required dose of cryoprecipitate 
units needed to achieve target fibrinogen levels in patients with hypofibrinogenemia. 
It uses validated formulas based on plasma volume calculations and fibrinogen content 
per unit to provide precise dosing recommendations for clinical use.

Cryoprecipitate is a blood component containing concentrated fibrinogen, factor VIII, 
factor XIII, von Willebrand factor, and fibronectin. It is primarily used for 
fibrinogen replacement in patients with congenital or acquired hypofibrinogenemia, 
including those with massive bleeding, liver disease, or disseminated intravascular 
coagulation (DIC).
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Optional


class CryoprecipitateDosIngRequest(BaseModel):
    """
    Request model for Cryoprecipitate Dosing for Fibrinogen Replacement
    
    The cryoprecipitate dosing calculator uses the following validated formula:
    
    **Required Units = (Target Fibrinogen - Current Fibrinogen) × Plasma Volume / Fibrinogen per Unit**
    
    **Plasma Volume Calculation**:
    - Plasma Volume (dL) = Weight (kg) × Factor × (1 - Hematocrit)
    - Factor: 0.07 for males, 0.065 for females
    
    **Clinical Parameters**:
    
    **Patient Weight (kg)**:
    - Used for plasma volume calculation
    - Range: 1.0-300.0 kg
    - Essential for accurate dosing calculations
    
    **Patient Sex**:
    - Male: Plasma factor 0.07
    - Female: Plasma factor 0.065
    - Based on physiological differences in plasma volume distribution
    
    **Hematocrit (decimal)**:
    - Current hematocrit as decimal (0.40 for 40%)
    - Range: 0.15-0.65 (15-65%)
    - Used to calculate plasma volume from total blood volume
    
    **Current Fibrinogen (mg/dL)**:
    - Baseline fibrinogen level before replacement
    - Range: 0.0-1000.0 mg/dL
    - Critical threshold: <50 mg/dL requires urgent replacement
    
    **Target Fibrinogen (mg/dL)**:
    - Desired fibrinogen level after replacement
    - Range: 50.0-500.0 mg/dL
    - Standard targets: 150 mg/dL (hemostasis), 200 mg/dL (major bleeding/surgery)
    
    **Fibrinogen per Unit (mg)** (Optional):
    - Fibrinogen content per cryoprecipitate unit
    - Range: 150-300 mg (default: 200 mg)
    - Varies by blood bank and preparation method
    
    **Clinical Applications**:
    - Congenital fibrinogen disorders (afibrinogenemia, hypofibrinogenemia)
    - Acquired hypofibrinogenemia (liver disease, DIC, massive bleeding)
    - Surgical bleeding with low fibrinogen
    - Postpartum hemorrhage with hypofibrinogenemia
    - Trauma-induced coagulopathy
    
    **Dosing Guidelines**:
    - Standard adult dose: 10 pooled units (≈2000 mg fibrinogen)
    - Alternative: 1 unit per 5-10 kg body weight
    - Expected increase: 60-100 mg/dL per 10 units
    - Monitor response: Repeat levels 1-2 hours post-transfusion
    
    References (Vancouver style):
    1. American Association of Blood Banks (AABB). Technical Manual, 20th Edition. 
    Bethesda, MD: AABB Press; 2020.
    2. British Committee for Standards in Haematology, Stainsby D, MacLennan S, 
    Thomas D, Isaac J, Hamilton PJ. Guidelines for the use of fresh-frozen plasma, 
    cryoprecipitate and cryosupernatant. Br J Haematol. 2004;126(1):11-28. 
    doi: 10.1111/j.1365-2141.2004.04972.x.
    3. American Red Cross. Circular of Information for the Use of Human Blood and 
    Blood Components. American Red Cross, America's Blood Centers, and American 
    Association of Blood Banks; 2017.
    """
    
    patient_weight: float = Field(
        ...,
        ge=1.0,
        le=300.0,
        description="Patient weight in kilograms. Used for plasma volume calculation based on body mass and distribution factors",
        example=70.0
    )
    
    patient_sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex for plasma volume calculation. Males use factor 0.07, females use factor 0.065 based on physiological differences",
        example="female"
    )
    
    hematocrit: float = Field(
        ...,
        ge=0.15,
        le=0.65,
        description="Current hematocrit as decimal (e.g., 0.40 for 40%). Used to calculate plasma volume from total blood volume. Range: 15-65%",
        example=0.38
    )
    
    current_fibrinogen: float = Field(
        ...,
        ge=0.0,
        le=1000.0,
        description="Current fibrinogen level in mg/dL. Critical threshold <50 mg/dL requires urgent replacement. Normal range: 200-400 mg/dL",
        example=85.0
    )
    
    target_fibrinogen: float = Field(
        ...,
        ge=50.0,
        le=500.0,
        description="Target fibrinogen level in mg/dL. Standard targets: 150 mg/dL for hemostasis, 200 mg/dL for major bleeding or surgery",
        example=200.0
    )
    
    fibrinogen_per_unit: Optional[float] = Field(
        None,
        ge=150.0,
        le=300.0,
        description="Fibrinogen content per cryoprecipitate unit in mg. Typical range 150-250 mg, default 200 mg. Varies by blood bank preparation method",
        example=200.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "patient_weight": 70.0,
                "patient_sex": "female",
                "hematocrit": 0.38,
                "current_fibrinogen": 85.0,
                "target_fibrinogen": 200.0,
                "fibrinogen_per_unit": 200.0
            }
        }


class CryoprecipitateDosingResponse(BaseModel):
    """
    Response model for Cryoprecipitate Dosing for Fibrinogen Replacement
    
    The cryoprecipitate dosing calculator provides comprehensive dosing recommendations 
    based on validated formulas and clinical guidelines. Results include the calculated 
    dose, detailed breakdown of calculations, clinical considerations, and alternative 
    dosing methods for comparison.
    
    **Dose Categories**:
    - **Low Dose** (1-5 units): Small fibrinogen replacement, monitor response
    - **Standard Dose** (6-15 units): Typical therapeutic replacement, consider pooled units
    - **High Dose** (16-30 units): Large replacement, consider fibrinogen concentrate
    - **Very High Dose** (>30 units): Massive replacement, strongly consider alternatives
    
    **Clinical Monitoring**:
    - Repeat fibrinogen levels 1-2 hours post-transfusion
    - Monitor for volume overload in large doses
    - Ensure ABO compatibility when possible
    - Watch for transfusion reactions
    
    **Administration Considerations**:
    - Each unit is approximately 15-20 mL volume
    - Pooled units (10 units) for convenience
    - Ensure adequate vascular access for large doses
    - Consider fibrinogen concentrate for massive requirements
    
    Reference: American Association of Blood Banks (AABB). Technical Manual, 20th Edition. 2020.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=200,
        description="Number of cryoprecipitate units required to achieve target fibrinogen level (rounded up to whole units)",
        example=13
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the dosing recommendation",
        example="units"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with dosing category and recommendations for administration and monitoring",
        example="Calculated dose of 13 cryoprecipitate units represents standard therapeutic replacement. Consider using pooled units (typically 10 units per pool) for efficient administration. This dose should increase fibrinogen from 85.0 to approximately 200.0 mg/dL."
    )
    
    stage: str = Field(
        ...,
        description="Dosing category (Low Dose, Standard Dose, High Dose, Very High Dose)",
        example="Standard Dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the dosing category",
        example="Typical therapeutic replacement"
    )
    
    calculation_details: Dict[str, float] = Field(
        ...,
        description="Detailed breakdown of calculations including plasma volume, fibrinogen requirements, and exact units calculated",
        example={
            "plasma_volume_dL": 27.3,
            "fibrinogen_increase_needed": 115.0,
            "total_fibrinogen_needed_mg": 3140.0,
            "fibrinogen_per_unit_mg": 200.0,
            "exact_units_calculated": 15.7
        }
    )
    
    clinical_considerations: Dict[str, Any] = Field(
        ...,
        description="Clinical considerations including monitoring recommendations, administration guidance, and special precautions",
        example={
            "monitoring": "Repeat fibrinogen levels 1-2 hours post-transfusion",
            "administration": "Cryoprecipitate should be ABO compatible when possible",
            "special_considerations": [
                "Target appropriate for major bleeding or surgery",
                "Monitor response with repeat fibrinogen levels 1-2 hours post-transfusion",
                "Each unit is approximately 15-20 mL volume",
                "Consider requesting 1 pooled unit (10 units) for convenience"
            ],
            "volume_consideration": "Total volume approximately 228 mL"
        }
    )
    
    alternative_dosing: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Alternative dosing methods for comparison including weight-based approaches and simple rules",
        example={
            "weight_based_5kg": {
                "units": 14,
                "description": "1 unit per 5 kg (increases fibrinogen ~100 mg/dL)",
                "note": "Simple weight-based dosing method"
            },
            "weight_based_10kg": {
                "units": 7,
                "description": "1 unit per 10 kg (increases fibrinogen ~60-100 mg/dL)",
                "note": "Conservative weight-based dosing method"
            },
            "simple_rule": {
                "units": 16,
                "description": "0.2 × weight × (target increase/100)",
                "note": "Simple calculation rule for comparison"
            },
            "standard_adult_dose": {
                "units": 10,
                "description": "Standard adult dose (1 pooled unit)",
                "note": "Typical starting dose for adults, increases fibrinogen ~50-100 mg/dL"
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 13,
                "unit": "units",
                "interpretation": "Calculated dose of 13 cryoprecipitate units represents standard therapeutic replacement. Consider using pooled units (typically 10 units per pool) for efficient administration. This dose should increase fibrinogen from 85.0 to approximately 200.0 mg/dL.",
                "stage": "Standard Dose",
                "stage_description": "Typical therapeutic replacement",
                "calculation_details": {
                    "plasma_volume_dL": 27.3,
                    "fibrinogen_increase_needed": 115.0,
                    "total_fibrinogen_needed_mg": 3140.0,
                    "fibrinogen_per_unit_mg": 200.0,
                    "exact_units_calculated": 15.7
                },
                "clinical_considerations": {
                    "monitoring": "Repeat fibrinogen levels 1-2 hours post-transfusion",
                    "administration": "Cryoprecipitate should be ABO compatible when possible",
                    "special_considerations": [
                        "Target appropriate for major bleeding or surgery",
                        "Monitor response with repeat fibrinogen levels 1-2 hours post-transfusion",
                        "Each unit is approximately 15-20 mL volume",
                        "Consider requesting 1 pooled unit (10 units) for convenience"
                    ],
                    "volume_consideration": "Total volume approximately 228 mL"
                },
                "alternative_dosing": {
                    "weight_based_5kg": {
                        "units": 14,
                        "description": "1 unit per 5 kg (increases fibrinogen ~100 mg/dL)",
                        "note": "Simple weight-based dosing method"
                    },
                    "weight_based_10kg": {
                        "units": 7,
                        "description": "1 unit per 10 kg (increases fibrinogen ~60-100 mg/dL)",
                        "note": "Conservative weight-based dosing method"
                    },
                    "simple_rule": {
                        "units": 16,
                        "description": "0.2 × weight × (target increase/100)",
                        "note": "Simple calculation rule for comparison"
                    },
                    "standard_adult_dose": {
                        "units": 10,
                        "description": "Standard adult dose (1 pooled unit)",
                        "note": "Typical starting dose for adults, increases fibrinogen ~50-100 mg/dL"
                    }
                }
            }
        }
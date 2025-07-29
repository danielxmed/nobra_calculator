"""
Blood Volume Calculation Models

Request and response models for blood volume calculation using Nadler equations.

References (Vancouver style):
1. Nadler SB, Hidalgo JH, Bloch T. Prediction of blood volume in normal human adults. 
   Surgery. 1962 Feb;51(2):224-32.
2. Gilcher RO, McCombs JS. Blood volume and red cell mass measurements. In: Hillman RS, 
   Ault KA, Rinder HM, editors. Hematology in Clinical Practice. 4th ed. New York: 
   McGraw-Hill; 2005. p. 595-605. doi: 10.1036/0071422978.
3. International Council for Standardization in Haematology. Recommended methods for 
   measurement of red-cell and plasma volume. J Nucl Med. 1980 Aug;21(8):793-800. 
   doi: 10.2967/jnumed.21.8.793.

The blood volume calculation methods implemented here are based on the seminal 
work by Nadler, Hidalgo, and Bloch in 1962, who used radioisotope labeling 
techniques to establish predictive equations for blood volume in normal adults. 
These equations correlate patient sex, height, and weight with total blood volume, 
providing the foundation for modern clinical blood volume estimation.

For pediatric patients, age-specific weight-based calculations are used, recognizing 
that blood volume per kilogram of body weight varies significantly with age and 
development. These values were established through extensive clinical studies and 
represent standard practice in pediatric hematology and transfusion medicine.

The calculations are essential for various clinical applications including 
transfusion therapy planning, plasma exchange procedures, coagulation factor 
dosing, and research protocols requiring accurate blood volume estimates.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, Dict, Any


class BloodVolumeCalculationRequest(BaseModel):
    """
    Request model for Blood Volume Calculation
    
    This calculator provides estimates for total blood volume, red blood cell volume, 
    and plasma volume using established clinical formulas:
    
    **Calculation Methods:**
    
    **1. Nadler Equations (Adults and Children ≥25 kg):**
    Used for patients with sufficient size where height and weight relationships 
    are well-established. Requires sex, height, and weight inputs.
    
    **Male Formula:**
    Total Blood Volume (L) = 0.3669 × height³ + 0.03219 × weight + 0.6041
    
    **Female Formula:**
    Total Blood Volume (L) = 0.3561 × height³ + 0.03308 × weight + 0.1833
    
    **2. Weight-Based Calculations (Pediatric Patients <25 kg):**
    Age-specific multipliers based on developmental physiology:
    
    - **Preterm Neonate**: 100 mL/kg (higher blood volume due to immature systems)
    - **Term Neonate**: 85 mL/kg (standard newborn blood volume)
    - **Infant (1-4 months)**: 75 mL/kg (decreasing relative blood volume)
    - **Child (<25 kg)**: 70 mL/kg (approaching adult proportions)
    
    **Additional Volume Calculations:**
    
    **Red Blood Cell Volume:**
    RBC Volume = Total Blood Volume × (Hematocrit ÷ 100)
    
    **Plasma Volume:**
    Plasma Volume = Total Blood Volume × (1 - Hematocrit ÷ 100)
    
    **Clinical Applications:**
    
    **Transfusion Medicine:**
    - Blood product dosing calculations
    - Massive transfusion protocols
    - Pediatric transfusion volume limits
    - Exchange transfusion planning
    
    **Therapeutic Procedures:**
    - Plasma exchange volume calculations
    - Therapeutic phlebotomy planning
    - Coagulation factor concentrate dosing
    - Immunoglobulin replacement therapy
    
    **Research Applications:**
    - Pharmacokinetic studies
    - Blood sampling volume limits
    - Clinical trial safety protocols
    - Physiological research
    
    **Parameter Guidelines:**
    
    **Patient Category Selection:**
    Choose the appropriate category based on age and weight:
    - Use pediatric categories for patients <25 kg regardless of age
    - Use adult equations for patients ≥25 kg regardless of age
    - Consider gestational age for neonates (preterm vs term)
    
    **Measurement Requirements:**
    - Weight: Actual body weight in kilograms
    - Height: Standing height in centimeters (for Nadler equations)
    - Hematocrit: Recent laboratory value as percentage
    
    References (Vancouver style):
    1. Nadler SB, Hidalgo JH, Bloch T. Prediction of blood volume in normal human adults. 
    Surgery. 1962 Feb;51(2):224-32.
    2. Gilcher RO, McCombs JS. Blood volume and red cell mass measurements. In: Hillman RS, 
    Ault KA, Rinder HM, editors. Hematology in Clinical Practice. 4th ed. New York: 
    McGraw-Hill; 2005. p. 595-605. doi: 10.1036/0071422978.
    3. International Council for Standardization in Haematology. Recommended methods for 
    measurement of red-cell and plasma volume. J Nucl Med. 1980 Aug;21(8):793-800. 
    doi: 10.2967/jnumed.21.8.793.
    """
    
    patient_category: Literal[
        "preterm_neonate", 
        "term_neonate", 
        "infant_1_4_months", 
        "child_under_25kg", 
        "adult_or_child_25kg_plus"
    ] = Field(
        ...,
        description="Patient age/weight category determining calculation method. Pediatric categories use mL/kg multipliers, adult category uses Nadler equations.",
        example="adult_or_child_25kg_plus"
    )
    
    weight: float = Field(
        ...,
        ge=0.5,
        le=300,
        description="Patient weight in kilograms. Used in all calculation methods.",
        example=70.0
    )
    
    sex: Optional[Literal["male", "female"]] = Field(
        None,
        description="Patient sex (required for adults/children ≥25 kg using Nadler equations). Different equations for males and females.",
        example="male"
    )
    
    height: Optional[float] = Field(
        None,
        ge=30,
        le=250,
        description="Patient height in centimeters (required for adults/children ≥25 kg using Nadler equations). Converted to meters for calculation.",
        example=175.0
    )
    
    hematocrit: Optional[float] = Field(
        None,
        ge=10,
        le=70,
        description="Hematocrit percentage (optional). Required for calculating RBC and plasma volumes separately.",
        example=42.0
    )
    
    @field_validator('sex', 'height')
    @classmethod
    def validate_adult_requirements(cls, v, info):
        """Validate that sex and height are provided for adult calculations"""
        if info.data.get('patient_category') == 'adult_or_child_25kg_plus':
            if v is None:
                field_name = info.field_name
                raise ValueError(f'{field_name} is required for adults/children ≥25 kg')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_category": "adult_or_child_25kg_plus",
                "weight": 70.0,
                "sex": "male",
                "height": 175.0,
                "hematocrit": 42.0
            }
        }


class BloodVolumeCalculationResponse(BaseModel):
    """
    Response model for Blood Volume Calculation
    
    Returns calculated blood volume components based on input parameters:
    
    **Total Blood Volume:**
    The complete volume of blood circulating in the body, calculated using either 
    Nadler equations (adults/children ≥25 kg) or age-specific multipliers 
    (pediatric patients <25 kg).
    
    **Red Blood Cell Volume:**
    The cellular component of blood, calculated when hematocrit is provided.
    Essential for transfusion planning and anemia assessment.
    
    **Plasma Volume:**
    The liquid component of blood, calculated when hematocrit is provided.
    Important for plasma exchange procedures and coagulation factor dosing.
    
    **Clinical Interpretation:**
    Results are provided with clinical context including volume per kilogram 
    of body weight and specific applications for transfusion medicine and 
    therapeutic procedures.
    
    **Normal Reference Values:**
    - Adult males: ~70 mL/kg total blood volume
    - Adult females: ~65 mL/kg total blood volume
    - Neonates: 85-100 mL/kg depending on gestational age
    - Children: 70-75 mL/kg depending on age
    
    Reference: Nadler SB, et al. Surgery. 1962;51(2):224-32.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Blood volume calculation results including total, RBC, and plasma volumes",
        example={
            "total_blood_volume": 4900.0,
            "rbc_volume": 2058.0,
            "plasma_volume": 2842.0
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for blood volumes",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with volume calculations and clinical applications",
        example="Total blood volume: 4900.0 mL (70.0 mL/kg). RBC volume: 2058.0 mL. Plasma volume: 2842.0 mL. Calculation based on Nadler equations using height, weight, and sex. These estimates guide transfusion therapy, plasma exchange procedures, and coagulation factor dosing decisions."
    )
    
    stage: str = Field(
        ...,
        description="Result category",
        example="Blood Volume Results"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the calculation results",
        example="Calculated blood volume components"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "total_blood_volume": 4900.0,
                    "rbc_volume": 2058.0,
                    "plasma_volume": 2842.0
                },
                "unit": "mL",
                "interpretation": "Total blood volume: 4900.0 mL (70.0 mL/kg). RBC volume: 2058.0 mL. Plasma volume: 2842.0 mL. Calculation based on Nadler equations using height, weight, and sex. These estimates guide transfusion therapy, plasma exchange procedures, and coagulation factor dosing decisions.",
                "stage": "Blood Volume Results",
                "stage_description": "Calculated blood volume components"
            }
        }
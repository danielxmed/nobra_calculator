"""
Fleischner Society Guidelines for Incidental Pulmonary Nodules Models

Request and response models for Fleischner Guidelines calculation.

References (Vancouver style):
1. MacMahon H, Naidich DP, Goo JM, Lee KS, Leung ANC, Mayo JR, et al. Guidelines for 
   Management of Incidental Pulmonary Nodules Detected on CT Images: From the Fleischner 
   Society 2017. Radiology. 2017 Jul;284(1):228-243. doi: 10.1148/radiol.2017161659.
2. Bankier AA, MacMahon H, Goo JM, Rubin GD, Schaefer-Prokop CM, Naidich DP. 
   Recommendations for Measuring Pulmonary Nodules at CT: A Statement from the 
   Fleischner Society. Radiology. 2017 Nov;285(2):584-600. doi: 10.1148/radiol.2017162894.

The 2017 Fleischner Society Guidelines provide evidence-based recommendations for the 
management of incidentally detected pulmonary nodules on CT imaging. These guidelines 
help reduce unnecessary follow-up examinations while ensuring appropriate management 
of potentially malignant nodules.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class FleischnerGuidelinesRequest(BaseModel):
    """
    Request model for Fleischner Society Guidelines for Incidental Pulmonary Nodules
    
    The 2017 Fleischner Guidelines provide follow-up recommendations based on:
    
    Nodule Type:
    - solid: Solid nodules with soft tissue attenuation
    - subsolid: Ground glass or part-solid nodules
    
    Nodule Number:
    - single: Solitary nodule
    - multiple: Multiple nodules (use size of largest)
    
    Size Categories:
    - less_than_6mm: <6 mm (<100 mm³)
    - 6_to_8mm: 6-8 mm (100-250 mm³)
    - greater_than_8mm: >8 mm (>250 mm³)
    
    Risk Level:
    - low: Minimal or no smoking history, no other risk factors
    - high: Heavy smoking history, family history, upper lobe location, 
            spiculation, older age, emphysema, pulmonary fibrosis
    
    Subsolid Features (if applicable):
    - ground_glass: Pure ground glass opacity
    - part_solid: Mixed ground glass and solid components
    
    Important Notes:
    - Guidelines apply to patients ≥35 years old
    - Not for lung cancer screening
    - Not for patients with known cancer or immunosuppression
    - Size measured as average of long and short axis for nodules <10mm

    References (Vancouver style):
    1. MacMahon H, Naidich DP, Goo JM, Lee KS, Leung ANC, Mayo JR, et al. Guidelines for 
    Management of Incidental Pulmonary Nodules Detected on CT Images: From the Fleischner 
    Society 2017. Radiology. 2017 Jul;284(1):228-243. doi: 10.1148/radiol.2017161659.
    2. Bankier AA, MacMahon H, Goo JM, Rubin GD, Schaefer-Prokop CM, Naidich DP. 
    Recommendations for Measuring Pulmonary Nodules at CT: A Statement from the 
    Fleischner Society. Radiology. 2017 Nov;285(2):584-600. doi: 10.1148/radiol.2017162894.
    """
    
    nodule_type: Literal["solid", "subsolid"] = Field(
        ...,
        description="Type of pulmonary nodule. Solid nodules have soft tissue attenuation, while subsolid nodules include ground glass and part-solid nodules",
        example="solid"
    )
    
    nodule_number: Literal["single", "multiple"] = Field(
        ...,
        description="Number of nodules. For multiple nodules, use the size of the largest nodule",
        example="single"
    )
    
    size_category: Literal["less_than_6mm", "6_to_8mm", "greater_than_8mm"] = Field(
        ...,
        description="Size category of the nodule (or largest nodule if multiple). Size should be measured as average of long and short axis for nodules <10mm",
        example="6_to_8mm"
    )
    
    risk_level: Literal["low", "high"] = Field(
        ...,
        description="Patient risk level. Low risk: minimal/no smoking history, no other risk factors. High risk: heavy smoking, family history, upper lobe, spiculation, older age, emphysema, fibrosis",
        example="low"
    )
    
    subsolid_features: Optional[Literal["ground_glass", "part_solid"]] = Field(
        None,
        description="Features of subsolid nodule (required only if nodule_type is 'subsolid'). Ground glass: pure ground glass opacity. Part solid: mixed ground glass and solid components",
        example="ground_glass"
    )
    
    @validator('subsolid_features')
    def validate_subsolid_features(cls, v, values):
        """Ensure subsolid_features is provided when nodule_type is subsolid"""
        if values.get('nodule_type') == 'subsolid' and v is None:
            # Default to ground_glass if not specified
            return 'ground_glass'
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "nodule_type": "solid",
                "nodule_number": "single",
                "size_category": "6_to_8mm",
                "risk_level": "low"
            }
        }


class FleischnerGuidelinesResponse(BaseModel):
    """
    Response model for Fleischner Society Guidelines for Incidental Pulmonary Nodules
    
    The response provides specific follow-up recommendations based on the 2017 
    Fleischner Society Guidelines. These evidence-based recommendations help balance 
    the risk of missing early lung cancer against the risks and costs of unnecessary 
    follow-up examinations.
    
    Reference: MacMahon H, et al. Radiology. 2017;284(1):228-243.
    """
    
    result: str = Field(
        ...,
        description="Follow-up recommendation based on Fleischner Society Guidelines",
        example="CT at 6-12 months, then consider CT at 18-24 months"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for recommendations)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed interpretation including nodule characteristics, risk level, and management recommendations",
        example="For single solid nodule(s) 6 to 8 mm in low risk (minimal/no smoking, no other risk factors) patient: CT at 6-12 months, then consider CT at 18-24 months."
    )
    
    stage: str = Field(
        ...,
        description="Risk category and follow-up requirement",
        example="Intermediate risk - Follow-up recommended"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of nodule type and size",
        example="Solid nodule, 6 to 8 mm"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "CT at 6-12 months, then consider CT at 18-24 months",
                "unit": "",
                "interpretation": "For single solid nodule(s) 6 to 8 mm in low risk (minimal/no smoking, no other risk factors) patient: CT at 6-12 months, then consider CT at 18-24 months.",
                "stage": "Intermediate risk - Follow-up recommended",
                "stage_description": "Solid nodule, 6 to 8 mm"
            }
        }
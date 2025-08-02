"""
US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia (FH) Models

Request and response models for US MEDPED FH diagnostic criteria calculation.

References (Vancouver style):
1. Williams RR, Hunt SC, Schumacher MC, et al. Diagnosing heterozygous familial 
   hypercholesterolemia using new practical criteria focused on the family history. 
   Am J Cardiol. 1993;72(2):171-176.
2. Stone NJ, Levy RI, Fredrickson DS, Verter J. Coronary artery disease in 116 kindred 
   with familial type II hyperlipoproteinemia. Circulation. 1974;49(3):476-488.
3. MEDPED Program. Make Early Diagnosis to Prevent Early Death (MEDPED). University of Utah. 
   Available at: https://www.medped.org/

The US MEDPED (Make Early Diagnosis to Prevent Early Death) diagnostic criteria for 
familial hypercholesterolemia provide a simplified approach to FH diagnosis using only 
total cholesterol levels and family history. These criteria use age-specific cholesterol 
cutoffs that are lower when there is a family history of FH.

Age-specific cholesterol cutoffs (mg/dL):
- Age <20: General population 270, 1st degree 220, 2nd degree 230, 3rd degree 240
- Age 20-29: General population 290, 1st degree 240, 2nd degree 250, 3rd degree 260  
- Age 30-39: General population 340, 1st degree 270, 2nd degree 280, 3rd degree 290
- Age ≥40: General population 360, 1st degree 290, 2nd degree 300, 3rd degree 310

Family history definitions:
- 1st degree: Parents, siblings, children
- 2nd degree: Grandparents, aunts, uncles, half-siblings, nephews, nieces
- 3rd degree: Great-grandparents, great-aunts, great-uncles, first cousins

Clinical utility:
- Simpler to apply than Dutch Lipid Clinic Network criteria
- Designed for population screening and early diagnosis
- Lower sensitivity but higher specificity than some other FH criteria
- Useful in settings where genetic testing is not readily available
"""

from pydantic import BaseModel, Field
from typing import Literal


class UsMedpedFhCriteriaRequest(BaseModel):
    """
    Request model for US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia
    
    The US MEDPED criteria diagnose FH using age-specific total cholesterol cutoffs that 
    vary based on family history of FH. This simplified approach requires only:
    1. Patient age
    2. Total cholesterol level (mg/dL)
    3. Family history of FH in relatives
    
    Age Groups and Cholesterol Cutoffs (mg/dL):
    
    Age <20 years:
    - No family history: ≥270 mg/dL
    - 1st degree relative with FH: ≥220 mg/dL  
    - 2nd degree relative with FH: ≥230 mg/dL
    - 3rd degree relative with FH: ≥240 mg/dL
    
    Age 20-29 years:
    - No family history: ≥290 mg/dL
    - 1st degree relative with FH: ≥240 mg/dL
    - 2nd degree relative with FH: ≥250 mg/dL
    - 3rd degree relative with FH: ≥260 mg/dL
    
    Age 30-39 years:
    - No family history: ≥340 mg/dL
    - 1st degree relative with FH: ≥270 mg/dL
    - 2nd degree relative with FH: ≥280 mg/dL
    - 3rd degree relative with FH: ≥290 mg/dL
    
    Age ≥40 years:
    - No family history: ≥360 mg/dL
    - 1st degree relative with FH: ≥290 mg/dL
    - 2nd degree relative with FH: ≥300 mg/dL
    - 3rd degree relative with FH: ≥310 mg/dL
    
    Diagnosis: FH is diagnosed if total cholesterol meets or exceeds the age and 
    family history-specific cutoff value.
    
    References (Vancouver style):
    1. Williams RR, Hunt SC, Schumacher MC, et al. Diagnosing heterozygous familial 
    hypercholesterolemia using new practical criteria focused on the family history. 
    Am J Cardiol. 1993;72(2):171-176.
    2. Stone NJ, Levy RI, Fredrickson DS, Verter J. Coronary artery disease in 116 kindred 
    with familial type II hyperlipoproteinemia. Circulation. 1974;49(3):476-488.
    """
    
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient's age in years. Used to determine age-specific cholesterol cutoff values",
        example=35
    )
    
    total_cholesterol_mg_dl: float = Field(
        ...,
        ge=50,
        le=1000,
        description="Total cholesterol level in mg/dL. Must be fasting measurement for accurate diagnosis",
        example=320
    )
    
    family_history: Literal["none", "1st_degree", "2nd_degree", "3rd_degree"] = Field(
        ...,
        description="Family history of familial hypercholesterolemia. 1st degree: parents/siblings/children, 2nd degree: grandparents/aunts/uncles/half-siblings, 3rd degree: great-grandparents/first cousins, none: no known family history",
        example="1st_degree"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "total_cholesterol_mg_dl": 320,
                "family_history": "1st_degree"
            }
        }


class UsMedpedFhCriteriaResponse(BaseModel):
    """
    Response model for US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia
    
    Returns the diagnostic result (Positive/Negative) based on whether the patient's 
    total cholesterol meets or exceeds the age and family history-specific cutoff.
    
    Interpretation guidelines:
    - Positive result: Meets MEDPED criteria for FH diagnosis
      → Consider genetic testing, family screening, high-intensity statin therapy
      → Target LDL-C <70 mg/dL (or <55 mg/dL if CVD present)
      → Refer to lipid specialist if goals not achieved
    
    - Negative result: Does not meet MEDPED criteria for FH
      → If cholesterol elevated, consider secondary causes or polygenic hypercholesterolemia
      → Apply standard cardiovascular risk assessment guidelines
    
    Clinical considerations:
    - MEDPED criteria have high specificity but may miss some FH cases (lower sensitivity)
    - Genetic testing remains gold standard for definitive FH diagnosis
    - Cascade screening of family members is recommended if criteria are met
    - Earlier diagnosis leads to better cardiovascular outcomes
    
    Reference: Williams RR, et al. Am J Cardiol. 1993;72(2):171-176.
    """
    
    result: Literal["Positive", "Negative"] = Field(
        ...,
        description="Diagnostic result based on US MEDPED criteria. Positive if cholesterol exceeds age/family history-specific cutoff",
        example="Positive"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations based on diagnostic result, including treatment and screening guidance",
        example="Patient meets the US MEDPED diagnostic criteria for familial hypercholesterolemia. Total cholesterol of 320 mg/dL exceeds the cutoff of 270 mg/dL for age 35 years with 1st degree relative with FH. Recommendations: Consider genetic testing for FH mutations, cascade screening of family members, and initiation of high-intensity statin therapy."
    )
    
    stage: Literal["Positive", "Negative"] = Field(
        ...,
        description="Diagnostic stage (same as result for binary criteria)",
        example="Positive"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic result",
        example="Meets US MEDPED criteria for FH"
    )
    
    cholesterol_cutoff: int = Field(
        ...,
        description="Age and family history-specific cholesterol cutoff value used for diagnosis (mg/dL)",
        example=270
    )
    
    age_group: str = Field(
        ...,
        description="Age group category used for cutoff determination",
        example="30_to_39"
    )
    
    family_history_category: str = Field(
        ...,
        description="Family history category used for cutoff determination",
        example="1st_degree"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Positive",
                "interpretation": "Patient meets the US MEDPED diagnostic criteria for familial hypercholesterolemia. Total cholesterol of 320 mg/dL exceeds the cutoff of 270 mg/dL for age 35 years with 1st degree relative with FH. Recommendations: Consider genetic testing for FH mutations, cascade screening of family members, and initiation of high-intensity statin therapy. Target LDL-C <70 mg/dL (or <55 mg/dL if cardiovascular disease present). Refer to lipid specialist if LDL-C goals not achieved with standard therapy.",
                "stage": "Positive",
                "stage_description": "Meets US MEDPED criteria for FH",
                "cholesterol_cutoff": 270,
                "age_group": "30_to_39", 
                "family_history_category": "1st_degree"
            }
        }
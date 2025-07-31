"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score Models

Request and response models for NAFLD Fibrosis Score calculation.

References (Vancouver style):
1. Angulo P, Hui JM, Marchesini G, Bugianesi E, George J, Farrell GC, et al. 
   The NAFLD fibrosis score: a noninvasive system that identifies liver fibrosis 
   in patients with NAFLD. Hepatology. 2007 Apr;45(4):846-54. doi: 10.1002/hep.21496.
2. McPherson S, Stewart SF, Henderson E, Burt AD, Day CP. Simple non-invasive 
   fibrosis scoring systems can reliably exclude advanced fibrosis in patients 
   with non-alcoholic fatty liver disease. Gut. 2010 Sep;59(9):1265-9. 
   doi: 10.1136/gut.2010.216077.
3. Shah AG, Lydecker A, Murray K, Tetri BN, Contos MJ, Sanyal AJ, et al. 
   Comparison of noninvasive markers of fibrosis in patients with nonalcoholic 
   fatty liver disease. Clin Gastroenterol Hepatol. 2009 Oct;7(10):1104-12. 
   doi: 10.1016/j.cgh.2009.05.033.

The NAFLD Fibrosis Score is a non-invasive scoring system that uses routinely 
available clinical and laboratory data to identify NAFLD patients with and without 
advanced liver fibrosis. It helps reduce the need for liver biopsy by accurately 
identifying patients unlikely to have advanced fibrosis with a negative predictive 
value of 93% and those likely to have advanced fibrosis with a positive predictive 
value of 90%. The score was developed and validated in a cohort of 733 patients 
with biopsy-proven NAFLD.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class NafldFibroseScoreRequest(BaseModel):
    """
    Request model for NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score
    
    The NAFLD Fibrosis Score uses 6 clinical and laboratory variables to predict 
    the presence or absence of advanced fibrosis (F3-F4) in patients with NAFLD:
    
    1. Age (years): Older age is associated with increased fibrosis risk
    2. BMI (kg/m²): Higher BMI correlates with more severe liver disease
    3. Hyperglycemia: Presence of impaired fasting glucose (IFG) or diabetes mellitus
    4. AST/ALT ratio: Higher ratios suggest more advanced fibrosis
    5. Platelet count (×10⁹/L): Lower counts indicate portal hypertension
    6. Albumin (g/dL): Lower levels suggest impaired liver synthetic function
    
    Formula:
    Score = -1.675 + 0.037 × age + 0.094 × BMI + 1.13 × hyperglycemia (yes=1) 
            + 0.99 × AST/ALT ratio - 0.013 × platelet - 0.66 × albumin
    
    Interpretation cutoffs:
    - Score < -1.455: Absence of significant fibrosis (F0-F2), NPV 93%
    - Score -1.455 to 0.676: Indeterminate zone (~30% of patients)
    - Score > 0.676: Presence of significant fibrosis (F3-F4), PPV 90%
    
    References (Vancouver style):
    1. Angulo P, Hui JM, Marchesini G, Bugianesi E, George J, Farrell GC, et al. 
       The NAFLD fibrosis score: a noninvasive system that identifies liver fibrosis 
       in patients with NAFLD. Hepatology. 2007 Apr;45(4):846-54. doi: 10.1002/hep.21496.
    """
    
    age: float = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Older age is an independent risk factor for advanced fibrosis in NAFLD",
        example=55.0
    )
    
    bmi: float = Field(
        ...,
        ge=10,
        le=70,
        description="Body Mass Index in kg/m². Higher BMI is associated with increased risk of NAFLD progression",
        example=32.5
    )
    
    hyperglycemia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of impaired fasting glucose (IFG ≥100 mg/dL) or diabetes mellitus. Insulin resistance is a key driver of NAFLD progression",
        example="yes"
    )
    
    ast: float = Field(
        ...,
        ge=1,
        le=2000,
        description="Aspartate aminotransferase (AST) level in IU/L. Used to calculate AST/ALT ratio",
        example=45.0
    )
    
    alt: float = Field(
        ...,
        ge=1,
        le=2000,
        description="Alanine aminotransferase (ALT) level in IU/L. ALT is typically elevated in NAFLD but the AST/ALT ratio increases with fibrosis progression",
        example=60.0
    )
    
    platelet_count: float = Field(
        ...,
        ge=10,
        le=800,
        description="Platelet count in ×10⁹/L. Thrombocytopenia suggests portal hypertension from advanced fibrosis",
        example=180.0
    )
    
    albumin: float = Field(
        ...,
        ge=1.0,
        le=6.0,
        description="Serum albumin level in g/dL. Hypoalbuminemia indicates impaired liver synthetic function",
        example=3.8
    )
    
    @field_validator('alt')
    def alt_not_zero(cls, v):
        """Ensure ALT is not zero to avoid division by zero"""
        if v == 0:
            raise ValueError("ALT cannot be zero")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 55.0,
                "bmi": 32.5,
                "hyperglycemia": "yes",
                "ast": 45.0,
                "alt": 60.0,
                "platelet_count": 180.0,
                "albumin": 3.8
            }
        }


class NafldFibroseScoreResponse(BaseModel):
    """
    Response model for NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score
    
    The NAFLD Fibrosis Score provides a non-invasive assessment of liver fibrosis 
    in NAFLD patients with excellent performance characteristics:
    - AUROC: 0.88 (95% CI 0.85-0.92) for detecting advanced fibrosis
    - NPV 93% for score < -1.455 (rules out F3-F4 fibrosis)
    - PPV 90% for score > 0.676 (rules in F3-F4 fibrosis)
    
    Fibrosis stages:
    - F0: No fibrosis
    - F1: Perisinusoidal or periportal fibrosis
    - F2: Perisinusoidal and portal/periportal fibrosis
    - F3: Bridging fibrosis
    - F4: Cirrhosis
    
    Reference: Angulo P, et al. Hepatology. 2007;45(4):846-54.
    """
    
    result: float = Field(
        ...,
        description="NAFLD Fibrosis Score calculated from clinical and laboratory variables (typical range: -4 to +4)",
        example=-0.234
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the score with specific cutoff values and predictive values",
        example="Score of -0.234 (between -1.455 and 0.676) falls in the indeterminate zone. Approximately 30% of patients fall into this range where the score cannot definitively rule in or rule out advanced fibrosis. Additional testing such as liver biopsy, elastography, or other non-invasive markers may be needed."
    )
    
    stage: str = Field(
        ...,
        description="Fibrosis stage category (F0-F2, Indeterminate, or F3-F4)",
        example="Indeterminate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the fibrosis stage",
        example="Indeterminate zone"
    )
    
    ast_alt_ratio: Optional[float] = Field(
        None,
        description="Calculated AST/ALT ratio used in the score calculation",
        example=0.75
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": -0.234,
                "unit": "points",
                "interpretation": "Score of -0.234 (between -1.455 and 0.676) falls in the indeterminate zone. Approximately 30% of patients fall into this range where the score cannot definitively rule in or rule out advanced fibrosis. Additional testing such as liver biopsy, elastography, or other non-invasive markers may be needed.",
                "stage": "Indeterminate",
                "stage_description": "Indeterminate zone",
                "ast_alt_ratio": 0.75
            }
        }
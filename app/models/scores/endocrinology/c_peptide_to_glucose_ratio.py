"""
C-Peptide to Glucose Ratio Models

Request and response models for C-Peptide to Glucose Ratio calculation.

References (Vancouver style):
1. Saisho Y. Postprandial C-Peptide to Glucose Ratio as a Marker of β Cell Function: 
   Implication for the Management of Type 2 Diabetes. Int J Mol Sci. 2016 May 6;17(5):744. 
   doi: 10.3390/ijms17050744.
2. Fritsche A, Heni M, Peter A, Stefan N, Häring HU, Wagner R. Different Effects of 
   Lifestyle Intervention in High- and Low-Insulin Secretors. Diabetes Care. 2023 Feb 
   1;46(2):290-297. doi: 10.2337/dc22-1523.
3. Iwao T, Sakata N, Takeuchi T, Nishimura K, Ohtake S, Akaiwa Y, Kawamura I, Ito A, 
   Yoshida A. Postprandial Serum C-Peptide to Plasma Glucose Ratio Predicts Future 
   Insulin Therapy in Patients with Type 2 Diabetes: A 10-Year Prospective Cohort Study. 
   J Diabetes Investig. 2021 Jan;12(1):68-75. doi: 10.1111/jdi.13304.

The C-peptide to glucose ratio (CGR) is a simple marker of beta cell function that helps 
evaluate endogenous insulin secretion capacity and guide diabetes management decisions.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CPeptideToGlucoseRatioRequest(BaseModel):
    """
    Request model for C-Peptide to Glucose Ratio
    
    The C-peptide to glucose ratio (CGR) evaluates pancreatic beta cell function by 
    assessing the relationship between C-peptide secretion and glucose levels:
    
    C-peptide:
    - Co-secreted with insulin in equimolar amounts from pancreatic beta cells
    - Not significantly extracted by the liver (unlike insulin)
    - Has a longer half-life than insulin (~30 min vs ~5 min)
    - Better marker of endogenous insulin secretion than insulin itself
    - Normal range: 0.5-3.0 ng/mL (fasting), higher postprandially
    
    Glucose:
    - Plasma glucose level at the time of C-peptide measurement
    - Should ideally be measured postprandially (1-2 hours after meal)
    - Fasting measurements can also be used but may be less informative
    
    Clinical Applications:
    - Differentiating Type 1 from Type 2 diabetes
    - Assessing residual beta cell function
    - Guiding insulin therapy decisions
    - Monitoring disease progression
    - Identifying candidates for therapy simplification
    
    Important Considerations:
    - Not recommended for patients with chronic kidney disease (reduced C-peptide clearance)
    - Best measured in postprandial state for optimal assessment
    - Should be interpreted in clinical context
    
    References (Vancouver style):
    1. Saisho Y. Postprandial C-Peptide to Glucose Ratio as a Marker of β Cell Function: 
    Implication for the Management of Type 2 Diabetes. Int J Mol Sci. 2016 May 6;17(5):744.
    """
    
    c_peptide: float = Field(
        ...,
        ge=0.01, le=50.0,
        description="Serum C-peptide level in ng/mL. Normal fasting range is 0.5-3.0 ng/mL. Higher values expected postprandially.",
        example=2.5
    )
    
    glucose: float = Field(
        ...,
        ge=10, le=1000,
        description="Plasma glucose level in mg/dL measured at the same time as C-peptide. Best if measured 1-2 hours postprandially.",
        example=180
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "c_peptide": 2.5,
                "glucose": 180
            }
        }


class CPeptideToGlucoseRatioResponse(BaseModel):
    """
    Response model for C-Peptide to Glucose Ratio
    
    The CGR provides a simple assessment of beta cell function:
    
    Formula:
    CGR = C-peptide (ng/mL) / Glucose (mg/dL) × 100
    
    Interpretation:
    - CGR < 2: Severe insulin secretion deficit
      * Indicates significant beta cell dysfunction
      * Insulin therapy necessary
      * Common in Type 1 diabetes or advanced Type 2 diabetes
    
    - CGR 2-5: Impaired insulin secretion
      * Moderate beta cell dysfunction
      * May require basal insulin plus other agents
      * Partial preservation of beta cell function
    
    - CGR > 5: Preserved insulin secretion
      * Adequate beta cell function
      * Insulin usually unnecessary
      * Can be managed with lifestyle and non-insulin agents
    
    Clinical Implications:
    - Helps personalize diabetes therapy
    - Predicts future insulin requirements
    - Monitors disease progression
    - Guides therapy intensification or simplification
    
    Limitations:
    - Not valid in chronic kidney disease
    - May be affected by recent hypoglycemia
    - Should not be used during acute illness
    
    Reference: Saisho Y. Int J Mol Sci. 2016;17(5):744.
    """
    
    result: float = Field(
        ...,
        description="C-peptide to glucose ratio value",
        example=1.39
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ratio",
        example="ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the ratio with management recommendations",
        example="With a C-peptide to glucose ratio of 1.39, there is evidence of severe insulin secretion deficit indicating significant beta cell dysfunction. Insulin therapy is necessary for adequate glycemic control."
    )
    
    stage: str = Field(
        ...,
        description="Beta cell function category (Insulin Secretion Deficit, Impaired Insulin Secretion, Preserved Insulin Secretion)",
        example="Insulin Secretion Deficit"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the beta cell function stage",
        example="Severe beta cell dysfunction"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Additional calculation details including input values and units",
        example={
            "c_peptide": 2.5,
            "glucose": 180,
            "c_peptide_unit": "ng/mL",
            "glucose_unit": "mg/dL"
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1.39,
                "unit": "ratio",
                "interpretation": "With a C-peptide to glucose ratio of 1.39, there is evidence of severe insulin secretion deficit indicating significant beta cell dysfunction. Insulin therapy is necessary for adequate glycemic control. This pattern is commonly seen in Type 1 diabetes, longstanding Type 2 diabetes with beta cell exhaustion, or other forms of diabetes with severe beta cell impairment. Regular monitoring and adjustment of insulin therapy is essential.",
                "stage": "Insulin Secretion Deficit",
                "stage_description": "Severe beta cell dysfunction",
                "details": {
                    "c_peptide": 2.5,
                    "glucose": 180,
                    "c_peptide_unit": "ng/mL",
                    "glucose_unit": "mg/dL"
                }
            }
        }
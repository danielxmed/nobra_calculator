"""
AST to Platelet Ratio Index (APRI) Models

Request and response models for APRI calculation.

References (Vancouver style):
1. Wai CT, Greenson JK, Fontana RJ, et al. A simple noninvasive index can predict both 
   significant fibrosis and cirrhosis in patients with chronic hepatitis C. Hepatology. 
   2003;38(2):518-26.
2. Shaheen AA, Myers RP. Diagnostic accuracy of the aspartate aminotransferase-to-platelet 
   ratio index for the prediction of hepatitis C-related fibrosis: a systematic review. 
   Hepatology. 2007;46(3):912-21.
3. Lin ZH, Xin YN, Dong QJ, et al. Performance of the aspartate aminotransferase-to-platelet 
   ratio index for the staging of hepatitis C-related fibrosis: an updated meta-analysis. 
   Hepatology. 2011;53(3):726-36.

The APRI is a simple, non-invasive index that uses readily available laboratory tests 
(AST and platelet count) to assess the likelihood of significant hepatic fibrosis and 
cirrhosis in patients with chronic hepatitis C. It has better negative predictive value 
than positive predictive value, making it particularly useful for ruling out advanced 
liver disease.
"""

from pydantic import BaseModel, Field


class ApriRequest(BaseModel):
    """
    Request model for AST to Platelet Ratio Index (APRI)
    
    The APRI uses three laboratory parameters to calculate the risk of hepatic fibrosis:
    
    1. AST (Aspartate Aminotransferase): Elevated levels indicate hepatocyte damage
    2. AST Upper Limit of Normal: Laboratory-specific reference range, typically:
       - Males: 40 U/L
       - Females: 32 U/L
       - May vary by laboratory and methodology
    3. Platelet Count: Decreased in portal hypertension and hypersplenism
    
    Formula: APRI = [(AST/AST upper limit of normal) × 100] / Platelet count (×10³/µL)
    
    Interpretation:
    - APRI ≤0.3: Rules out significant fibrosis (high negative predictive value)
    - APRI ≤0.5: Rules out cirrhosis (good negative predictive value)
    - APRI ≥1.5: Suggests significant fibrosis (good positive predictive value)
    - APRI ≥2.0: Strongly suggests cirrhosis
    
    References (Vancouver style):
    1. Wai CT, Greenson JK, Fontana RJ, et al. A simple noninvasive index can predict both 
    significant fibrosis and cirrhosis in patients with chronic hepatitis C. Hepatology. 
    2003;38(2):518-26.
    2. Shaheen AA, Myers RP. Diagnostic accuracy of the aspartate aminotransferase-to-platelet 
    ratio index for the prediction of hepatitis C-related fibrosis: a systematic review. 
    Hepatology. 2007;46(3):912-21.
    3. Lin ZH, Xin YN, Dong QJ, et al. Performance of the aspartate aminotransferase-to-platelet 
    ratio index for the staging of hepatitis C-related fibrosis: an updated meta-analysis. 
    Hepatology. 2011;53(3):726-36.
    """
    
    ast: float = Field(
        ...,
        description="Serum aspartate aminotransferase (AST) level. Normal ranges vary by laboratory but are typically 10-40 U/L for males and 7-35 U/L for females",
        ge=1,
        le=2000,
        example=80.0
    )
    
    ast_upper_limit: float = Field(
        ...,
        description="Upper limit of normal for AST based on laboratory reference range. Commonly 40 U/L for males, 32 U/L for females, but may vary by laboratory and methodology",
        ge=10,
        le=100,
        example=40.0
    )
    
    platelet_count: float = Field(
        ...,
        description="Platelet count in thousands per microliter (×10³/µL). Normal range is typically 150-450 ×10³/µL. Decreased counts may indicate portal hypertension or hypersplenism",
        ge=10,
        le=1000,
        example=150.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "ast": 80.0,
                "ast_upper_limit": 40.0,
                "platelet_count": 150.0
            }
        }


class ApriResponse(BaseModel):
    """
    Response model for AST to Platelet Ratio Index (APRI)
    
    The APRI score provides a non-invasive assessment of hepatic fibrosis risk:
    
    Risk Categories:
    - Low Risk (≤0.3): Rules out significant fibrosis
    - Low-Intermediate Risk (0.3-0.5): Low probability of cirrhosis  
    - Intermediate Risk (0.5-1.5): Indeterminate, may need additional assessment
    - High Risk (1.5-2.0): Suggests significant fibrosis
    - Very High Risk (≥2.0): Strongly suggests cirrhosis
    
    Clinical Implications:
    - High negative predictive value for excluding advanced fibrosis
    - Lower sensitivity for detecting cirrhosis
    - Best used in combination with other non-invasive markers
    - May guide need for liver biopsy or further hepatology evaluation
    
    Reference: Wai CT, et al. Hepatology. 2003;38(2):518-26.
    """
    
    result: float = Field(
        ...,
        description="APRI score calculated using the formula: [(AST/AST upper limit) × 100] / Platelet count. Higher scores indicate greater likelihood of hepatic fibrosis",
        example=3.56
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the APRI score",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with recommendations for patient management based on the calculated APRI score",
        example="APRI ≥2.0 strongly suggests cirrhosis (METAVIR F4). Requires hepatology evaluation, surveillance for hepatocellular carcinoma, and assessment for portal hypertension complications."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on APRI score (Low Risk, Low-Intermediate Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Very High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Suggests cirrhosis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3.56,
                "unit": "index",
                "interpretation": "APRI ≥2.0 strongly suggests cirrhosis (METAVIR F4). Requires hepatology evaluation, surveillance for hepatocellular carcinoma, and assessment for portal hypertension complications.",
                "stage": "Very High Risk",
                "stage_description": "Suggests cirrhosis"
            }
        }

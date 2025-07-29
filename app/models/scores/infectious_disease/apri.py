"""
AST to Platelet Ratio Index (APRI) Models

Request and response models for APRI calculation.

References (Vancouver style):
1. Lin ZH, Xin YN, Dong QJ, Douillet D, Kline JA, Righini M, et al. Performance of 
   the aspartate aminotransferase-to-platelet ratio index for the staging of 
   hepatitis C-related fibrosis: an updated meta-analysis. Hepatology. 2011;53(3):726-36.
2. Chou R, Wasson N. Blood tests to diagnose fibrosis or cirrhosis in patients with 
   chronic hepatitis C virus infection: a systematic review. Ann Intern Med. 
   2013;158(11):807-20.
3. Wai CT, Greenson JK, Fontana RJ, Kalbfleisch JD, Marrero JA, Conjeevaram HS, 
   et al. A simple noninvasive index can predict both significant fibrosis and 
   cirrhosis in patients with chronic hepatitis C. Hepatology. 2003;38(2):518-26.

The APRI is a non-invasive serum marker that uses AST levels and platelet count to 
assess liver fibrosis and cirrhosis risk in patients with chronic hepatitis C. The 
score is calculated as [(AST/upper limit of normal) × 100] / platelet count. APRI 
values ≤0.5 have high negative predictive value for ruling out significant fibrosis, 
while values ≥1.5 have high positive predictive value for ruling in cirrhosis.
"""

from pydantic import BaseModel, Field


class ApriRequest(BaseModel):
    """
    Request model for AST to Platelet Ratio Index (APRI)
    
    The APRI uses three clinical parameters to assess liver fibrosis risk:
    
    AST Level:
    - Aspartate aminotransferase level in IU/L
    - Normal range varies by laboratory but typically <40 IU/L for men, <32 IU/L for women
    - Elevated levels indicate hepatocellular injury and inflammation
    
    AST Upper Limit Normal:
    - Laboratory-specific upper limit of normal for AST
    - Most experts recommend using 40 IU/L as standard reference
    - This value is used to normalize AST levels across different laboratories
    
    Platelet Count:
    - Platelet count in ×10⁹/L (equivalent to ×10³/μL)
    - Normal range: 150-400 ×10⁹/L
    - Low platelet count (thrombocytopenia) is common in cirrhosis due to hypersplenism
    
    Clinical Application:
    - Primary validation in hepatitis C patients
    - Can be used in other chronic liver diseases with caution
    - Non-invasive alternative to liver biopsy for fibrosis assessment
    - Cost-effective screening tool for liver fibrosis
    
    Interpretation Thresholds:
    - ≤0.5: High negative predictive value for significant fibrosis
    - 0.7: Cutoff for significant fibrosis (77% sensitivity, 72% specificity)
    - 1.0: Cutoff for cirrhosis (76% sensitivity, 72% specificity)  
    - ≥1.5: High positive predictive value for cirrhosis
    - ≥2.0: Very high specificity (91%) for cirrhosis

    References (Vancouver style):
    1. Lin ZH, Xin YN, Dong QJ, Douillet D, Kline JA, Righini M, et al. Performance of 
       the aspartate aminotransferase-to-platelet ratio index for the staging of 
       hepatitis C-related fibrosis: an updated meta-analysis. Hepatology. 2011;53(3):726-36.
    2. Chou R, Wasson N. Blood tests to diagnose fibrosis or cirrhosis in patients with 
       chronic hepatitis C virus infection: a systematic review. Ann Intern Med. 
       2013;158(11):807-20.
    3. Wai CT, Greenson JK, Fontana RJ, Kalbfleisch JD, Marrero JA, Conjeevaram HS, 
       et al. A simple noninvasive index can predict both significant fibrosis and 
       cirrhosis in patients with chronic hepatitis C. Hepatology. 2003;38(2):518-26.
    """
    
    ast_level: float = Field(
        ...,
        description="Aspartate aminotransferase (AST) level in IU/L. Normal values are typically <40 IU/L for men and <32 IU/L for women. Elevated levels indicate hepatocellular injury.",
        example=120.0,
        ge=1.0,
        le=2000.0
    )
    
    ast_upper_limit_normal: float = Field(
        ...,
        description="Upper limit of normal for AST in IU/L. Most laboratories and experts recommend using 40 IU/L as the standard reference value for calculation consistency.",
        example=40.0,
        ge=10.0,
        le=100.0
    )
    
    platelet_count: float = Field(
        ...,
        description="Platelet count in ×10⁹/L (equivalent to ×10³/μL). Normal range is 150-400 ×10⁹/L. Low counts are common in cirrhosis due to hypersplenism and portal hypertension.",
        example=100.0,
        ge=10.0,
        le=1000.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ast_level": 120.0,
                "ast_upper_limit_normal": 40.0,
                "platelet_count": 100.0
            }
        }


class ApriResponse(BaseModel):
    """
    Response model for AST to Platelet Ratio Index (APRI)
    
    The APRI score is calculated as [(AST ÷ AST Upper Limit Normal) × 100] ÷ Platelet Count
    and provides risk stratification for liver fibrosis and cirrhosis:
    
    Risk Categories:
    - Low Risk (≤0.5): Minimal or no fibrosis, high NPV for significant fibrosis
    - Low-Moderate Risk (0.5-0.7): Possible mild fibrosis, additional testing may be needed
    - Moderate Risk (0.7-1.0): Significant fibrosis likely (77% sensitivity, 72% specificity)
    - High Risk (1.0-1.5): Cirrhosis likely (76% sensitivity, 72% specificity)
    - Very High Risk (1.5-2.0): Cirrhosis very likely, high PPV for cirrhosis
    - Extremely High Risk (≥2.0): Cirrhosis highly likely (91% specificity, 46% sensitivity)
    
    Clinical Utility:
    - Non-invasive assessment of liver fibrosis in hepatitis C
    - Cost-effective alternative to liver biopsy
    - Useful for monitoring disease progression
    - Can guide treatment decisions and follow-up intervals
    
    Limitations:
    - Most validated in hepatitis C; caution in other liver diseases
    - Mid-range values (0.5-1.5) less definitive
    - May not be sufficiently sensitive alone to rule out significant disease
    - Consider combining with other indices (e.g., FIB-4) for improved accuracy
    
    Reference: Lin ZH, et al. Hepatology. 2011;53(3):726-36.
    """
    
    result: float = Field(
        ...,
        description="APRI score calculated as [(AST ÷ AST Upper Limit Normal) × 100] ÷ Platelet Count. Values range from <0.5 (low risk) to >2.0 (extremely high risk).",
        example=3.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the APRI score",
        example="ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the APRI score and established literature thresholds",
        example="APRI score ≥2.0 indicates very high probability of cirrhosis with 91% specificity but 46% sensitivity. Strong positive predictor of cirrhosis."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on APRI score (Low Risk, Low-Moderate Risk, Moderate Risk, High Risk, Very High Risk, Extremely High Risk)",
        example="Extremely High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and likelihood of liver fibrosis or cirrhosis",
        example="Cirrhosis highly likely"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3.0,
                "unit": "ratio",
                "interpretation": "APRI score ≥2.0 indicates very high probability of cirrhosis with 91% specificity but 46% sensitivity. Strong positive predictor of cirrhosis.",
                "stage": "Extremely High Risk",
                "stage_description": "Cirrhosis highly likely"
            }
        }
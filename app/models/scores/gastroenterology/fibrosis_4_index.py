"""
Fibrosis-4 (FIB-4) Index for Liver Fibrosis Models

Request and response models for FIB-4 Index calculation.

References (Vancouver style):
1. Sterling RK, Lissen E, Clumeck N, Sola R, Correa MC, Montaner J, et al. 
   Development of a simple noninvasive index to predict significant fibrosis in 
   patients with HIV/HCV coinfection. Hepatology. 2006 Jun;43(6):1317-25. 
   doi: 10.1002/hep.21178. PMID: 16729309.
2. Vallet-Pichard A, Mallet V, Nalpas B, Verkarre V, Nalpas A, Dhalluin-Venier V, 
   et al. FIB-4: an inexpensive and accurate marker of fibrosis in HCV infection. 
   comparison with liver biopsy and fibrotest. Hepatology. 2007 Jul;46(1):32-6. 
   doi: 10.1002/hep.21669. PMID: 17567829.
3. Shah AG, Lydecker A, Murray K, Tetri BN, Contos MJ, Sanyal AJ, et al. 
   Comparison of noninvasive markers of fibrosis in patients with nonalcoholic 
   fatty liver disease. Clin Gastroenterol Hepatol. 2009 Oct;7(10):1104-12. 
   doi: 10.1016/j.cgh.2009.05.033. PMID: 19523535.

The FIB-4 Index is a non-invasive scoring system that uses routine laboratory 
values to estimate the degree of liver fibrosis. Originally developed for HIV/HCV 
coinfection, it has been validated in various liver diseases including NAFLD, 
HBV, and HCV. The score helps identify patients who can avoid liver biopsy 
(low risk) and those who need further evaluation (high risk).
"""

from pydantic import BaseModel, Field
from typing import Literal


class Fibrosis4IndexRequest(BaseModel):
    """
    Request model for Fibrosis-4 (FIB-4) Index for Liver Fibrosis calculation
    
    The FIB-4 Index uses four routine clinical parameters to estimate liver fibrosis:
    
    Formula: FIB-4 = (Age × AST) / (Platelet count × √ALT)
    
    Parameters:
    - Age: Patient's age in years (range: 18-120)
    - AST: Aspartate aminotransferase in U/L (range: 1-10000)
    - ALT: Alanine aminotransferase in U/L (range: 1-10000)
    - Platelet count: In 10⁹/L or 10³/µL (range: 1-1000)
    
    Interpretation:
    - FIB-4 < 1.45: Low risk of advanced fibrosis (F0-F1 on METAVIR scale)
    - FIB-4 1.45-3.25: Indeterminate risk (F2-F3)
    - FIB-4 > 3.25: High risk of advanced fibrosis/cirrhosis (F3-F4)
    
    Special considerations:
    - Use with caution in patients <35 or >65 years old
    - For patients >65 years, consider using a cutoff of 2.0 instead of 1.45
    - Validated in multiple liver diseases: HCV, HBV, NAFLD, alcoholic liver disease
    
    References (Vancouver style):
    1. Sterling RK, et al. Hepatology. 2006 Jun;43(6):1317-25.
    2. Vallet-Pichard A, et al. Hepatology. 2007 Jul;46(1):32-6.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient's age in years. Important note: FIB-4 is less accurate in patients <35 or >65 years old",
        example=52
    )
    
    ast: float = Field(
        ...,
        gt=0,
        le=10000,
        description="Aspartate aminotransferase (AST) level in U/L. Normal range typically 10-40 U/L",
        example=65
    )
    
    alt: float = Field(
        ...,
        gt=0,
        le=10000,
        description="Alanine aminotransferase (ALT) level in U/L. Normal range typically 7-56 U/L",
        example=45
    )
    
    platelet_count: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Platelet count in 10⁹/L (or ×10³/µL). Normal range typically 150-400 × 10⁹/L",
        example=220
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 52,
                "ast": 65,
                "alt": 45,
                "platelet_count": 220
            }
        }


class Fibrosis4IndexResponse(BaseModel):
    """
    Response model for Fibrosis-4 (FIB-4) Index for Liver Fibrosis calculation
    
    The FIB-4 Index provides a non-invasive assessment of liver fibrosis risk:
    
    Risk Categories:
    - Low risk (<1.45): ~90% negative predictive value for advanced fibrosis
    - Indeterminate (1.45-3.25): Requires further evaluation
    - High risk (>3.25): 97% specificity for advanced fibrosis
    
    Clinical Actions:
    - Low risk: Can avoid liver biopsy, monitor every 2-3 years
    - Indeterminate: Consider elastography, FibroTest, or biopsy
    - High risk: Refer to hepatologist, consider confirmatory testing
    
    Reference: Sterling RK, et al. Hepatology. 2006;43(6):1317-25.
    """
    
    result: float = Field(
        ...,
        description="FIB-4 index value calculated from (Age × AST) / (Platelet count × √ALT)",
        example=1.72
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the FIB-4 index",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on FIB-4 score",
        example="Indeterminate risk for advanced fibrosis. Consider second-line testing (elastography, FibroTest, or liver biopsy). Close monitoring required."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Indeterminate risk, High risk)",
        example="Indeterminate risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of fibrosis risk category with METAVIR correlation",
        example="Indeterminate risk (F2-F3)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1.72,
                "unit": "index",
                "interpretation": "Indeterminate risk for advanced fibrosis. Consider second-line testing (elastography, FibroTest, or liver biopsy). Close monitoring required.",
                "stage": "Indeterminate risk",
                "stage_description": "Indeterminate risk (F2-F3)"
            }
        }
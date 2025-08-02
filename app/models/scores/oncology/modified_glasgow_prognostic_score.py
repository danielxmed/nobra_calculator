"""
Modified Glasgow Prognostic Score (mGPS) for Cancer Outcomes Models

Request and response models for Modified Glasgow Prognostic Score assessment of cancer prognosis.

References (Vancouver style):
1. Proctor MJ, Morrison DS, Talwar D, Balmer SM, O'Reilly DS, Foulis AK, Horgan PG, 
   McMillan DC. An inflammation-based prognostic score (mGPS) predicts cancer survival 
   independent of tumour site: a Glasgow Inflammation Outcome Study. Br J Cancer. 
   2011 Aug 23;105(5):726-34. doi: 10.1038/bjc.2011.292.
2. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade of 
   experience in patients with cancer. Cancer Treat Rev. 2013 Aug;39(5):534-40. 
   doi: 10.1016/j.ctrv.2012.08.003.
3. Forrest LM, McMillan DC, McArdle CS, Angerson WJ, Dunlop DJ. Evaluation of 
   cumulative prognostic scores based on the systemic inflammatory response in 
   patients with inoperable non-small-cell lung cancer. Br J Cancer. 2003 Aug 4;89(3):477-81. 
   doi: 10.1038/sj.bjc.6601242.

The Modified Glasgow Prognostic Score (mGPS) improves upon the original Glasgow 
Prognostic Score by weighting the inflammatory component (CRP) more heavily. It uses 
readily available laboratory markers to assess systemic inflammation and nutritional 
status, providing prognostic information across multiple cancer types independent of 
tumor site and staging.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ModifiedGlasgowPrognosticScoreRequest(BaseModel):
    """
    Request model for Modified Glasgow Prognostic Score (mGPS) for Cancer Outcomes
    
    The mGPS uses two readily available laboratory markers to assess cancer prognosis:
    
    **C-Reactive Protein (CRP):**
    - Acute-phase protein reflecting systemic inflammation
    - Normal: ≤10 mg/L
    - Elevated: >10 mg/L (indicates systemic inflammatory response)
    
    **Serum Albumin:**
    - Reflects nutritional status and synthetic liver function
    - Normal: ≥35 g/L (≥3.5 g/dL)
    - Low: <35 g/L (<3.5 g/dL) (indicates malnutrition or chronic disease)
    
    **Scoring System (Modified from Original GPS):**
    - Score 0: CRP ≤10 mg/L (regardless of albumin level) - Good prognosis
    - Score 1: CRP >10 mg/L and albumin ≥35 g/L - Intermediate prognosis
    - Score 2: CRP >10 mg/L and albumin <35 g/L - Poor prognosis
    
    **Key Modification from Original GPS:**
    - Low albumin alone (without elevated CRP) scores 0 points in mGPS
    - Original GPS scored low albumin alone as 1 point
    - This modification weights inflammatory component more heavily
    
    **Clinical Applications:**
    - Validated across multiple cancer types (gastric, renal, lung, pancreatic, colorectal)
    - Provides prognostic information independent of TNM staging
    - Useful for treatment planning and patient counseling
    - Can guide supportive care interventions
    
    **Laboratory Considerations:**
    - Use concurrent laboratory values when possible
    - CRP can be elevated due to infection, trauma, or other inflammatory conditions
    - Albumin can be decreased due to liver dysfunction, nephrotic syndrome, or malnutrition
    - Consider clinical context when interpreting results
    
    References (Vancouver style):
    1. Proctor MJ, Morrison DS, Talwar D, Balmer SM, O'Reilly DS, Foulis AK, Horgan PG, 
       McMillan DC. An inflammation-based prognostic score (mGPS) predicts cancer survival 
       independent of tumour site: a Glasgow Inflammation Outcome Study. Br J Cancer. 
       2011 Aug 23;105(5):726-34.
    2. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade of 
       experience in patients with cancer. Cancer Treat Rev. 2013 Aug;39(5):534-40.
    """
    
    crp_level: float = Field(
        ...,
        ge=0,
        le=500,
        description="C-Reactive Protein (CRP) level in mg/L. Normal ≤10 mg/L, elevated >10 mg/L. Reflects systemic inflammatory response",
        example=15.2
    )
    
    albumin_level: float = Field(
        ...,
        ge=10,
        le=60,
        description="Serum albumin level in g/L. Normal ≥35 g/L, low <35 g/L. Reflects nutritional status and synthetic function",
        example=32.8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "crp_level": 15.2,
                "albumin_level": 32.8
            }
        }


class ModifiedGlasgowPrognosticScoreResponse(BaseModel):
    """
    Response model for Modified Glasgow Prognostic Score (mGPS) for Cancer Outcomes
    
    The mGPS stratifies cancer patients into three prognostic groups:
    
    **Score 0 (Good Prognosis):**
    - CRP ≤10 mg/L (regardless of albumin level)
    - Normal inflammatory markers indicate better prognosis
    - Associated with better overall survival across cancer types
    
    **Score 1 (Intermediate Prognosis):**
    - CRP >10 mg/L and albumin ≥35 g/L
    - Systemic inflammation present but nutritional status preserved
    - Intermediate survival outcomes
    - Consider anti-inflammatory supportive measures
    
    **Score 2 (Poor Prognosis):**
    - CRP >10 mg/L and albumin <35 g/L
    - Both systemic inflammation and nutritional compromise present
    - Associated with worse overall, disease-specific, and disease-free survival
    - Consider aggressive supportive care including nutritional support
    
    **Clinical Management Implications:**
    - Higher scores may indicate need for more intensive supportive care
    - Consider nutritional interventions for low albumin
    - Anti-inflammatory measures may be beneficial for elevated CRP
    - Useful for patient counseling and treatment planning
    - Should be interpreted alongside standard prognostic factors
    
    **Survival Examples (vary by cancer type and stage):**
    - Gastric Cancer 5-year survival: Score 0 (74.6%), Score 1 (61.4%), Score 2 (34.6%)
    - Results vary significantly based on patient selection, cancer stage, and treatment
    
    **Limitations:**
    - Not a standalone diagnostic or treatment decision tool
    - Should be interpreted in context of cancer stage and other prognostic factors
    - Laboratory values can be affected by non-cancer conditions
    - Survival outcomes vary significantly between cancer types and stages
    
    Reference: Proctor MJ, et al. Br J Cancer. 2011;105(5):726-34.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=2,
        description="Modified Glasgow Prognostic Score indicating cancer prognosis (0-2 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prognostic implications and management recommendations based on mGPS score",
        example="Modified Glasgow Prognostic Score 2: Poor prognosis. CRP 15.2 mg/L (>10 mg/L, elevated) with albumin 32.8 g/L (<35 g/L, low). This combination reflects both systemic inflammation and compromised nutritional status, associated with worse overall survival, disease-specific survival, and disease-free survival. Consider aggressive supportive care including nutritional support and anti-inflammatory measures where appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic category (Score 0-2)",
        example="Score 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic implications",
        example="Poor prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Modified Glasgow Prognostic Score 2: Poor prognosis. CRP 15.2 mg/L (>10 mg/L, elevated) with albumin 32.8 g/L (<35 g/L, low). This combination reflects both systemic inflammation and compromised nutritional status, associated with worse overall survival, disease-specific survival, and disease-free survival. Consider aggressive supportive care including nutritional support and anti-inflammatory measures where appropriate.",
                "stage": "Score 2",
                "stage_description": "Poor prognosis"
            }
        }
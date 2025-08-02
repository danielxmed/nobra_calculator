"""
Karnofsky Performance Status Scale Models

Request and response models for Karnofsky Performance Status calculation.

References (Vancouver style):
1. Karnofsky DA, Abelmann WH, Craver LF, Burchenal JH. The use of the nitrogen mustards 
   in the palliative treatment of carcinoma. With particular reference to bronchogenic 
   carcinoma. Cancer. 1948;1(4):634-656.
2. Karnofsky DA, Burchenal JH. The clinical evaluation of chemotherapeutic agents in cancer. 
   In: MacLeod CM, editor. Evaluation of chemotherapeutic agents. New York: Columbia 
   University Press; 1949. p. 196.
3. Schag CC, Heinrich RL, Ganz PA. Karnofsky performance status revisited reliability, 
   validity, and guidelines. J Clin Oncol. 1984;2(3):187-193.
4. Yates JW, Chalmer B, McKegney FP. Evaluation of patients with advanced cancer using 
   the Karnofsky performance status. Cancer. 1980;45(8):2220-2224.

The Karnofsky Performance Status Scale is a widely used tool in oncology to assess a 
patient's functional status and ability to tolerate cancer treatments. Originally developed 
in 1949 by David Karnofsky and colleagues for nitrogen mustard chemotherapy studies, it 
provides an 11-point scale (0-100% in 10% increments) that correlates with treatment 
tolerance, survival outcomes, and quality of life measures in cancer patients.

The scale is particularly valuable for:
- Treatment eligibility assessment
- Clinical trial enrollment criteria
- Prognosis evaluation
- Treatment intensity decisions
- Quality of life assessment

Higher scores (80-100%) generally indicate good performance status suitable for aggressive 
treatments, while lower scores (0-40%) may indicate need for palliative care or less 
intensive treatments. The scale has been validated across multiple cancer types and 
remains a standard assessment tool in oncology practice.
"""

from pydantic import BaseModel, Field
from typing import Literal


class KarnofskyPerformanceStatusRequest(BaseModel):
    """
    Request model for Karnofsky Performance Status Scale
    
    The Karnofsky Performance Status Scale uses a single assessment parameter to evaluate 
    functional status on an 11-point scale:
    
    Performance Status Levels:
    - 100%: Normal, no complaints, no evidence of disease
    - 90%: Able to carry on normal activity; minor signs or symptoms of disease  
    - 80%: Normal activity with some effort; some signs or symptoms of disease
    - 70%: Cares for self; unable to carry on normal activity or active work
    - 60%: Requires occasional assistance but able to care for most personal needs
    - 50%: Requires considerable assistance and frequent medical care
    - 40%: Disabled; requires special care and assistance
    - 30%: Severely disabled; hospitalization indicated though death not imminent
    - 20%: Very sick; hospitalization necessary; active supportive treatment necessary
    - 10%: Moribund; fatal processes progressing rapidly
    - 0%: Death
    
    Clinical Interpretation:
    - 80-100%: Excellent performance status, suitable for aggressive treatments
    - 60-70%: Good performance status, suitable for standard treatments with monitoring
    - 40-50%: Poor performance status, consider palliative or reduced-intensity treatments
    - 10-30%: Very poor performance status, focus on comfort care and symptom management
    - 0%: Death
    
    Treatment Eligibility Guidelines:
    - KPS ≥80%: Generally eligible for clinical trials and aggressive treatments
    - KPS 60-70%: May be eligible for standard chemotherapy with dose modifications
    - KPS 40-50%: Consider palliative treatments or best supportive care
    - KPS <40%: Focus on comfort care, symptom management, and quality of life
    
    References (Vancouver style):
    1. Karnofsky DA, Abelmann WH, Craver LF, Burchenal JH. The use of the nitrogen mustards 
       in the palliative treatment of carcinoma. With particular reference to bronchogenic 
       carcinoma. Cancer. 1948;1(4):634-656.
    2. Karnofsky DA, Burchenal JH. The clinical evaluation of chemotherapeutic agents in cancer. 
       In: MacLeod CM, editor. Evaluation of chemotherapeutic agents. New York: Columbia 
       University Press; 1949. p. 196.
    3. Schag CC, Heinrich RL, Ganz PA. Karnofsky performance status revisited reliability, 
       validity, and guidelines. J Clin Oncol. 1984;2(3):187-193.
    4. Yates JW, Chalmer B, McKegney FP. Evaluation of patients with advanced cancer using 
       the Karnofsky performance status. Cancer. 1980;45(8):2220-2224.
    """
    
    performance_status: Literal[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] = Field(
        ...,
        description="Karnofsky Performance Status percentage based on patient's functional capabilities and symptoms. "
                   "0% = Death, 10% = Moribund, 20% = Very sick requiring hospitalization, "
                   "30% = Severely disabled requiring hospitalization, 40% = Disabled requiring special care, "
                   "50% = Requires considerable assistance and frequent medical care, "
                   "60% = Requires occasional assistance but cares for most personal needs, "
                   "70% = Cares for self but unable to work, 80% = Normal activity with some effort, "
                   "90% = Normal activity with minor symptoms, 100% = Normal with no complaints or disease evidence",
        example=80
    )
    
    class Config:
        schema_extra = {
            "example": {
                "performance_status": 80
            }
        }


class KarnofskyPerformanceStatusResponse(BaseModel):
    """
    Response model for Karnofsky Performance Status Scale
    
    The Karnofsky Performance Status Scale provides functional status assessment with 
    clinical interpretation and treatment recommendations. The scale ranges from 0-100% 
    and categorizes patients into functional performance levels:
    
    - Excellent Performance (80-100%): Normal activity with minimal symptoms
    - Good Performance (50-70%): Unable to work but independent at home  
    - Poor Performance (20-40%): Requires assistance and medical care
    - Very Poor Performance (10%): Moribund state
    - Death (0%): Death
    
    Clinical significance:
    - Correlates with chemotherapy tolerance and survival outcomes
    - Used for treatment eligibility and clinical trial enrollment
    - Guides treatment intensity and supportive care decisions
    - Helps assess prognosis and quality of life measures
    
    Reference: Karnofsky DA, Burchenal JH. In: MacLeod CM, editor. Evaluation of 
    chemotherapeutic agents. New York: Columbia University Press; 1949. p. 196.
    """
    
    result: int = Field(
        ...,
        description="Karnofsky Performance Status score (0-100% in 10% increments)",
        example=80
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the performance status",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including functional capabilities, treatment eligibility, and recommendations based on the performance status",
        example="Excellent functional status (KPS 80%). Normal activity with some effort; some signs or symptoms of disease. Patient is suitable for aggressive treatments including high-dose chemotherapy, clinical trials, and complex procedures. Generally associated with better treatment tolerance and survival outcomes. Treatment eligibility: Eligible for all treatment options. Functional capability: Able to carry on normal activity and to work."
    )
    
    stage: str = Field(
        ...,
        description="Performance status category (Excellent Performance, Good Performance, Poor Performance, Very Poor Performance, Death)",
        example="Excellent Performance"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the performance status category",
        example="Normal activity with minimal symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 80,
                "unit": "percentage",
                "interpretation": "Excellent functional status (KPS 80%). Normal activity with some effort; some signs or symptoms of disease. Patient is suitable for aggressive treatments including high-dose chemotherapy, clinical trials, and complex procedures. Generally associated with better treatment tolerance and survival outcomes. Treatment eligibility: Eligible for all treatment options. Functional capability: Able to carry on normal activity and to work.",
                "stage": "Excellent Performance",
                "stage_description": "Normal activity with minimal symptoms"
            }
        }
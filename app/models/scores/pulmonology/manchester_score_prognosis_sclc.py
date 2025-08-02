"""
Manchester Score for Prognosis in Small Cell Lung Cancer Models

Request and response models for Manchester Score calculation.

References (Vancouver style):
1. Cerny T, Blair V, Anderson H, Bramwell V, Thatcher N. Pretreatment prognostic factors 
   and scoring system in 407 small-cell lung cancer patients. Int J Cancer. 1987 Jul 15;40(1):1-7. 
   doi: 10.1002/ijc.2910400102.
2. Paesmans M, Sculier JP, Libert P, Bureau G, Dabouis G, Thiriaux J, et al. Prognostic 
   factors for survival in advanced non-small-cell lung cancer: univariate and multivariate 
   analyses including recursive partitioning and amalgamation algorithms in 1,052 patients. 
   J Clin Oncol. 1995 May;13(5):1221-30. doi: 10.1200/JCO.1995.13.5.1221.
3. Albain KS, Crowley JJ, LeBlanc M, Livingston RB. Determinants of improved outcome in 
   small-cell lung cancer: an analysis of the 2,580-patient Southwest Oncology Group data base. 
   J Clin Oncol. 1990 Sep;8(9):1563-74. doi: 10.1200/JCO.1990.8.9.1563.

The Manchester Score for Prognosis in Small Cell Lung Cancer is a validated prognostic tool 
that predicts 2-year survival in SCLC patients using six clinical and laboratory parameters. 
Developed from analysis of 407 patients treated between 1979-1985, it stratifies patients into 
three distinct prognostic groups (good, medium, poor) to guide treatment decisions and clinical 
management. The score demonstrates excellent discrimination, with the good prognostic group 
containing all long-term survivors while the poor prognostic group had no patients surviving 
longer than one year.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ManchesterScorePrognosisSclcRequest(BaseModel):
    """
    Request model for Manchester Score for Prognosis in Small Cell Lung Cancer
    
    The Manchester Score uses six clinical and laboratory parameters to predict 2-year 
    survival in small cell lung cancer patients:
    
    1. Serum Lactate Dehydrogenase (LDH):
       - Normal: 0 points
       - Elevated (>upper limit of normal): 1 point
       - Reflects tumor burden and metabolic activity
    
    2. Serum Sodium:
       - ≥132 mmol/L: 0 points
       - <132 mmol/L: 1 point
       - Hyponatremia often due to SIADH associated with SCLC
    
    3. Serum Alkaline Phosphatase (ALP):
       - Normal or ≤1.5x upper limit: 0 points
       - >1.5x upper limit of normal: 1 point
       - Suggests liver or bone metastases
    
    4. Serum Bicarbonate:
       - ≥24 mmol/L: 0 points
       - <24 mmol/L: 1 point
       - May indicate metabolic acidosis from advanced disease
    
    5. Disease Stage:
       - Limited stage: 0 points
       - Extensive stage: 1 point
       - Key prognostic factor in SCLC staging
    
    6. Karnofsky Performance Status (KPS):
       - >50: 0 points
       - ≤50: 1 point
       - Measures functional status and daily activity capability
    
    Prognostic Groups:
    - 0-1 points: Good prognosis (16.2% two-year survival)
    - 2-3 points: Medium prognosis (2.5% two-year survival)
    - 4-6 points: Poor prognosis (0% two-year survival)
    
    Clinical Applications:
    - Treatment planning and intensity decisions
    - Patient counseling regarding prognosis
    - Clinical trial stratification
    - Comparison between different treatment studies
    - Shared decision-making for aggressive vs. palliative care
    
    References (Vancouver style):
    1. Cerny T, Blair V, Anderson H, Bramwell V, Thatcher N. Pretreatment prognostic factors 
       and scoring system in 407 small-cell lung cancer patients. Int J Cancer. 1987 Jul 15;40(1):1-7. 
       doi: 10.1002/ijc.2910400102.
    2. Paesmans M, Sculier JP, Libert P, Bureau G, Dabouis G, Thiriaux J, et al. Prognostic 
       factors for survival in advanced non-small-cell lung cancer: univariate and multivariate 
       analyses including recursive partitioning and amalgamation algorithms in 1,052 patients. 
       J Clin Oncol. 1995 May;13(5):1221-30. doi: 10.1200/JCO.1995.13.5.1221.
    """
    
    serum_ldh: Literal["normal", "elevated"] = Field(
        ...,
        description="Serum lactate dehydrogenase level relative to institutional upper limit of normal. Elevated LDH reflects increased tumor burden and metabolic activity, scoring 1 point",
        example="normal"
    )
    
    serum_sodium: float = Field(
        ...,
        ge=110.0,
        le=160.0,
        description="Serum sodium concentration in mmol/L. Hyponatremia (<132 mmol/L) often results from SIADH commonly associated with SCLC and scores 1 point",
        example=140.0
    )
    
    serum_alkaline_phosphatase: Literal["normal", "1.1_to_1.5_times_normal", "greater_than_1.5_times_normal"] = Field(
        ...,
        description="Serum alkaline phosphatase level relative to upper limit of normal. >1.5x normal suggests liver or bone metastases and scores 1 point",
        example="normal"
    )
    
    serum_bicarbonate: float = Field(
        ...,
        ge=10.0,
        le=40.0,
        description="Serum bicarbonate concentration in mmol/L. Low bicarbonate (<24 mmol/L) may indicate metabolic acidosis from advanced disease and scores 1 point",
        example=26.0
    )
    
    disease_stage: Literal["limited", "extensive"] = Field(
        ...,
        description="Small cell lung cancer staging. Limited: confined to one hemithorax including ipsilateral hilar/supraclavicular nodes. Extensive: disease beyond limited stage boundaries. Extensive stage scores 1 point",
        example="limited"
    )
    
    karnofsky_performance_status: int = Field(
        ...,
        ge=0,
        le=100,
        description="Karnofsky Performance Status scale (0-100). Measures functional status and ability to perform daily activities. KPS ≤50 indicates significant functional impairment and scores 1 point",
        example=80
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_ldh": "normal",
                "serum_sodium": 140.0,
                "serum_alkaline_phosphatase": "normal",
                "serum_bicarbonate": 26.0,
                "disease_stage": "limited",
                "karnofsky_performance_status": 80
            }
        }


class ManchesterScorePrognosisSclcResponse(BaseModel):
    """
    Response model for Manchester Score for Prognosis in Small Cell Lung Cancer
    
    The Manchester Score stratifies SCLC patients into three distinct prognostic groups:
    
    Good Prognosis (0-1 points):
    - Two-year survival: 16.2%
    - Contains all long-term survivors from original study
    - Suitable for aggressive treatment with curative intent
    - Consider concurrent chemoradiotherapy for limited stage
    
    Medium Prognosis (2-3 points):
    - Two-year survival: 2.5%
    - Standard treatment with careful monitoring
    - Balance treatment intensity with quality of life
    - Early palliative care consultation recommended
    
    Poor Prognosis (4-6 points):
    - Two-year survival: 0%
    - No patients survived >1 year in original study
    - Palliative care approach recommended
    - Treatment focus on symptom management and quality of life
    
    The Manchester Score provides evidence-based prognostic information to guide treatment 
    decisions, facilitate patient counseling, and support clinical trial design. It helps 
    distinguish patients who may benefit from aggressive treatment from those who should 
    receive primarily palliative care.
    
    Reference: Cerny T, et al. Int J Cancer. 1987;40(1):1-7.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Manchester Score assessment results including total score, component scores, prognostic categories, and detailed survival data",
        example={
            "total_score": 1,
            "ldh_score": 0,
            "sodium_score": 0,
            "alp_score": 0,
            "bicarbonate_score": 0,
            "stage_score": 1,
            "kps_score": 0,
            "ldh_category": "LDH normal",
            "sodium_category": "Sodium ≥132 mmol/L: 140.0",
            "alp_category": "Alkaline phosphatase normal",
            "bicarbonate_category": "Bicarbonate ≥24 mmol/L: 26.0",
            "stage_category": "Disease stage: extensive",
            "kps_category": "Karnofsky Performance Status >50: 80",
            "survival_data": {
                "two_year_survival": "16.2%",
                "prognostic_group": "Good",
                "contains_long_term_survivors": "Yes",
                "treatment_approach": "Curative intent"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with prognostic assessment, survival data, and detailed treatment recommendations",
        example="Good prognosis with 16.2% two-year survival rate. This prognostic group contains all long-term survivors identified in the original Manchester study cohort. Consider standard chemotherapy regimens with curative intent."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic group classification (Good Prognosis, Medium Prognosis, Poor Prognosis)",
        example="Good Prognosis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic group and expected outcomes",
        example="Good prognostic group with best survival outcomes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 1,
                    "ldh_score": 0,
                    "sodium_score": 0,
                    "alp_score": 0,
                    "bicarbonate_score": 0,
                    "stage_score": 1,
                    "kps_score": 0,
                    "ldh_category": "LDH normal",
                    "sodium_category": "Sodium ≥132 mmol/L: 140.0",
                    "alp_category": "Alkaline phosphatase normal",
                    "bicarbonate_category": "Bicarbonate ≥24 mmol/L: 26.0",
                    "stage_category": "Disease stage: extensive",
                    "kps_category": "Karnofsky Performance Status >50: 80",
                    "survival_data": {
                        "two_year_survival": "16.2%",
                        "prognostic_group": "Good",
                        "contains_long_term_survivors": "Yes",
                        "treatment_approach": "Curative intent"
                    }
                },
                "unit": "points",
                "interpretation": "Good prognosis with 16.2% two-year survival rate. This prognostic group contains all long-term survivors identified in the original Manchester study cohort. Consider standard chemotherapy regimens with curative intent.",
                "stage": "Good Prognosis",
                "stage_description": "Good prognostic group with best survival outcomes"
            }
        }
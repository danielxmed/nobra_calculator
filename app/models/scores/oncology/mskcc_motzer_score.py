"""
MSKCC/Motzer Score Models

Request and response models for MSKCC/Motzer Score calculation.

References (Vancouver style):
1. Motzer RJ, Mazumdar M, Bacik J, Berg W, Amsterdam A, Ferrara J. Survival and 
   prognostic stratification of 670 patients with advanced renal cell carcinoma. 
   J Clin Oncol. 1999 Aug;17(8):2530-40. doi: 10.1200/JCO.1999.17.8.2530.
2. Motzer RJ, Bacik J, Murphy BA, Russo P, Mazumdar M. Interferon-alfa as a 
   comparative treatment for clinical trials of new therapies against advanced 
   renal cell carcinoma. J Clin Oncol. 2002 Jan 1;20(1):289-96. 
   doi: 10.1200/JCO.2002.20.1.289.
3. Motzer RJ, Bacik J, Schwartz LH, Reuter V, Russo P, Marion S, et al. Prognostic 
   factors for survival in previously treated patients with metastatic renal cell 
   carcinoma. J Clin Oncol. 2004 Feb 1;22(3):454-63. doi: 10.1200/JCO.2004.06.132.

The MSKCC/Motzer Score is a prognostic model for metastatic renal cell carcinoma 
that uses five clinical and laboratory factors to stratify patients into risk groups. 
Originally developed for patients treated with interferon-alpha, it remains a 
foundational prognostic tool in RCC management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MskccMotzerScoreRequest(BaseModel):
    """
    Request model for MSKCC/Motzer Score for Metastatic RCC
    
    The MSKCC/Motzer Score uses five independent risk factors to predict survival 
    in metastatic renal cell carcinoma:
    
    Risk Factors (each worth 1 point if present):
    1. Time from diagnosis to systemic treatment < 1 year
    2. Hemoglobin < lower limit of normal
    3. Corrected calcium > 10 mg/dL
    4. LDH > 1.5x upper limit of normal
    5. Karnofsky Performance Status < 80%
    
    Risk Stratification:
    - Good Risk: 0 factors (median survival: 20 months)
    - Intermediate Risk: 1-2 factors (median survival: 10 months)
    - High Risk: ≥3 factors (median survival: 4 months)
    
    Clinical Context:
    This score was developed using data from 670 patients with metastatic RCC treated 
    with interferon-alpha or participating in clinical trials between 1975-1996. While 
    newer models like IMDC are preferred for patients receiving targeted therapy, the 
    MSKCC score remains valuable for understanding RCC prognosis and comparing outcomes 
    across different treatment eras.
    
    References (Vancouver style):
    1. Motzer RJ, Mazumdar M, Bacik J, Berg W, Amsterdam A, Ferrara J. Survival and 
       prognostic stratification of 670 patients with advanced renal cell carcinoma. 
       J Clin Oncol. 1999 Aug;17(8):2530-40. doi: 10.1200/JCO.1999.17.8.2530.
    """
    
    time_to_treatment_less_than_1_year: Literal["yes", "no"] = Field(
        ...,
        description="Time from initial RCC diagnosis to start of systemic treatment < 1 year. "
                    "Rapid progression to metastatic disease requiring treatment indicates more "
                    "aggressive tumor biology. Patients diagnosed with de novo metastatic disease "
                    "are automatically classified as 'yes'. Scores 1 point if yes.",
        example="yes"
    )
    
    hemoglobin_low: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin below lower limit of normal. Normal ranges: Men ≥13.5 g/dL, "
                    "Women ≥12.0 g/dL. Anemia in RCC can result from chronic disease, bone "
                    "marrow involvement, bleeding, or paraneoplastic effects. Use the most "
                    "recent value before starting treatment. Scores 1 point if yes.",
        example="no"
    )
    
    calcium_high: Literal["yes", "no"] = Field(
        ...,
        description="Corrected serum calcium > 10 mg/dL (>2.5 mmol/L). Always use corrected "
                    "calcium: Corrected Ca = Measured Ca + 0.8 × (4 - Albumin in g/dL). "
                    "Hypercalcemia in RCC often indicates bone metastases or paraneoplastic "
                    "syndrome from PTHrP production. Scores 1 point if yes.",
        example="no"
    )
    
    ldh_high: Literal["yes", "no"] = Field(
        ...,
        description="Lactate dehydrogenase (LDH) > 1.5x upper limit of normal. Normal ULN is "
                    "typically 140 U/L, so threshold is usually >210 U/L. Elevated LDH indicates "
                    "high tumor burden, cellular turnover, and tissue damage. Check your lab's "
                    "specific reference range. Scores 1 point if yes.",
        example="yes"
    )
    
    performance_status_low: Literal["yes", "no"] = Field(
        ...,
        description="Karnofsky Performance Status (KPS) < 80%. KPS <80% means the patient is "
                    "unable to carry out normal activities or do active work. This includes "
                    "patients who require occasional assistance but can care for most personal "
                    "needs (KPS 70%) or those requiring considerable assistance (KPS ≤60%). "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "time_to_treatment_less_than_1_year": "yes",
                "hemoglobin_low": "no",
                "calcium_high": "no",
                "ldh_high": "yes",
                "performance_status_low": "no"
            }
        }


class MskccMotzerScoreResponse(BaseModel):
    """
    Response model for MSKCC/Motzer Score for Metastatic RCC
    
    Provides risk stratification and survival prognosis for patients with metastatic 
    renal cell carcinoma. The score helps clinicians:
    - Counsel patients about prognosis
    - Select appropriate treatment intensity
    - Stratify patients for clinical trials
    - Compare outcomes across different studies
    
    Important Considerations:
    - Survival times are based on patients treated with interferon-alpha
    - Modern targeted therapies and immunotherapy have improved outcomes
    - The IMDC model is preferred for patients receiving targeted therapy
    - Individual patient outcomes may vary significantly
    
    Reference: Motzer RJ, et al. J Clin Oncol. 1999;17(8):2530-40.
    """
    
    result: int = Field(
        ...,
        description="Number of risk factors present (range: 0-5)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="risk factors"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk category, median survival from "
                    "the original study, and treatment implications",
        example="Intermediate risk group with median survival of 10 months. These patients "
                "require active treatment with targeted therapy or immunotherapy. Close "
                "monitoring is essential."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Good Risk, Intermediate Risk, or High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category based on number of factors",
        example="1-2 risk factors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "risk factors",
                "interpretation": "Intermediate risk group with median survival of 10 months. "
                                "These patients require active treatment with targeted therapy "
                                "or immunotherapy. Close monitoring is essential.",
                "stage": "Intermediate Risk",
                "stage_description": "1-2 risk factors"
            }
        }
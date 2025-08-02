"""
Mekhail Extension of the Motzer Score Models

Request and response models for Mekhail Extension of the Motzer Score calculation.

References (Vancouver style):
1. Mekhail TM, Abou-Jawde RM, Boumerhi G, Malhi S, Wood L, Elson P, et al. Validation 
   and extension of the Memorial Sloan-Kettering prognostic factors model for survival 
   in patients with previously untreated metastatic renal cell carcinoma. J Clin Oncol. 
   2005 Feb 1;23(4):832-41. doi: 10.1200/JCO.2005.05.179.
2. Motzer RJ, Mazumdar M, Bacik J, Berg W, Amsterdam A, Ferrara J. Survival and 
   prognostic stratification of 670 patients with advanced renal cell carcinoma. 
   J Clin Oncol. 1999 Aug;17(8):2530-40. doi: 10.1200/JCO.1999.17.8.2530.
3. Motzer RJ, Bacik J, Murphy BA, Russo P, Mazumdar M. Interferon-alfa as a 
   comparative treatment for clinical trials of new therapies against advanced renal 
   cell carcinoma. J Clin Oncol. 2002 Jan 1;20(1):289-96. doi: 10.1200/JCO.2002.20.1.289.

The Mekhail Extension of the Motzer Score is a prognostic tool for metastatic renal 
cell carcinoma (mRCC) that extends the original Memorial Sloan-Kettering Cancer Center 
(MSKCC/Motzer) score by adding two additional risk factors: prior radiotherapy and 
number of metastatic sites. This extension provides more accurate risk stratification 
for survival prediction in mRCC patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MekhailExtensionMotzerScoreRequest(BaseModel):
    """
    Request model for Mekhail Extension of the Motzer Score
    
    The Mekhail Extension builds upon the original Motzer score by incorporating 
    6 risk factors instead of 4, providing improved prognostic accuracy for 
    metastatic renal cell carcinoma patients.
    
    Risk Factors (each worth 1 point if present):
    1. LDH > 1.5x upper limit of normal (ULN)
    2. Hemoglobin < lower limit of normal (LLN)
    3. Corrected serum calcium > 10 mg/dL
    4. Time from diagnosis to systemic treatment < 1 year
    5. Prior radiotherapy (Mekhail addition)
    6. ≥2 sites of metastasis (Mekhail addition)
    
    Risk Stratification:
    - Favorable Risk: 0-1 points (median survival: 28 months)
    - Intermediate Risk: 2 points (median survival: 14 months)
    - Poor Risk: ≥3 points (median survival: 5 months)
    
    Clinical Context:
    This score was developed using data from 353 previously untreated mRCC patients 
    enrolled in clinical trials between 1987 and 2002. While it provides historical 
    prognostic information, its applicability to patients receiving modern targeted 
    therapies (e.g., tyrosine kinase inhibitors, immune checkpoint inhibitors) is limited.
    
    References (Vancouver style):
    1. Mekhail TM, Abou-Jawde RM, Boumerhi G, Malhi S, Wood L, Elson P, et al. Validation 
       and extension of the Memorial Sloan-Kettering prognostic factors model for survival 
       in patients with previously untreated metastatic renal cell carcinoma. J Clin Oncol. 
       2005 Feb 1;23(4):832-41. doi: 10.1200/JCO.2005.05.179.
    """
    
    ldh_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Lactate dehydrogenase (LDH) > 1.5x upper limit of normal. Normal ULN is "
                    "typically 140 U/L, so threshold is usually >210 U/L. Elevated LDH indicates "
                    "high tumor burden and cellular turnover. Scores 1 point if yes.",
        example="no"
    )
    
    hemoglobin_low: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin below lower limit of normal. Typically <12 g/dL for women and "
                    "<13.5 g/dL for men. Anemia in mRCC can result from chronic disease, bone "
                    "marrow infiltration, or treatment effects. Scores 1 point if yes.",
        example="yes"
    )
    
    corrected_calcium_high: Literal["yes", "no"] = Field(
        ...,
        description="Corrected serum calcium > 10 mg/dL (2.5 mmol/L). Use corrected calcium "
                    "formula: Corrected Ca = Measured Ca + 0.8 × (4 - Albumin). Hypercalcemia "
                    "in RCC often indicates bone metastases or paraneoplastic syndrome. "
                    "Scores 1 point if yes.",
        example="no"
    )
    
    time_to_treatment_less_than_1_year: Literal["yes", "no"] = Field(
        ...,
        description="Time from initial RCC diagnosis to initiation of systemic treatment < 1 year. "
                    "Rapid progression to metastatic disease indicates aggressive tumor biology. "
                    "Scores 1 point if yes.",
        example="yes"
    )
    
    prior_radiotherapy: Literal["yes", "no"] = Field(
        ...,
        description="Prior treatment with radiation therapy for RCC or metastases. This is one "
                    "of the additional factors in the Mekhail extension. Prior RT may indicate "
                    "more advanced or treatment-resistant disease. Scores 1 point if yes.",
        example="no"
    )
    
    metastatic_sites_2_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Two or more sites of metastatic disease. Common sites include lung, bone, "
                    "liver, brain, and lymph nodes. Multiple metastatic sites indicate higher "
                    "disease burden. This is the second additional factor in the Mekhail "
                    "extension. Scores 1 point if yes.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ldh_elevated": "no",
                "hemoglobin_low": "yes",
                "corrected_calcium_high": "no",
                "time_to_treatment_less_than_1_year": "yes",
                "prior_radiotherapy": "no",
                "metastatic_sites_2_or_more": "yes"
            }
        }


class MekhailExtensionMotzerScoreResponse(BaseModel):
    """
    Response model for Mekhail Extension of the Motzer Score
    
    Provides risk stratification and survival prognosis for patients with metastatic 
    renal cell carcinoma. The score helps clinicians:
    - Stratify patients for clinical trials
    - Inform treatment decisions and counseling
    - Provide prognostic information to patients and families
    
    Important Limitations:
    - Developed before the era of targeted therapy and immunotherapy
    - May not accurately predict outcomes with modern treatments
    - Should be used in conjunction with other clinical factors
    - Individual patient outcomes may vary significantly
    
    Reference: Mekhail TM, et al. J Clin Oncol. 2005;23(4):832-41.
    """
    
    result: int = Field(
        ...,
        description="Total Mekhail Extension of the Motzer Score (range: 0-6 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk category, median survival, and "
                    "treatment implications based on the calculated score",
        example="Poor risk group with median survival of 5 months. These patients have the "
                "worst prognosis and may benefit from aggressive systemic therapy or clinical "
                "trial enrollment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Favorable Risk, Intermediate Risk, or Poor Risk)",
        example="Poor Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category based on number of risk factors",
        example="≥3 risk factors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Poor risk group with median survival of 5 months. These patients "
                                "have the worst prognosis and may benefit from aggressive systemic "
                                "therapy or clinical trial enrollment.",
                "stage": "Poor Risk",
                "stage_description": "≥3 risk factors"
            }
        }
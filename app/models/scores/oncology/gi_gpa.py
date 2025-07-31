"""
Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA) Models

Request and response models for GI-GPA calculation.

References (Vancouver style):
1. Sperduto PW, Mesko S, Li J, Cagney D, Aizer A, Lin NU, et al. Estimating survival 
   in patients with gastrointestinal cancers and brain metastases: An update of the 
   graded prognostic assessment for gastrointestinal cancers (GI-GPA). Clin Transl 
   Radiat Oncol. 2019;18:39-45. doi: 10.1016/j.ctro.2019.06.009.
2. Sperduto PW, Chao ST, Sneed PK, Luo X, Suh J, Roberge D, et al. Diagnosis-specific 
   prognostic factors, indexes, and treatment outcomes for patients with newly diagnosed 
   brain metastases: a multi-institutional analysis of 4,259 patients. Int J Radiat 
   Oncol Biol Phys. 2010;77(3):655-61. doi: 10.1016/j.ijrobp.2009.08.025.
3. Sperduto PW, Yang TJ, Beal K, Pan H, Brown PD, Bangdiwala A, et al. Estimating 
   Survival in Patients With Lung Cancer and Brain Metastases: An Update of the Graded 
   Prognostic Assessment for Lung Cancer Using Molecular Markers (Lung-molGPA). JAMA 
   Oncol. 2017;3(6):827-831. doi: 10.1001/jamaoncol.2016.3834.

The Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA) is a validated 
prognostic tool designed specifically for patients with gastrointestinal cancers who 
develop brain metastases. This scoring system provides crucial information for treatment 
planning and prognostic discussions in a patient population with historically poor outcomes.

**Clinical Background**:
Brain metastases occur in approximately 10-20% of patients with gastrointestinal cancers, 
representing a devastating complication with historically poor survival outcomes. The 
median survival for patients with GI cancers and brain metastases is approximately 
8 months, but varies significantly based on patient and disease characteristics.

**Scoring System**:
The GI-GPA uses four key prognostic factors, each contributing specific point values:

**Age Categories**:
- Under 60 years: 0.5 points (better prognosis)
- 60 years or over: 0.0 points

**Karnofsky Performance Status (KPS)**:
- KPS <80: 0.0 points (poor functional status)
- KPS 80: 1.0 point (moderate functional status)
- KPS 90-100: 2.0 points (excellent functional status)

**Extracranial Metastases**:
- Present: 0.0 points (indicates more advanced systemic disease)
- Absent: 0.5 points (brain-only metastatic disease)

**Number of Brain Metastases**:
- >3 brain metastases: 0.0 points (extensive intracranial disease)
- 2-3 brain metastases: 0.5 points (moderate intracranial disease)
- 1 brain metastasis: 1.0 point (limited intracranial disease)

**Survival Outcomes by GI-GPA Score**:
- **Score 0-1.0**: 3 months median survival (Poor Prognosis)
- **Score 1.5-2.0**: 9 months median survival (Intermediate-Poor Prognosis)
- **Score 2.5-3.0**: 12 months median survival (Intermediate Prognosis)
- **Score 3.5-4.0**: 17 months median survival (Good Prognosis)

**Clinical Applications**:
1. **Treatment Selection**: Guides decisions between aggressive multimodal therapy and palliative care
2. **Prognostic Communication**: Provides evidence-based survival estimates for patients and families
3. **Clinical Trial Stratification**: Helps stratify patients in research studies
4. **Resource Allocation**: Assists in determining appropriate level of care and interventions
5. **Multidisciplinary Planning**: Facilitates coordinated care between oncology, radiation oncology, and neurosurgery

**Treatment Implications by Score**:
- **Poor Prognosis (0-1.0)**: Focus on comfort care, symptom palliation, and quality of life
- **Intermediate-Poor (1.5-2.0)**: Consider limited interventions, palliative radiation
- **Intermediate (2.5-3.0)**: Consider radiation therapy, selective surgical intervention
- **Good Prognosis (3.5-4.0)**: Consider aggressive multimodal therapy, clinical trials

**Important Clinical Considerations**:
- Developed from multi-institutional cohort of 845 patients with GI cancers and brain metastases
- Applicable to various GI cancer types (colorectal, gastric, esophageal, hepatobiliary)
- Score ranges from 0.0 (worst prognosis) to 4.0 (best prognosis)
- Should complement, not replace, clinical judgment and patient preferences
- Over 30% of patients present in the worst prognostic group (GI-GPA ≤1.0)
- Free online calculator available at brainmetgpa.com for clinical use

The GI-GPA provides a standardized, evidence-based approach to prognostication in a 
challenging clinical scenario, helping clinicians and patients make informed decisions 
about treatment goals and intensity of care.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GiGpaRequest(BaseModel):
    """
    Request model for Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA)
    
    The GI-GPA uses four prognostic factors to estimate survival in patients with 
    gastrointestinal cancers and brain metastases. All parameters should be assessed 
    at the time of brain metastases diagnosis.
    
    **Age Category**: Younger patients generally have better prognosis, with the cutoff 
    at 60 years reflecting differences in overall health status and treatment tolerance:
    - under_60: Age <60 years (0.5 points) - Better prognosis
    - 60_or_over: Age ≥60 years (0.0 points) - Standard reference
    
    **Karnofsky Performance Status (KPS)**: Functional status is a critical prognostic 
    factor reflecting the patient's ability to perform daily activities and tolerate 
    treatment:
    - under_80: KPS <80 (0.0 points) - Poor functional status, limited ability for 
      self-care, significant symptoms affecting daily activities
    - 80: KPS 80 (1.0 point) - Moderate functional status, able to carry out normal 
      activities with effort, some symptoms present
    - 90_to_100: KPS 90-100 (2.0 points) - Excellent functional status, normal activity 
      with minimal symptoms (KPS 90) or completely normal (KPS 100)
    
    **Extracranial Metastases**: Presence of metastatic disease outside the brain 
    indicates more advanced systemic disease and affects treatment options:
    - present: Extracranial metastases present (0.0 points) - More advanced systemic 
      disease, may limit treatment options and overall prognosis
    - absent: No extracranial metastases (0.5 points) - Brain-only metastatic disease, 
      potentially more favorable for aggressive local treatments
    
    **Number of Brain Metastases**: Tumor burden in the brain affects treatment options 
    and prognosis, with single lesions having better outcomes:
    - more_than_3: >3 brain metastases (0.0 points) - Extensive intracranial disease, 
      typically managed with whole brain radiation or systemic therapy
    - 2_to_3: 2-3 brain metastases (0.5 points) - Moderate intracranial disease, may 
      be candidates for stereotactic radiosurgery or limited surgical intervention
    - 1: Single brain metastasis (1.0 point) - Limited intracranial disease, best 
      candidates for surgical resection or stereotactic radiosurgery

    References (Vancouver style):
    1. Sperduto PW, Mesko S, Li J, Cagney D, Aizer A, Lin NU, et al. Estimating survival 
    in patients with gastrointestinal cancers and brain metastases: An update of the 
    graded prognostic assessment for gastrointestinal cancers (GI-GPA). Clin Transl 
    Radiat Oncol. 2019;18:39-45. doi: 10.1016/j.ctro.2019.06.009.
    2. Sperduto PW, Chao ST, Sneed PK, Luo X, Suh J, Roberge D, et al. Diagnosis-specific 
    prognostic factors, indexes, and treatment outcomes for patients with newly diagnosed 
    brain metastases: a multi-institutional analysis of 4,259 patients. Int J Radiat 
    Oncol Biol Phys. 2010;77(3):655-61. doi: 10.1016/j.ijrobp.2009.08.025.
    """
    
    age_category: Literal["under_60", "60_or_over"] = Field(
        ...,
        description="Patient age category. Younger patients (<60 years) have better prognosis (0.5 points) compared to older patients (≥60 years, 0.0 points)",
        example="under_60"
    )
    
    kps: Literal["under_80", "80", "90_to_100"] = Field(
        ...,
        description="Karnofsky Performance Status reflecting functional capacity. Higher KPS indicates better functional status: <80 (0.0 pts), 80 (1.0 pt), 90-100 (2.0 pts)",
        example="90_to_100"
    )
    
    extracranial_metastases: Literal["present", "absent"] = Field(
        ...,
        description="Presence of metastatic disease outside the brain. Absent extracranial metastases (brain-only disease) has better prognosis (0.5 pts) than present (0.0 pts)",
        example="absent"
    )
    
    number_brain_metastases: Literal["more_than_3", "2_to_3", "1"] = Field(
        ...,
        description="Number of brain metastases on imaging. Single metastasis has best prognosis (1.0 pt), 2-3 lesions moderate (0.5 pts), >3 lesions worst (0.0 pts)",
        example="1"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "under_60",
                "kps": "90_to_100",
                "extracranial_metastases": "absent",
                "number_brain_metastases": "1"
            }
        }


class GiGpaResponse(BaseModel):
    """
    Response model for Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA)
    
    Provides the calculated GI-GPA score with prognostic category and treatment recommendations 
    based on validated survival outcomes from multi-institutional studies.
    
    **Prognostic Categories and Clinical Implications**:
    
    **Poor Prognosis (Score 0-1.0, Median survival: 3 months)**:
    - Worst survival group with very limited treatment options
    - Focus on comfort care, symptom palliation, and quality of life
    - Consider palliative whole brain radiation for symptom control
    - Avoid aggressive interventions that may worsen quality of life
    - Facilitate goals of care discussions with patient and family
    
    **Intermediate-Poor Prognosis (Score 1.5-2.0, Median survival: 9 months)**:
    - Below average survival with limited benefit from aggressive interventions
    - Consider palliative radiation therapy for symptomatic lesions
    - Systemic therapy decisions should weigh benefits against toxicity
    - Focus on maintaining quality of life and functional status
    - Multidisciplinary team discussion recommended
    
    **Intermediate Prognosis (Score 2.5-3.0, Median survival: 12 months)**:
    - Moderate survival allowing for selective aggressive interventions
    - Consider radiation therapy (WBRT or SRS) for appropriate candidates
    - Surgical resection may be beneficial for single, accessible lesions
    - Systemic therapy may provide meaningful benefit
    - Multidisciplinary team approach essential for optimal treatment planning
    
    **Good Prognosis (Score 3.5-4.0, Median survival: 17 months)**:
    - Best survival group benefiting from aggressive multimodal therapy
    - Strong candidates for surgical resection of single brain metastases
    - Consider stereotactic radiosurgery for limited disease (1-3 lesions)
    - Aggressive systemic therapy appropriate
    - Consider enrollment in clinical trials
    - Multidisciplinary team coordination crucial for optimal outcomes
    
    **Treatment Decision Framework**:
    - Higher scores favor more aggressive interventions with curative intent
    - Lower scores favor palliative approaches focused on quality of life
    - Consider patient preferences, comorbidities, and primary tumor control
    - Multidisciplinary team input from medical oncology, radiation oncology, and neurosurgery
    - Regular reassessment as clinical status changes
    
    **Important Clinical Considerations**:
    - Score should complement, not replace, clinical judgment
    - Patient preferences and values must be incorporated into decision-making
    - Primary tumor control status affects treatment options
    - Overall performance status may change rapidly in this patient population
    - Consider enrollment in clinical trials for appropriate candidates
    
    Reference: Sperduto PW, et al. Clin Transl Radiat Oncol. 2019;18:39-45.
    """
    
    result: float = Field(
        ...,
        description="GI-GPA score calculated from prognostic factors (range: 0.0-4.0 points)",
        ge=0.0,
        le=4.0,
        example=4.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the GI-GPA score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including parameter summary, GI-GPA score, prognostic category, median survival estimate, and specific treatment recommendations",
        example="Clinical parameters: Age <60 years, KPS 90-100, No extracranial metastases, 1 brain metastasis. GI-GPA Score: 4.0 points. Prognostic category: Good Prognosis (Median survival: 17 months). Clinical recommendations: Best prognosis group. Consider aggressive multimodal therapy including surgical resection for solitary lesions, stereotactic radiosurgery for limited disease, and systemic therapy. These patients may benefit from clinical trial enrollment. Multidisciplinary team approach essential for optimal outcomes. Important note: This score should be used in conjunction with clinical judgment and patient preferences. Consider patient's overall condition, primary tumor control, and quality of life goals when making treatment decisions."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic category (Poor Prognosis, Intermediate-Poor Prognosis, Intermediate Prognosis, Good Prognosis)",
        example="Good Prognosis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Best survival group"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4.0,
                "unit": "points",
                "interpretation": "Clinical parameters: Age <60 years, KPS 90-100, No extracranial metastases, 1 brain metastasis. GI-GPA Score: 4.0 points. Prognostic category: Good Prognosis (Median survival: 17 months). Clinical recommendations: Best prognosis group. Consider aggressive multimodal therapy including surgical resection for solitary lesions, stereotactic radiosurgery for limited disease, and systemic therapy. These patients may benefit from clinical trial enrollment. Multidisciplinary team approach essential for optimal outcomes. Important note: This score should be used in conjunction with clinical judgment and patient preferences. Consider patient's overall condition, primary tumor control, and quality of life goals when making treatment decisions.",
                "stage": "Good Prognosis",
                "stage_description": "Best survival group"
            }
        }
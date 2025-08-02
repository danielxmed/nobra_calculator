"""
Indian Takayasu Clinical Activity Score (ITAS2010) Models

Request and response models for ITAS2010 calculation.

References (Vancouver style):
1. Misra R, Danda D, Rajappa SM, et al. Development and initial validation of the 
   Indian Takayasu Clinical Activity Score (ITAS2010). Rheumatology (Oxford). 
   2013 Oct;52(10):1795-801. doi: 10.1093/rheumatology/ket128.
2. Abularrage CJ, Sidawy AN, White PW, et al. Evaluation of the clinical effectiveness 
   of percutaneous transluminal angioplasty for Takayasu arteritis. J Vasc Surg. 
   2007;45(2):314-318.
3. Kerr GS, Hallahan CW, Giordano J, et al. Takayasu arteritis. Ann Intern Med. 
   1994;120(11):919-929.

The Indian Takayasu Clinical Activity Score (ITAS2010) is a validated clinical activity 
measure specifically developed for Takayasu arteritis, incorporating 44 clinical items 
with emphasis on cardiovascular manifestations. The score was developed from the Disease 
Extent Index (DEI.Tak) and validated in over 300 TA patients with excellent inter-observer 
reliability (IRR 0.97). It differentiates between active and inactive disease, with 
scores <2 indicating inactive disease and scores ≥2 indicating active disease requiring 
treatment intensification.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Itas2010Request(BaseModel):
    """
    Request model for Indian Takayasu Clinical Activity Score (ITAS2010) calculation
    
    Assesses new or worsening symptoms within the past 3 months across multiple domains:
    
    Systemic Manifestations:
    - Malaise or weight loss >2 kg (1 point)
    - Myalgia, arthralgia, or arthritis (1 point)
    - Headache (1 point)
    
    Abdominal Manifestations:
    - Severe abdominal pain (1 point)
    
    Genitourinary Manifestations:
    - Recent spontaneous abortion (1 point)
    
    Renal Manifestations:
    - Systolic BP >140 mmHg (1 point)
    - Diastolic BP >90 mmHg (2 points) - weighted for clinical significance
    
    Neurological Manifestations:
    - Stroke (2 points) - weighted for severity
    - Seizures (1 point)
    - Syncope (1 point)
    - Vertigo/dizziness (1 point)
    
    Cardiovascular Manifestations (key items weighted at 2 points):
    - Bruits (2 points) - key vascular sign
    - Pulse inequality (2 points) - indicates asymmetric involvement
    - New loss of pulses (2 points) - progressive occlusion
    - Claudication (2 points) - significant stenosis
    - Carotidynia (2 points) - classic inflammatory sign
    - Aortic incompetence (1 point)
    - MI/angina (1 point)
    - Cardiomyopathy/cardiac failure (1 point)
    
    Score Interpretation:
    - <2 points: Inactive disease
    - ≥2 points: Active disease requiring treatment
    
    References (Vancouver style):
    1. Misra R, Danda D, Rajappa SM, et al. Development and initial validation of the 
       Indian Takayasu Clinical Activity Score (ITAS2010). Rheumatology (Oxford). 
       2013 Oct;52(10):1795-801. doi: 10.1093/rheumatology/ket128.
    2. Abularrage CJ, Sidawy AN, White PW, et al. Evaluation of the clinical effectiveness 
       of percutaneous transluminal angioplasty for Takayasu arteritis. J Vasc Surg. 
       2007;45(2):314-318.
    """
    
    malaise_weight_loss: Literal["no", "yes"] = Field(
        ...,
        description="Malaise or weight loss >2 kg within past 3 months. Systemic manifestations indicating active inflammatory process. Scores 1 point if present",
        example="no"
    )
    
    myalgia_arthralgia: Literal["no", "yes"] = Field(
        ...,
        description="Myalgia, arthralgia, or frank arthritis within past 3 months. Musculoskeletal manifestations of systemic inflammation. Scores 1 point if present",
        example="no"
    )
    
    headache: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening headache within past 3 months. May indicate intracranial vascular involvement or systemic inflammation. Scores 1 point if present",
        example="no"
    )
    
    severe_abdominal_pain: Literal["no", "yes"] = Field(
        ...,
        description="Severe abdominal pain within past 3 months. May indicate mesenteric vessel involvement or gastrointestinal complications. Scores 1 point if present",
        example="no"
    )
    
    recent_spontaneous_abortion: Literal["no", "yes"] = Field(
        ...,
        description="Recent spontaneous abortion within past 3 months. Reproductive complication potentially related to vascular involvement. Scores 1 point if present",
        example="no"
    )
    
    systolic_bp_over_140: Literal["no", "yes"] = Field(
        ...,
        description="Systolic blood pressure >140 mmHg. Indicates renal artery involvement or secondary hypertension. Scores 1 point if present",
        example="no"
    )
    
    diastolic_bp_over_90: Literal["no", "yes"] = Field(
        ...,
        description="Diastolic blood pressure >90 mmHg. Indicates significant renal vascular involvement. Scores 2 points if present (weighted for clinical significance)",
        example="no"
    )
    
    stroke: Literal["no", "yes"] = Field(
        ...,
        description="Stroke within past 3 months. Major neurological complication indicating cerebrovascular involvement. Scores 2 points if present (weighted for severity)",
        example="no"
    )
    
    seizures: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening seizures within past 3 months. Neurological manifestation of cerebrovascular involvement. Scores 1 point if present",
        example="no"
    )
    
    syncope: Literal["no", "yes"] = Field(
        ...,
        description="Syncope episodes within past 3 months. May indicate carotid or subclavian artery involvement affecting cerebral perfusion. Scores 1 point if present",
        example="no"
    )
    
    vertigo_dizziness: Literal["no", "yes"] = Field(
        ...,
        description="Vertigo or dizziness within past 3 months. Neurological symptoms potentially related to vertebrobasilar insufficiency. Scores 1 point if present",
        example="no"
    )
    
    bruits: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening arterial bruits within past 3 months. Key cardiovascular sign indicating active vascular stenosis. Scores 2 points if present (weighted for diagnostic significance)",
        example="no"
    )
    
    pulse_inequality: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening pulse inequality between limbs within past 3 months. Indicates asymmetric arterial involvement. Scores 2 points if present (weighted for clinical significance)",
        example="no"
    )
    
    new_loss_of_pulses: Literal["no", "yes"] = Field(
        ...,
        description="New loss of pulses within past 3 months. Indicates progressive arterial occlusion. Scores 2 points if present (weighted for severity)",
        example="no"
    )
    
    claudication: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening claudication within past 3 months. Indicates significant arterial stenosis affecting limb perfusion. Scores 2 points if present (weighted for functional impact)",
        example="no"
    )
    
    carotidynia: Literal["no", "yes"] = Field(
        ...,
        description="Carotidynia (carotid artery tenderness) within past 3 months. Classic sign of active carotid artery inflammation. Scores 2 points if present (weighted for diagnostic specificity)",
        example="no"
    )
    
    aortic_incompetence: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening aortic incompetence within past 3 months. Cardiac complication of aortic root involvement. Scores 1 point if present",
        example="no"
    )
    
    mi_angina: Literal["no", "yes"] = Field(
        ...,
        description="Myocardial infarction or angina within past 3 months. Indicates coronary artery involvement or secondary cardiac ischemia. Scores 1 point if present",
        example="no"
    )
    
    cardiomyopathy_cardiac_failure: Literal["no", "yes"] = Field(
        ...,
        description="New or worsening cardiomyopathy or cardiac failure within past 3 months. Advanced cardiac complication of systemic arteritis. Scores 1 point if present",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "malaise_weight_loss": "yes",
                "myalgia_arthralgia": "no",
                "headache": "yes",
                "severe_abdominal_pain": "no",
                "recent_spontaneous_abortion": "no",
                "systolic_bp_over_140": "no",
                "diastolic_bp_over_90": "no",
                "stroke": "no",
                "seizures": "no",
                "syncope": "no",
                "vertigo_dizziness": "no",
                "bruits": "yes",
                "pulse_inequality": "no",
                "new_loss_of_pulses": "no",
                "claudication": "no",
                "carotidynia": "no",
                "aortic_incompetence": "no",
                "mi_angina": "no",
                "cardiomyopathy_cardiac_failure": "no"
            }
        }


class Itas2010Response(BaseModel):
    """
    Response model for Indian Takayasu Clinical Activity Score (ITAS2010) calculation
    
    Returns the ITAS2010 score with disease activity classification and clinical 
    management recommendations for Takayasu arteritis patients.
    
    Score Interpretation:
    - <2 points: Inactive disease - continue maintenance therapy
    - ≥2 points: Active disease - requires treatment intensification
    
    The ITAS2010 score provides validated assessment of disease activity that correlates 
    with clinical outcomes and treatment response. Higher scores indicate greater disease 
    activity and need for therapeutic intervention. The score is useful for monitoring 
    disease progression and guiding treatment decisions in clinical practice.
    
    Reference: Misra R, et al. Rheumatology (Oxford). 2013;52(10):1795-801.
    """
    
    result: int = Field(
        ...,
        description="ITAS2010 score calculated from clinical manifestations (range 0-29 points)",
        example=4,
        ge=0,
        le=29
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the disease activity score",
        example="Active disease. Evidence of active Takayasu arteritis requiring treatment intensification. Consider immunosuppressive therapy escalation or initiation of biological agents."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity classification (Inactive, Active)",
        example="Active"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the activity category with score threshold",
        example="Score 4 points (≥2 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Active disease. Evidence of active Takayasu arteritis requiring treatment intensification. Consider immunosuppressive therapy escalation or initiation of biological agents.",
                "stage": "Active",
                "stage_description": "Score 4 points (≥2 points)"
            }
        }
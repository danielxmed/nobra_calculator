"""
Eastern Cooperative Oncology Group (ECOG) Performance Status Models

Request and response models for ECOG Performance Status assessment.

References (Vancouver style):
1. Oken MM, Creech RH, Tormey DC, Horton J, Davis TE, McFadden ET, et al. Toxicity 
   and response criteria of the Eastern Cooperative Oncology Group. Am J Clin Oncol. 
   1982;5(6):649-55. doi: 10.1097/00000421-198212000-00014.
2. Zubrod CG, Schneiderman M, Frei E, Brindley C, Gold GL, Shnider B, et al. Appraisal 
   of methods for the study of chemotherapy of cancer in man: comparative therapeutic 
   trial of nitrogen mustard and triethylene thiophosphoramide. J Chronic Dis. 1960;11:7-33. 
   doi: 10.1016/0021-9681(60)90137-5.
3. Buccheri G, Ferrigno D, Tamburini M. Karnofsky and ECOG performance status scoring 
   in lung cancer: a prospective, longitudinal study of 536 patients from a single 
   institution. Eur J Cancer. 1996;32A(7):1135-41. doi: 10.1016/0959-8049(95)00664-8.

The Eastern Cooperative Oncology Group (ECOG) Performance Status is a fundamental 
assessment tool in oncology that describes a patient's level of functioning in terms 
of their ability to care for themselves, daily activity, and physical ability. 
Originally developed in 1982, it provides a simple 5-point scale (0-4) that is 
easier to use than the Karnofsky Performance Scale and is widely adopted in clinical 
practice, research, and treatment decision-making.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EcogPerformanceStatusRequest(BaseModel):
    """
    Request model for Eastern Cooperative Oncology Group (ECOG) Performance Status
    
    The ECOG Performance Status is a simple 5-point scale that assesses a patient's 
    functional status and ability to tolerate medical treatments, particularly 
    chemotherapy. It is a critical tool for:
    
    - Determining treatment eligibility and intensity
    - Prognostic assessment
    - Clinical trial stratification
    - Quality of life evaluation
    - End-of-life care planning
    
    Performance Status Levels:
    
    ECOG 0 (ecog_0): Fully Active
    - Able to carry on all pre-disease performance without restriction
    - Can perform normal activities and work
    - No symptoms or minimal symptoms
    - Excellent chemotherapy tolerance expected
    - Suitable for all clinical trials
    
    ECOG 1 (ecog_1): Restricted in Strenuous Activity
    - Restricted in physically strenuous activity but ambulatory
    - Able to carry out work of a light or sedentary nature
    - Examples: light housework, office work
    - Good chemotherapy tolerance expected
    - Suitable for most clinical trials
    
    ECOG 2 (ecog_2): Ambulatory but Unable to Work
    - Ambulatory and capable of all self-care
    - Unable to carry out any work activities
    - Up and about more than 50% of waking hours
    - Borderline for chemotherapy - requires careful evaluation
    - May need supportive care optimization
    
    ECOG 3 (ecog_3): Limited Self-Care
    - Capable of only limited self-care
    - Confined to bed or chair more than 50% of waking hours
    - Generally NOT suitable for cytotoxic chemotherapy
    - Focus on palliative care and symptom management
    - Poor prognosis
    
    ECOG 4 (ecog_4): Completely Disabled
    - Completely disabled, cannot carry on any self-care
    - Totally confined to bed or chair
    - NOT suitable for chemotherapy
    - Focus on comfort care and hospice services
    - Very poor prognosis
    
    Clinical Guidelines:
    - ASCO recommends against chemotherapy in ECOG 3-4 patients with advanced cancer
    - Medical Oncology Group of Australia (MOGA) advises focusing on palliative care for ECOG 3-4
    - ECOG 0-1 patients are optimal candidates for standard chemotherapy regimens
    - ECOG 2 patients require individualized assessment and may benefit from less intensive regimens
    
    Assessment Considerations:
    - Should be performed by trained healthcare professionals
    - Inter-rater reliability improves with standardized training
    - Nurse ratings may be stronger predictors of outcomes than physician ratings
    - Should be reassessed regularly as status can change with disease progression
    - Consider patient's baseline functional status before illness
    
    References (Vancouver style):
    1. Oken MM, Creech RH, Tormey DC, Horton J, Davis TE, McFadden ET, et al. Toxicity 
       and response criteria of the Eastern Cooperative Oncology Group. Am J Clin Oncol. 
       1982;5(6):649-55.
    2. Ma C, Bandukwala S, Burman D, Bryson J, Seccareccia D, Banerjee S, et al. 
       Interconversion of three measures of performance status: an empirical analysis. 
       Eur J Cancer. 2010;46(18):3175-83.
    """
    
    performance_status: Literal["ecog_0", "ecog_1", "ecog_2", "ecog_3", "ecog_4"] = Field(
        ...,
        description="Patient's current ECOG Performance Status level based on functional assessment. ecog_0=fully active, ecog_1=restricted in strenuous activity, ecog_2=ambulatory but unable to work, ecog_3=limited self-care, ecog_4=completely disabled",
        example="ecog_1"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "performance_status": "ecog_1"
            }
        }


class EcogPerformanceStatusResponse(BaseModel):
    """
    Response model for Eastern Cooperative Oncology Group (ECOG) Performance Status
    
    The ECOG Performance Status provides critical information for treatment planning 
    and prognostic assessment in cancer patients:
    
    ECOG 0 - Fully Active:
    - Treatment: Excellent candidate for all chemotherapy regimens including dose-dense protocols
    - Clinical Trials: Eligible for all phases of clinical trials
    - Prognosis: Generally favorable with optimal treatment tolerance
    - Monitoring: Standard surveillance intervals appropriate
    - Quality of Life: Maintain normal activities and work capacity
    
    ECOG 1 - Restricted in Strenuous Activity:
    - Treatment: Good candidate for standard chemotherapy with acceptable toxicity
    - Clinical Trials: Suitable for most trials, may need dose modifications for some intensive protocols
    - Prognosis: Good with appropriate treatment selection
    - Monitoring: Regular assessment for performance status changes
    - Quality of Life: Can maintain most activities with some limitations
    
    ECOG 2 - Ambulatory but Unable to Work:
    - Treatment: Requires careful evaluation - may benefit from less intensive regimens
    - Supportive Care: Nutrition optimization, physical therapy, symptom management
    - Clinical Trials: Limited eligibility, case-by-case assessment
    - Prognosis: Variable, depends on underlying disease and response to supportive measures
    - Quality of Life: Significant impact on daily activities and independence
    
    ECOG 3 - Limited Self-Care:
    - Treatment: Generally avoid cytotoxic chemotherapy per guidelines
    - Alternative Options: Consider targeted therapy, immunotherapy, or clinical trials in select cases
    - Palliative Care: Primary focus on symptom management and comfort
    - Prognosis: Poor, median survival typically measured in months
    - Goals of Care: Symptom relief, maintaining dignity, family support
    
    ECOG 4 - Completely Disabled:
    - Treatment: Contraindicated for chemotherapy - focus on comfort care
    - Hospice Services: Strong consideration for hospice referral
    - Symptom Management: Pain control, dyspnea management, psychological support
    - Prognosis: Very poor, life expectancy typically weeks to months
    - Goals of Care: Comfort, dignity, spiritual care, family support
    
    Treatment Decision Framework:
    - ECOG 0-1: Standard therapy with curative intent when appropriate
    - ECOG 2: Individualized approach, consider performance status optimization
    - ECOG 3: Palliative care focus, very selective use of targeted agents
    - ECOG 4: Comfort care only, hospice evaluation
    
    Prognostic Significance:
    - Strong independent predictor of survival across cancer types
    - Used for stratification in clinical trials and epidemiological studies
    - Guides discussions about goals of care and advance directives
    - Important for resource allocation and healthcare planning
    
    Monitoring and Reassessment:
    - Performance status can improve with treatment or supportive care
    - Regular reassessment allows for treatment plan modifications
    - Changes in status may indicate disease progression or treatment toxicity
    - Important for timing of palliative care or hospice referrals
    
    Reference: Oken MM, et al. Am J Clin Oncol. 1982;5(6):649-55.
    """
    
    result: int = Field(
        ...,
        description="ECOG Performance Status score (0-4 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on performance status",
        example="ECOG Performance Status 1 - Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature. Good candidate for chemotherapy with acceptable tolerance. Suitable for most clinical trials. Generally good prognosis with appropriate treatment."
    )
    
    stage: str = Field(
        ...,
        description="ECOG performance status level (ECOG 0, ECOG 1, ECOG 2, ECOG 3, ECOG 4)",
        example="ECOG 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the performance status level",
        example="Restricted in strenuous activity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "ECOG Performance Status 1 - Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature. Good candidate for chemotherapy with acceptable tolerance. Suitable for most clinical trials. Generally good prognosis with appropriate treatment.",
                "stage": "ECOG 1",
                "stage_description": "Restricted in strenuous activity"
            }
        }
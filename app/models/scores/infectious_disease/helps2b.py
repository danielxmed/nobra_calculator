"""
Helps2b calculation models
"""

from pydantic import BaseModel, Field
from typing import Any
from app.models.shared import YesNoType

class Helps2bRequest(BaseModel):
    """
    Request model for 2HELPS2B Score - Seizure Risk Prediction in Hospitalized Patients
    
    The 2HELPS2B score is a validated clinical tool for predicting seizure risk in 
    acutely ill hospitalized patients undergoing continuous EEG monitoring. It helps
    optimize the duration of neurological monitoring and resource allocation.
    
    **Clinical Applications**:
    - Seizure risk stratification in hospitalized patients
    - Continuous EEG monitoring duration optimization
    - Neurological ICU resource allocation
    - Early seizure detection protocol guidance
    - Clinical decision-making for EEG monitoring
    
    **Score Components (Each worth 1 point)**:
    - **H**: History of seizures (remote or acute suspected)
    - **E**: Epileptiform discharges on EEG
    - **L**: Lateralized periodic discharges (LPDs)
    - **P**: Bilateral independent periodic discharges (BIPDs)
    - **S**: Brief potentially ictal rhythmic discharges (BIRDs)
    - **2B**: Burst-suppression pattern
    
    **Risk Stratification**:
    - Score 0: Very low risk (5% in 72h) - 1h screening sufficient
    - Score 1: Moderate risk (12% in 72h) - 12h monitoring recommended
    - Score 2: High risk (27% in 72h) - 24h monitoring recommended
    - Score 3: Very high risk (50% in 72h) - Extended monitoring
    - Score 4+: Extreme risk (>70% in 72h) - Intensive monitoring
    
    **Clinical Validation**:
    - Validated in multicenter cohorts
    - Superior discrimination compared to clinical judgment alone
    - Helps reduce unnecessary prolonged monitoring
    - Improves seizure detection efficiency
    
    **References**:
    - Struck AF, et al. Assessment of the Validity of the 2HELPS2B Score for Inpatient Seizure Risk Prediction. JAMA Neurol. 2020;77(4):500-507.
    - Struck AF, et al. Comparison of machine learning models for seizure prediction in hospitalized patients. Ann Clin Transl Neurol. 2019;6(7):1239-1247.
    """
    seizure_history: YesNoType = Field(
        ..., 
        description="History of seizures including remote seizures or recent acute suspected seizures. Any seizure history regardless of timing adds 1 point."
    )
    epileptiform_discharges: EegFindingType = Field(
        ..., 
        description="Epileptiform discharges on EEG including spikes, sharp waves, or sporadic epileptiform activity. Classic interictal epileptiform patterns add 1 point."
    )
    lateralized_periodic_discharges: EegFindingType = Field(
        ..., 
        description="Lateralized periodic discharges (LPDs) on EEG. Repetitive, lateralized discharges at 0.5-3 Hz that are potentially epileptogenic add 1 point."
    )
    bilateral_independent_periodic_discharges: EegFindingType = Field(
        ..., 
        description="Bilateral independent periodic discharges (BIPDs) on EEG. Independent periodic patterns from both hemispheres add 1 point."
    )
    brief_potentially_ictal_rhythmic_discharges: EegFindingType = Field(
        ..., 
        description="Brief potentially ictal rhythmic discharges (BIRDs) on EEG. Brief rhythmic patterns that may represent brief seizures or ictal-interictal continuum add 1 point."
    )
    burst_suppression: EegFindingType = Field(
        ..., 
        description="Burst-suppression pattern on EEG. Alternating periods of high-amplitude activity and suppression, often indicating severe brain dysfunction, add 1 point."
    )
    
    class Config:
        schema_extra = {
            "example": {
                "seizure_history": "no",
                "epileptiform_discharges": "absent",
                "lateralized_periodic_discharges": "absent",
                "bilateral_independent_periodic_discharges": "absent",
                "brief_potentially_ictal_rhythmic_discharges": "absent",
                "burst_suppression": "absent"
            }
        }


class Helps2bResponse(BaseModel):
    """
    Response model for 2HELPS2B Score - Seizure Risk Prediction
    
    Provides evidence-based seizure risk assessment with specific monitoring
    recommendations for hospitalized patients undergoing EEG evaluation.
    
    **Risk Categories and Monitoring Recommendations**:
    - Score 0 (5% risk): 1-hour screening EEG sufficient
    - Score 1 (12% risk): 12-hour continuous monitoring
    - Score 2 (27% risk): 24-hour continuous monitoring  
    - Score 3 (50% risk): Extended monitoring (≥24h)
    - Score 4 (73% risk): Intensive monitoring, consider prophylaxis
    - Score 5 (88% risk): Critical monitoring, prophylaxis indicated
    - Score 6 (>95% risk): Maximum risk, urgent intervention
    
    **Clinical Decision Framework**:
    - Low risk (0-1): Conservative monitoring approach
    - Moderate risk (2): Standard 24-hour protocol
    - High risk (3+): Intensive monitoring and intervention
    
    **Resource Optimization**:
    - Reduces unnecessary prolonged monitoring
    - Improves seizure detection rates
    - Optimizes neurological ICU resources
    - Guides anticonvulsant prophylaxis decisions
    """
    result: int = Field(
        ..., 
        description="Total 2HELPS2B score ranging from 0-6 points. Higher scores indicate exponentially increased seizure risk within 72 hours."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the seizure risk score"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific seizure risk percentage, monitoring duration recommendations, and clinical management guidance."
    )
    stage: str = Field(
        ..., 
        description="Risk classification category (Low Risk, Moderate Risk, High Risk, Very High Risk, Extreme Risk, Critical Risk, Maximum Risk)"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the seizure risk level with clinical significance and monitoring implications"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Seizure risk in 72h: 5%. Only 1-hour screening EEG recommended. Additional monitoring generally not necessary.",
                "stage": "Low Risk",
                "stage_description": "Very low seizure risk"
            }
        }
"""
ACC/AHA Heart Failure Staging System models
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.models.shared import YesNoType, HospitalizationFrequencyType


class AccAhaHfStagingRequest(BaseModel):
    """
    Request model for ACC/AHA Heart Failure Staging System
    
    The ACC/AHA Heart Failure Staging System provides a comprehensive framework for 
    classifying heart failure progression and guiding evidence-based therapy at each stage.
    This system emphasizes prevention and early intervention to prevent disease progression.
    
    **Clinical Applications**:
    - Heart failure risk stratification and staging
    - Evidence-based therapy selection
    - Prognosis assessment and patient counseling
    - Healthcare resource allocation
    - Clinical trial enrollment criteria
    - Quality improvement initiatives
    
    **Staging Philosophy**:
    - Stage A: At risk for HF (prevention focus)
    - Stage B: Pre-HF with structural disease (progression prevention)
    - Stage C: Symptomatic HF (symptom and hospitalization control)
    - Stage D: Advanced HF (specialized care and advanced therapies)
    
    **Key Features**:
    - Hierarchical progression (no regression between stages)
    - Evidence-based therapy recommendations for each stage
    - Integration with ejection fraction classification (HFrEF, HFmrEF, HFpEF)
    - Emphasis on guideline-directed medical therapy (GDMT)
    
    **Clinical Decision Points**:
    - Stage A→B: Development of structural disease
    - Stage B→C: Onset of HF symptoms
    - Stage C→D: Refractory symptoms despite optimal therapy
    
    **References**:
    - Heidenreich PA, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145(18):e895-e1032.
    - Yancy CW, et al. 2017 ACC/AHA/HFSA Focused Update of the 2013 ACCF/AHA Guideline for the Management of Heart Failure. Circulation. 2017;136(6):e137-e161.
    """
    risk_factors: YesNoType = Field(
        ..., 
        description="Presence of risk factors for heart failure including hypertension, diabetes, metabolic syndrome, cardiotoxic drug therapy, family history of cardiomyopathy, or coronary artery disease."
    )
    structural_disease: YesNoType = Field(
        ..., 
        description="Evidence of structural heart disease (LV hypertrophy, reduced LVEF, valvular disease, previous MI) or elevated natriuretic peptides without current HF symptoms."
    )
    current_symptoms: YesNoType = Field(
        ..., 
        description="Current or previous symptoms of heart failure including dyspnea, fatigue, reduced exercise tolerance, or fluid retention with structural heart disease."
    )
    advanced_symptoms: YesNoType = Field(
        ..., 
        description="Severe symptoms refractory to optimized guideline-directed medical therapy, requiring specialized interventions or advanced heart failure care."
    )
    hospitalization_frequency: HospitalizationFrequencyType = Field(
        ..., 
        description="Frequency of heart failure-related hospitalizations: frequent (≥2 per year), rare (<2 per year), or none."
    )
    ejection_fraction: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=100.0, 
        description="Left ventricular ejection fraction percentage. Used to classify HFrEF (≤40%), HFmrEF (41-49%), or HFpEF (≥50%) and guide therapy selection."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_factors": "yes",
                "structural_disease": "yes",
                "current_symptoms": "no",
                "advanced_symptoms": "no",
                "hospitalization_frequency": "none",
                "ejection_fraction": 45.0
            }
        }


class AccAhaHfStagingResponse(BaseModel):
    """
    Response model for ACC/AHA Heart Failure Staging System
    
    Provides comprehensive heart failure staging with evidence-based therapy recommendations
    and prognostic assessment according to the 2022 AHA/ACC/HFSA Guidelines.
    
    **Stage Characteristics**:
    - Stage A: Risk factors present, no structural disease or symptoms
    - Stage B: Structural disease present, no current or prior symptoms
    - Stage C: Structural disease with current or prior HF symptoms
    - Stage D: Refractory HF requiring specialized interventions
    
    **Therapy Framework**:
    - All stages: Risk factor modification and lifestyle interventions
    - Stage A: Primary prevention with ACEI/ARB, statins
    - Stage B: ACEI/ARB, beta-blockers, ICD if indicated
    - Stage C: GDMT optimization, devices, sodium restriction
    - Stage D: Advanced therapies (VAD, transplant, palliative care)
    
    **Prognostic Implications**:
    - Stage progression is irreversible (no regression)
    - Earlier intervention improves outcomes
    - Stage D has highest mortality and morbidity
    """
    result: str = Field(
        ..., 
        description="Determined heart failure stage (A, B, C, or D) based on hierarchical assessment of risk factors, structural disease, symptoms, and treatment response."
    )
    unit: str = Field(
        ..., 
        description="Unit of the staging result"
    )
    interpretation: str = Field(
        ..., 
        description="Comprehensive clinical interpretation with stage-specific evidence-based therapeutic recommendations and management goals according to current guidelines."
    )
    stage: str = Field(
        ..., 
        description="Full stage designation with descriptive name (e.g., 'Stage A', 'Stage B', 'Stage C', 'Stage D')"
    )
    stage_description: str = Field(
        ..., 
        description="Brief description of the stage characteristics and clinical significance"
    )
    therapy_recommendations: Dict[str, Any] = Field(
        ..., 
        description="Detailed evidence-based therapeutic recommendations organized by category (primary medications, devices, lifestyle, monitoring) specific to the determined stage."
    )
    prognosis: Dict[str, str] = Field(
        ..., 
        description="Prognostic assessment including outlook, mortality risk, and progression likelihood with stage-specific considerations."
    )
    ejection_fraction: Optional[float] = Field(
        None, 
        description="Provided left ventricular ejection fraction used for HF phenotype classification and therapy selection"
    )
    can_regress: bool = Field(
        ..., 
        description="Indicates whether patients can regress to previous stages (always False in ACC/AHA system - progression is irreversible)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "B",
                "unit": "stage",
                "interpretation": "Structural disease without symptoms. Recommendations: ACEI/ARB, beta-blockers, statins, ICD if indicated (LVEF ≤30% post-MI). Goal: prevent progression to symptomatic HF.",
                "stage": "Stage B",
                "stage_description": "Pre-heart failure",
                "therapy_recommendations": {
                    "primary": ["ACEI or ARB (LVEF ≤40%)", "Evidence-based beta-blockers", "Statins"],
                    "devices": ["ICD if LVEF ≤30% post-MI (>40 days)"],
                    "monitoring": ["Follow-up echocardiogram", "Renal function monitoring"]
                },
                "prognosis": {
                    "outlook": "Good with optimized treatment",
                    "mortality": "Low to moderate",
                    "progression": "Prevention of symptoms is the goal"
                },
                "ejection_fraction": 45.0,
                "can_regress": False
            }
        }
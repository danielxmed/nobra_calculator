"""
Cumulative Illness Rating Scale-Geriatric (CIRS-G) Models

Request and response models for CIRS-G calculation.

References (Vancouver style):
1. Miller MD, Paradis CF, Houck PR, et al. Rating chronic medical illness burden in 
   geropsychiatric practice and research: application of the Cumulative Illness Rating Scale. 
   Psychiatry Res. 1992;41(3):237-248. doi: 10.1016/0165-1781(92)90005-n.
2. Linn BS, Linn MW, Gurel L. Cumulative illness rating scale. J Am Geriatr Soc. 
   1968;16(5):622-626. doi: 10.1111/j.1532-5415.1968.tb02103.x.
3. Salvi F, Miller MD, Grilli A, et al. A manual of guidelines to score the modified 
   cumulative illness rating scale and its validation in acute hospitalized elderly patients. 
   J Am Geriatr Soc. 2008;56(10):1926-1931. doi: 10.1111/j.1532-5415.2008.01935.x.
4. Hudon C, Fortin M, Vanasse A. Cumulative Illness Rating Scale was a reliable and 
   valid index in a family practice context. J Clin Epidemiol. 2005;58(6):603-608. 
   doi: 10.1016/j.jclinepi.2004.10.017.

The CIRS-G quantifies burden of illness in elderly patients by systematically rating 
the severity of medical conditions across 13 organ systems. Each system is scored 
from 0 (no problem) to 4 (extremely severe), providing a comprehensive assessment 
of overall health status and comorbidity burden. The scale has good inter-rater 
reliability (ICC 0.78-0.88) and is considered potentially more accurate than the 
Charlson Comorbidity Index for geriatric patients.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class CirsGRequest(BaseModel):
    """
    Request model for Cumulative Illness Rating Scale-Geriatric (CIRS-G)
    
    The CIRS-G systematically evaluates 13 organ systems, each scored from 0-4:
    
    **Scoring Criteria:**
    - **0**: No problem - No disease or symptoms in this organ system
    - **1**: Mild - Mild disease with minimal symptoms or well-controlled conditions  
    - **2**: Moderate - Moderate disease requiring ongoing management, some functional limitation
    - **3**: Severe - Severe disease significantly impacting daily activities
    - **4**: Extremely severe - Life-threatening condition or end-stage disease
    
    **Organ Systems Evaluated:**
    
    1. **Heart**: Arrhythmias, congestive heart failure, coronary artery disease, MI, valvular disease
    2. **Vascular**: Hypertension, peripheral vascular disease, cerebrovascular disease, aortic aneurysm
    3. **Hematopoietic**: Anemia, leukemia, lymphoma, bleeding disorders, blood clotting disorders
    4. **Respiratory**: COPD, asthma, pneumonia, lung cancer, pulmonary embolism
    5. **EENT**: Eyes, ears, nose, throat, larynx - vision problems, hearing loss, ENT disorders
    6. **Upper GI**: Esophagus, stomach, duodenum - ulcers, reflux, gastritis
    7. **Lower GI**: Small bowel, colon, rectum - IBD, diverticulitis, cancer
    8. **Liver/Pancreas/Biliary**: Hepatitis, cirrhosis, pancreatitis, gallbladder disease
    9. **Renal**: Chronic kidney disease, acute kidney injury, nephrolithiasis, glomerulonephritis
    10. **Genitourinary**: Prostate disease, urinary incontinence, sexual dysfunction, reproductive disorders
    11. **Musculoskeletal/Skin**: Arthritis, osteoporosis, fractures, skin disorders, wounds
    12. **Neurologic**: Stroke, dementia, Parkinson's disease, seizures, peripheral neuropathy
    13. **Endocrine/Breast**: Diabetes, thyroid disease, adrenal disorders, breast cancer
    
    **Clinical Applications:**
    - Comprehensive geriatric assessment
    - Predicting hospital outcomes and length of stay
    - Research tool for comorbidity assessment  
    - Treatment planning and prognosis
    - Resource allocation in geriatric care
    
    **Calculated Indices:**
    - **Total Score**: Sum of all 13 organ system scores (0-52)
    - **Severity Index**: Total Score / Number of categories with scores > 0
    - **Comorbidity Index**: Number of categories with scores ≥ 3
    
    References (Vancouver style):
    1. Miller MD, Paradis CF, Houck PR, et al. Rating chronic medical illness burden in 
       geropsychiatric practice and research: application of the Cumulative Illness Rating Scale. 
       Psychiatry Res. 1992;41(3):237-248. doi: 10.1016/0165-1781(92)90005-n.
    2. Salvi F, Miller MD, Grilli A, et al. A manual of guidelines to score the modified 
       cumulative illness rating scale and its validation in acute hospitalized elderly patients. 
       J Am Geriatr Soc. 2008;56(10):1926-1931. doi: 10.1111/j.1532-5415.2008.01935.x.
    """
    
    heart: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Heart system: arrhythmias, congestive heart failure, coronary artery disease, "
            "myocardial infarction, valvular disease. Score 0=no problem, 1=mild, 2=moderate, "
            "3=severe, 4=extremely severe/life-threatening"
        ),
        example=1
    )
    
    vascular: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Vascular system: hypertension, peripheral vascular disease, cerebrovascular disease, "
            "aortic aneurysm. Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=2
    )
    
    hematopoietic: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Blood and lymphatic systems: anemia, leukemia, lymphoma, bleeding disorders, "
            "blood clotting disorders. Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=0
    )
    
    respiratory: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Respiratory system: COPD, asthma, pneumonia, lung cancer, pulmonary embolism. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=1
    )
    
    eent: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Eyes, Ears, Nose, Throat, Larynx: vision problems, hearing loss, ENT disorders. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=1
    )
    
    upper_gi: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Upper gastrointestinal: esophagus, stomach, duodenum - ulcers, reflux, gastritis. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=0
    )
    
    lower_gi: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Lower gastrointestinal: small bowel, colon, rectum - IBD, diverticulitis, cancer. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=0
    )
    
    liver_pancreas_biliary: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Liver, Pancreas, Biliary: hepatitis, cirrhosis, pancreatitis, gallbladder disease. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=0
    )
    
    renal: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Renal system: chronic kidney disease, acute kidney injury, nephrolithiasis, glomerulonephritis. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=1
    )
    
    genitourinary: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Genitourinary: prostate disease, urinary incontinence, sexual dysfunction, reproductive disorders. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=1
    )
    
    musculoskeletal_skin: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Musculoskeletal and Skin: arthritis, osteoporosis, fractures, skin disorders, wounds. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=2
    )
    
    neurologic: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Neurologic: stroke, dementia, Parkinson's disease, seizures, peripheral neuropathy. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=0
    )
    
    endocrine_breast: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Endocrine and Breast: diabetes, thyroid disease, adrenal disorders, breast cancer. "
            "Score 0=no problem, 1=mild, 2=moderate, 3=severe, 4=extremely severe"
        ),
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "heart": 1,
                "vascular": 2,
                "hematopoietic": 0,
                "respiratory": 1,
                "eent": 1,
                "upper_gi": 0,
                "lower_gi": 0,
                "liver_pancreas_biliary": 0,
                "renal": 1,
                "genitourinary": 1,
                "musculoskeletal_skin": 2,
                "neurologic": 0,
                "endocrine_breast": 2
            }
        }


class CirsGResponse(BaseModel):
    """
    Response model for Cumulative Illness Rating Scale-Geriatric (CIRS-G)
    
    Provides comprehensive assessment of illness burden including total score, 
    calculated indices, system analysis, and clinical recommendations.
    
    **Key Metrics:**
    - **Total Score**: 0-52 points (13 systems × 4 max points each)
    - **Severity Index**: Average severity of affected systems
    - **Comorbidity Index**: Number of severely affected systems (score ≥3)
    
    **Burden Categories:**
    - Low Burden (0-6): Minimal illness burden, good prognosis
    - Mild Burden (7-12): Some conditions, generally well-managed
    - Moderate Burden (13-20): Multiple conditions, comprehensive care needed
    - High Burden (21-30): Multiple severe conditions, intensive management
    - Very High Burden (31-52): Extensive comorbidities, poor prognosis
    
    Reference: Miller MD, et al. Psychiatry Res. 1992;41(3):237-248.
    """
    
    result: int = Field(
        ...,
        description="CIRS-G total score (sum of all 13 organ system scores, range 0-52)",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the total score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation based on total score and indices",
        example="CIRS-G total score of 11 indicates mild illness burden. Patient has some health conditions but generally well-managed. Severity index of 1.83 suggests conditions are on average mild to moderate. Overall prognosis remains good with appropriate medical management."
    )
    
    stage: str = Field(
        ...,
        description="Illness burden category based on total score",
        example="Mild Burden"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the illness burden category",
        example="Mild illness burden"
    )
    
    total_score: int = Field(
        ...,
        description="Total CIRS-G score (0-52 points)",
        example=11
    )
    
    severity_index: float = Field(
        ...,
        description="Severity index (total score / number of affected systems)",
        example=1.83
    )
    
    comorbidity_index: int = Field(
        ...,
        description="Comorbidity index (number of systems with score ≥3)",
        example=0
    )
    
    affected_systems: int = Field(
        ...,
        description="Number of organ systems with score >0",
        example=6
    )
    
    severe_systems: int = Field(
        ...,
        description="Number of organ systems with score ≥3",
        example=0
    )
    
    system_breakdown: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of affected organ systems",
        example=[
            {"system": "Heart", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms"},
            {"system": "Vascular", "score": 2, "severity": "Moderate", "description": "Moderate disease requiring ongoing management"}
        ]
    )
    
    burden_assessment: Dict[str, Any] = Field(
        ...,
        description="Overall burden assessment with risk level",
        example={
            "stage": "Mild Burden",
            "description": "Mild illness burden",
            "risk_level": "mild"
        }
    )
    
    clinical_recommendations: List[str] = Field(
        ...,
        description="Clinical recommendations based on CIRS-G assessment",
        example=[
            "Regular monitoring of existing conditions",
            "Optimize management of chronic diseases",
            "Consider comprehensive geriatric assessment"
        ]
    )
    
    prognosis_indicators: Dict[str, str] = Field(
        ...,
        description="Prognosis indicators for various outcomes",
        example={
            "mortality_risk": "Low to Moderate",
            "functional_decline_risk": "Low to Moderate",
            "hospitalization_risk": "Moderate",
            "care_needs": "Basic to Moderate"
        }
    )
    
    care_complexity: Dict[str, str] = Field(
        ...,
        description="Assessment of care complexity and requirements",
        example={
            "complexity_level": "Moderate",
            "care_setting": "Outpatient with specialist involvement",
            "specialist_needs": "Limited",
            "coordination_requirements": "Moderate"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "CIRS-G total score of 11 indicates mild illness burden. Patient has some health conditions but generally well-managed. Severity index of 1.83 suggests conditions are on average mild to moderate. Overall prognosis remains good with appropriate medical management.",
                "stage": "Mild Burden",
                "stage_description": "Mild illness burden",
                "total_score": 11,
                "severity_index": 1.83,
                "comorbidity_index": 0,
                "affected_systems": 6,
                "severe_systems": 0,
                "system_breakdown": [
                    {"system": "Heart", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
                    {"system": "Vascular", "score": 2, "severity": "Moderate", "description": "Moderate disease requiring ongoing management, some functional limitation"},
                    {"system": "Respiratory", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
                    {"system": "Eent", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
                    {"system": "Renal", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
                    {"system": "Genitourinary", "score": 1, "severity": "Mild", "description": "Mild disease with minimal symptoms or well-controlled conditions"},
                    {"system": "Musculoskeletal Skin", "score": 2, "severity": "Moderate", "description": "Moderate disease requiring ongoing management, some functional limitation"},
                    {"system": "Endocrine Breast", "score": 2, "severity": "Moderate", "description": "Moderate disease requiring ongoing management, some functional limitation"}
                ],
                "burden_assessment": {
                    "stage": "Mild Burden",
                    "description": "Mild illness burden",
                    "risk_level": "mild"
                },
                "clinical_recommendations": [
                    "Regular monitoring of existing conditions",
                    "Optimize management of chronic diseases",
                    "Consider comprehensive geriatric assessment",
                    "Coordinate care between specialties as needed"
                ],
                "prognosis_indicators": {
                    "mortality_risk": "Low to Moderate",
                    "functional_decline_risk": "Low to Moderate",
                    "hospitalization_risk": "Moderate",
                    "care_needs": "Basic to Moderate"
                },
                "care_complexity": {
                    "complexity_level": "Moderate",
                    "care_setting": "Outpatient with specialist involvement",
                    "specialist_needs": "Limited",
                    "coordination_requirements": "Moderate"
                }
            }
        }
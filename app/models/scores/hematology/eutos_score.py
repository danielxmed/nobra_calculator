"""
EUTOS Score for Chronic Myelogenous Leukemia (CML) Models

Request and response models for EUTOS Score calculation for predicting outcomes 
in chronic myelogenous leukemia patients treated with tyrosine kinase inhibitors.

References (Vancouver style):
1. Hasford J, Baccarani M, Hoffmann V, Guilhot J, Saussele S, Rosti G, et al. Predicting 
   complete cytogenetic response and subsequent progression-free survival in 2060 patients 
   with CML on imatinib treatment: the EUTOS score. Blood. 2011 Jul 21;118(3):686-92. 
   doi: 10.1182/blood-2010-12-319038.
2. Hoffman R, Nagler A, Keating A, Kamel-Reid S, Lipton JH. The EUTOS score predicts 
   outcome in CML patients treated with nilotinib front-line. Blood. 2012 Dec 6;120(23):4684; 
   author reply 4684-5. doi: 10.1182/blood-2012-08-449249.
3. Baccarani M, Deininger MW, Rosti G, Hochhaus A, Soverini S, Apperley JF, et al. 
   European LeukemiaNet recommendations for the management of chronic myeloid leukemia: 
   2013 update. Blood. 2013 Aug 8;122(6):872-84. doi: 10.1182/blood-2013-05-501569.

The EUTOS Score is a prognostic tool for newly-diagnosed chronic myelogenous leukemia 
patients that predicts complete cytogenetic response at 18 months and progression-free 
survival. It uses only two simple laboratory and clinical parameters: basophil percentage 
and spleen size, making it practical for routine clinical use.
"""

from pydantic import BaseModel, Field
from typing import Optional


class EutosScoreRequest(BaseModel):
    """
    Request model for EUTOS Score for Chronic Myelogenous Leukemia (CML)
    
    The EUTOS Score predicts treatment outcomes in newly-diagnosed CML patients using 
    two simple clinical parameters:
    
    Formula: EUTOS Score = (7 × basophil percentage) + (4 × spleen size in cm)
    
    Risk Stratification:
    - Score ≤87: Low Risk (90% 5-year PFS, 86% CCyR at 18 months)
    - Score >87: High Risk (82% 5-year PFS, 66% CCyR at 18 months)
    
    Clinical Parameters:
    
    1. Basophil Percentage:
       - Basophils as percentage of peripheral blood leukocytes
       - Obtained from complete blood count with differential
       - Normal range typically 0-2%, but can be elevated in CML
       - Higher percentages associated with worse prognosis
    
    2. Spleen Size:
       - Maximum distance palpable below left costal margin in cm
       - Clinical examination finding
       - 0 cm indicates non-palpable spleen (normal)
       - Larger spleen size associated with higher tumor burden
       - Subjective measurement but validated in clinical studies
    
    Clinical Application:
    - Used only for newly-diagnosed CML patients before starting therapy
    - Developed and validated in patients treated with imatinib
    - Assists in treatment discussions and prognostic assessment
    - Helps identify patients needing more intensive monitoring
    - Simpler alternative to other CML prognostic scores (Sokal, Hasford)
    
    Validation and Performance:
    - Derived from 2,060 patients in European LeukemiaNet CML registry
    - Validated across multiple international cohorts
    - Positive predictive value for not achieving CCyR: 34%
    - Good discrimination between risk groups
    - Maintains prognostic value across different age groups
    
    Important Limitations:
    - Developed in imatinib-treated patients (outcomes may differ with newer TKIs)
    - Spleen size assessment is subjective but reflects real clinical practice
    - Should be used as part of comprehensive patient assessment
    - Not applicable to patients already on treatment
    - Mixed results in some validation studies
    
    References (Vancouver style):
    1. Hasford J, et al. Predicting complete cytogenetic response and subsequent 
       progression-free survival in 2060 patients with CML on imatinib treatment: 
       the EUTOS score. Blood. 2011;118(3):686-92.
    2. Baccarani M, et al. European LeukemiaNet recommendations for the management 
       of chronic myeloid leukemia: 2013 update. Blood. 2013;122(6):872-84.
    """
    
    basophil_percentage: float = Field(
        ...,
        description="Basophils as percentage of peripheral blood leukocytes (0-100%). Obtained from complete blood count with differential. Higher percentages indicate worse prognosis.",
        ge=0.0,
        le=100.0,
        example=3.5
    )
    
    spleen_size_cm: float = Field(
        ...,
        description="Spleen size palpable below left costal margin in centimeters (0-30 cm). 0 cm indicates non-palpable spleen. Measured by clinical examination.",
        ge=0.0,
        le=30.0,
        example=5.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "basophil_percentage": 3.5,
                "spleen_size_cm": 5.0
            }
        }


class EutosScoreResponse(BaseModel):
    """
    Response model for EUTOS Score for Chronic Myelogenous Leukemia (CML)
    
    Provides EUTOS Score with risk stratification and clinical interpretation for 
    treatment planning and prognostic assessment in newly-diagnosed CML patients.
    
    Risk Categories and Clinical Management:
    
    Low Risk (Score ≤87):
    - 5-year progression-free survival: 90%
    - Complete cytogenetic response at 18 months: 86%
    - Standard imatinib therapy recommended
    - Routine monitoring protocols
    - Excellent prognosis expected
    - Standard treatment intervals and assessments
    
    High Risk (Score >87):
    - 5-year progression-free survival: 82%
    - Complete cytogenetic response at 18 months: 66%
    - Consider more intensive monitoring
    - Earlier assessment of treatment response (3-6 months)
    - May benefit from alternative treatment strategies
    - Enhanced clinical surveillance recommended
    - Consider second-generation TKIs in appropriate cases
    
    Clinical Decision Support:
    
    Treatment Planning:
    - Risk-stratified treatment approach
    - Informed consent discussions with patients
    - Treatment goal setting and expectations
    - Resource allocation for monitoring
    
    Monitoring Strategy:
    - Low risk: Standard monitoring intervals
    - High risk: More frequent assessments
    - Earlier intervention if suboptimal response
    - Personalized treatment milestones
    
    Patient Communication:
    - Prognostic information in understandable terms
    - Treatment expectations and timelines
    - Importance of adherence and monitoring
    - Long-term outlook and quality of life
    
    Quality Improvement:
    - Outcome prediction and benchmarking
    - Treatment response tracking
    - Population health management
    - Clinical research stratification
    
    Model Performance and Validation:
    - Derived from 2,060 patients across multiple centers
    - Validated in European LeukamiaNet registry
    - Good discrimination between risk groups
    - Practical clinical implementation
    - Maintains prognostic value across age groups
    
    Important Clinical Considerations:
    - Designed for newly-diagnosed patients only
    - Developed in imatinib-treated cohorts
    - Should complement comprehensive clinical assessment
    - Regular re-evaluation during treatment recommended
    - Consider local institutional experience and outcomes
    
    Limitations and Cautions:
    - Outcomes may differ with newer TKI therapies
    - Spleen assessment subjective but clinically relevant
    - Population-based predictions may not reflect individual outcomes
    - Mixed validation results in some cohorts
    - Should be integrated with other clinical factors
    
    Reference: Hasford J, et al. Blood. 2011;118(3):686-92.
    """
    
    result: float = Field(
        ...,
        description="EUTOS Score calculated from basophil percentage and spleen size (range: 0-400+ points)",
        example=38.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EUTOS Score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk level, prognosis, and management recommendations",
        example="EUTOS Score: 38.5 points (≤87 = Low Risk). 5-year progression-free survival: 90%, complete cytogenetic response at 18 months: 86%. Standard imatinib therapy recommended with routine monitoring. Excellent prognosis expected with first-line tyrosine kinase inhibitor treatment."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification level (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low risk for CML progression"
    )
    
    probability_no_ccyr: float = Field(
        ...,
        description="Probability of not achieving complete cytogenetic response at 18 months (%)",
        example=12.5
    )
    
    five_year_pfs: str = Field(
        ...,
        description="Expected 5-year progression-free survival percentage",
        example="90%"
    )
    
    ccyr_18_months: str = Field(
        ...,
        description="Expected complete cytogenetic response rate at 18 months",
        example="86%"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 38.5,
                "unit": "points",
                "interpretation": "EUTOS Score: 38.5 points (≤87 = Low Risk). 5-year progression-free survival: 90%, complete cytogenetic response at 18 months: 86%. Standard imatinib therapy recommended with routine monitoring. Excellent prognosis expected with first-line tyrosine kinase inhibitor treatment.",
                "stage": "Low Risk",
                "stage_description": "Low risk for CML progression",
                "probability_no_ccyr": 12.5,
                "five_year_pfs": "90%",
                "ccyr_18_months": "86%"
            }
        }
"""
FourAt calculation models
"""

from pydantic import BaseModel, Field
from enum import Enum


class AlertnessType(str, Enum):
    """Enum for alertness level in 4AT"""
    NORMAL = "normal"
    ALTERED = "altered"


class AttentionMonthsType(str, Enum):
    """Enum for attention test performance in 4AT"""
    SEVEN_OR_MORE = "7_or_more"
    STARTS_BUT_LESS_7 = "starts_but_less_7"
    REFUSES_UNTESTABLE = "refuses_untestable"


class AcuteChangeType(str, Enum):
    """Enum for acute change presence in 4AT"""
    PRESENT = "present"
    ABSENT = "absent"


class FourAtRequest(BaseModel):
    """
    Request model for 4AT (4 A's Test) Delirium Screening Tool
    
    The 4AT is a rapid, validated screening tool for delirium detection in elderly patients
    and acute care settings. It can be completed in <2 minutes and requires no special
    training, making it ideal for routine clinical use.
    
    **Clinical Applications**:
    - Delirium screening in emergency departments
    - Acute care and hospital ward assessments
    - Post-operative delirium detection
    - Geriatric and elderly care evaluations
    - ICU delirium screening (when appropriate)
    - Cognitive impairment differentiation
    
    **Test Components (4 A's)**:
    1. **Alertness**: Normal vs. altered consciousness
    2. **AMT4**: Abbreviated Mental Test (age, DOB, place, year)
    3. **Attention**: Months backwards test
    4. **Acute change**: Fluctuating course or acute onset
    
    **Scoring System**:
    - Alertness: Normal (0), Altered (4)
    - AMT4 errors: 0 errors (0), 1 error (1), ≥2 errors (2)
    - Attention: ≥7 months (0), starts but <7 (1), refuses/untestable (2)
    - Acute change: Absent (0), Present (4)
    
    **Interpretation Thresholds**:
    - 0 points: Delirium unlikely
    - 1-3 points: Possible cognitive impairment
    - ≥4 points: Possible delirium (requires clinical assessment)
    
    **Clinical Validation**:
    - Sensitivity: 89.7% for delirium detection
    - Specificity: 84.1% for delirium exclusion
    - Validated across multiple healthcare settings
    - Superior to many longer assessment tools
    
    **References**:
    - Bellelli G, et al. Validation of the 4AT, a new instrument for rapid delirium screening: a study in 234 hospitalised older people. Age Ageing. 2014;43(4):496-502.
    - Shenkin SD, et al. Delirium detection in older acute medical inpatients: a multicentre prospective comparative diagnostic test accuracy study of the 4AT and the confusion assessment method. BMC Med. 2019;17(1):138.
    """
    alertness: AlertnessType = Field(
        ..., 
        description="Patient's alertness level. Normal alertness (0 points) vs. altered alertness including mild drowsiness, hypervigilance, or clearly abnormal alertness (4 points)."
    )
    amt4_errors: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Number of errors in Abbreviated Mental Test 4 (AMT4): patient's age, date of birth, current place, current year. 0 errors = 0 points, 1 error = 1 point, ≥2 errors = 2 points."
    )
    attention_months: AttentionMonthsType = Field(
        ..., 
        description="Performance on attention test (months of year in reverse order). Achieves ≥7 months correctly (0 points), starts but <7 months (1 point), refuses or untestable (2 points)."
    )
    acute_change: AcuteChangeType = Field(
        ..., 
        description="Evidence of acute change or fluctuating course in cognition, behavior, or function. Absent (0 points) or present (4 points). Key feature distinguishing delirium from dementia."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "alertness": "normal",
                "amt4_errors": 1,
                "attention_months": "7_or_more",
                "acute_change": "absent"
            }
        }


class FourAtResponse(BaseModel):
    """
    Response model for 4AT (4 A's Test) Delirium Screening
    
    Provides rapid delirium screening results with clinical interpretation
    and management recommendations based on validated thresholds.
    
    **Score Interpretation**:
    - 0 points: Delirium unlikely, no cognitive impairment detected
    - 1-3 points: Possible cognitive impairment, further assessment needed
    - ≥4 points: Possible delirium, requires immediate clinical evaluation
    
    **Clinical Actions by Score**:
    - Score 0: Continue routine monitoring
    - Score 1-3: Detailed cognitive assessment, investigate causes
    - Score ≥4: Delirium workup, identify precipitants, consider interventions
    
    **Important Considerations**:
    - Not diagnostic - clinical judgment required
    - False positives possible in severe dementia
    - Acute change component is crucial for delirium diagnosis
    - May be affected by hearing/visual impairments
    """
    result: int = Field(
        ..., 
        description="Total 4AT score ranging from 0-12 points. Higher scores indicate greater likelihood of delirium or cognitive impairment."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the screening score"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with delirium probability assessment and recommended clinical actions based on validated thresholds."
    )
    stage: str = Field(
        ..., 
        description="Classification result (Negative, Cognitive Impairment, Possible Delirium) based on score thresholds and clinical significance"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the screening result with clinical implications and recommended next steps"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Score ≥4 suggests possible delirium. This result is not diagnostic - the final diagnosis must be based on clinical judgment. Comprehensive mental assessment and investigation of reversible causes are recommended.",
                "stage": "Possible Delirium",
                "stage_description": "Result suggests delirium"
            }
        }

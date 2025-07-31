"""
Aims calculation models
"""

from pydantic import BaseModel, Field
from typing import Any
from enum import Enum


class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"


class AimsRequest(BaseModel):
    """
    Request model for Abnormal Involuntary Movement Scale (AIMS)
    
    The AIMS is a standardized rating scale developed by the National Institute of Mental Health 
    to assess tardive dyskinesia (TD) in patients receiving neuroleptic medications. It provides 
    systematic evaluation of involuntary movements across different body regions.
    
    **Clinical Applications**:
    - Tardive dyskinesia detection and monitoring
    - Antipsychotic medication safety assessment
    - Longitudinal tracking of movement disorders
    - Clinical trial endpoints for TD studies
    - Medico-legal documentation of drug-induced movements
    - Treatment response monitoring
    
    **Assessment Areas**:
    1. **Facial/Oral Movements**: Face, lips, jaw, tongue
    2. **Extremity Movements**: Arms, hands, legs, feet
    3. **Trunk Movements**: Neck, shoulders, hips
    4. **Global Assessment**: Overall severity and impact
    
    **Scoring System**:
    - 0 = None (no abnormal movements)
    - 1 = Minimal (may be extreme normal)
    - 2 = Mild (abnormal but not disabling)
    - 3 = Moderate (abnormal and somewhat disabling)
    - 4 = Severe (abnormal and markedly disabling)
    
    **TD Diagnosis Criteria**:
    - Any single item rated ≥3 (moderate-severe), OR
    - Any two items rated ≥2 (mild or greater)
    - Must persist for ≥4 weeks after drug discontinuation
    
    **Risk Factors for TD**:
    - Age >50 years, female gender, diabetes
    - Duration and dose of antipsychotic exposure
    - First-generation > second-generation antipsychotics
    - Concurrent anticholinergic use
    
    **References**:
    - Guy W. ECDEU Assessment Manual for Psychopharmacology. Rockville, MD: US Department of Health, Education, and Welfare; 1976.
    - Schooler NR, Kane JM. Research diagnoses for tardive dyskinesia. Arch Gen Psychiatry. 1982;39(4):486-7.
    """
    facial_muscles: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Facial muscles and facial expression movements including forehead, eyebrows, periorbital area, cheeks. Includes frowning, blinking, smiling, grimacing."
    )
    lips_perioral: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Lips and perioral area movements including puckering, pouting, smacking. Common early sign of tardive dyskinesia."
    )
    jaw: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Jaw movements including biting, clenching, chewing, mouth opening, lateral movement. May interfere with speech and eating."
    )
    tongue: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Tongue movements both in and out of mouth. Rate only increases in movement, NOT inability to sustain movement. Darting movements are characteristic."
    )
    upper_extremities: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Upper extremity movements (arms, wrists, hands, fingers). Include choreic (rapid, irregular) and athetoid (slow, complex) movements. Exclude tremor."
    )
    lower_extremities: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Lower extremity movements (legs, knees, ankles, toes) including lateral knee movement, foot tapping, heel dropping, foot squirming, inversion/eversion."
    )
    trunk_movements: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Trunk movements of neck, shoulders, hips including rocking, twisting, squirming, pelvic gyrations. May affect posture and gait."
    )
    global_severity: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Global assessment of overall severity of abnormal movements considering frequency, amplitude, and functional impact."
    )
    incapacitation: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Degree of incapacitation due to abnormal movements affecting daily activities, work, social functioning, and quality of life."
    )
    patient_awareness: int = Field(
        ..., 
        ge=0, 
        le=4, 
        description="Patient's awareness of abnormal movements: 0=no awareness, 1=aware/no distress, 2=mild distress, 3=moderate distress, 4=severe distress."
    )
    current_problems_teeth: YesNoType = Field(
        ..., 
        description="Current problems with teeth and/or dentures that might affect oral movement assessment or be affected by oral dyskinesia."
    )
    dental_problems_interfere: YesNoType = Field(
        ..., 
        description="Whether dental problems interfere with the assessment of oral movements or are exacerbated by tardive dyskinesia."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "facial_muscles": 2,
                "lips_perioral": 1,
                "jaw": 2,
                "tongue": 3,
                "upper_extremities": 1,
                "lower_extremities": 2,
                "trunk_movements": 1,
                "global_severity": 2,
                "incapacitation": 2,
                "patient_awareness": 3,
                "current_problems_teeth": "no",
                "dental_problems_interfere": "no"
            }
        }


class AimsResponse(BaseModel):
    """
    Response model for Abnormal Involuntary Movement Scale (AIMS)
    
    Provides comprehensive tardive dyskinesia assessment with clinical significance
    evaluation and management recommendations based on standardized criteria.
    
    **Diagnostic Interpretation**:
    - No TD: Score ≤1 and no items ≥2
    - Mild-Moderate TD: Any item ≥2 or total score 2-13
    - Severe TD: Total score ≥14 or marked functional impairment
    
    **Clinical Significance**:
    - Rating of 2 or higher indicates abnormal movements
    - Two or more items ≥2 suggests probable TD
    - Single item ≥3 indicates definite abnormal movements
    - Global severity and incapacitation guide treatment urgency
    
    **Management Recommendations**:
    - Mild TD: Consider dose reduction, switch to lower-risk antipsychotic
    - Moderate TD: Evaluate risk-benefit, consider TD-specific treatments
    - Severe TD: Urgent intervention, TD-specific medications (VMAT2 inhibitors)
    - Monitor progression with regular AIMS assessments
    
    **Treatment Options for TD**:
    - VMAT2 inhibitors: valbenazine, deutetrabenazine
    - Antipsychotic adjustment: dose reduction, switch to clozapine/quetiapine
    - Supportive care: vitamin E, ginkgo biloba (limited evidence)
    """
    result: int = Field(
        ..., 
        description="Total AIMS score (sum of items 1-7) ranging from 0-28 points. Higher scores indicate more severe tardive dyskinesia."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the movement disorder assessment"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with tardive dyskinesia probability, severity assessment, and specific management recommendations."
    )
    stage: str = Field(
        ..., 
        description="Dyskinesia classification (No Dyskinesia, Mild to Moderate Dyskinesia, Severe Dyskinesia) based on validated criteria"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the tardive dyskinesia severity with clinical implications and treatment urgency"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "Evidence of tardive dyskinesia. Re-evaluate need for neuroleptic medication, consider dose reduction or medication change.",
                "stage": "Mild to Moderate Dyskinesia",
                "stage_description": "Presence of tardive dyskinesia"
            }
        }

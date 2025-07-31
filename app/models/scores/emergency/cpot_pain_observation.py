"""
Critical Care Pain Observation Tool (CPOT) Models

Request and response models for CPOT pain assessment calculation.

References (Vancouver style):
1. Gélinas C, Fillion L, Puntillo KA, Viens C, Fortier M. Validation of the critical-care 
   pain observation tool in adult patients. Am J Crit Care. 2006;15(4):420-427.
2. Gélinas C, Harel F, Fillion L, Puntillo KA, Johnston CC. Sensitivity and specificity 
   of the critical-care pain observation tool for the detection of pain in intubated 
   adults after cardiac surgery. J Pain Symptom Manage. 2009;37(1):58-67.
3. Payen JF, Bru O, Bosson JL, et al. Assessing pain in critically ill sedated patients 
   by using a behavioral pain scale. Crit Care Med. 2001;29(12):2258-2263.

The Critical Care Pain Observation Tool (CPOT) is a validated behavioral pain assessment 
tool designed for critically ill adults who cannot self-report pain. It evaluates pain 
using four domains of behavioral indicators: facial expression, body movements, muscle 
tension, and either ventilator compliance (intubated patients) or vocalization (extubated 
patients). Each domain is scored 0-2 points for a total possible score of 0-8 points.

The CPOT is part of the ABCDEF bundle for ICU pain management and has been validated 
across multiple critical care settings for both conscious and unconscious patients.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, List, Dict, Any


class CpotPainObservationRequest(BaseModel):
    """
    Request model for Critical Care Pain Observation Tool (CPOT)
    
    The CPOT assesses pain in critically ill adults using 4 behavioral domains:
    
    Domain 1 - Facial Expression (0-2 points):
    - relaxed_neutral: No muscular tension observed (0 points)
    - tense: Frowning, brow lowering, orbit tightening (1 point)
    - grimacing: All previous facial movements plus eyelids tightly closed (2 points)
    
    Domain 2 - Body Movements (0-2 points):
    - absence_of_movements: Does not move at all (0 points)
    - protection: Slow cautious movements, touching pain site (1 point)
    - restlessness: Pulling tube, attempting to sit up, thrashing (2 points)
    
    Domain 3 - Muscle Tension (0-2 points):
    - relaxed: No resistance to passive movements (0 points)
    - tense_rigid: Resistance to passive movements (1 point)
    - very_tense_rigid: Strong resistance, unable to complete movements (2 points)
    
    Domain 4 - Patient Status Specific (0-2 points):
    For Intubated Patients - Ventilator Compliance:
    - tolerating: Tolerating ventilator or movement (0 points)
    - coughing_tolerating: Coughing but tolerating (1 point)
    - fighting_ventilator: Fighting ventilator (2 points)
    
    For Extubated Patients - Vocalization:
    - normal_tone_no_sound: Talking in normal tone or no sound (0 points)
    - sighing_moaning: Sighing, moaning (1 point)
    - crying_sobbing: Crying out, sobbing (2 points)
    
    Clinical Interpretation:
    - Score ≤2: Minimal to no pain (acceptable level)
    - Score >2: Unacceptable pain level requiring intervention
    
    Assessment Guidelines:
    - Observe patient at rest for 60 seconds before scoring
    - Use during procedures and after procedures for comparison
    - Consider patient's baseline behavior and cultural expressions
    - Reassess within 30 minutes after pain interventions
    
    References (Vancouver style):
    1. Gélinas C, Fillion L, Puntillo KA, Viens C, Fortier M. Validation of the critical-care 
    pain observation tool in adult patients. Am J Crit Care. 2006;15(4):420-427.
    2. Gélinas C, Harel F, Fillion L, Puntillo KA, Johnston CC. Sensitivity and specificity 
    of the critical-care pain observation tool for the detection of pain in intubated 
    adults after cardiac surgery. J Pain Symptom Manage. 2009;37(1):58-67.
    3. Payen JF, Bru O, Bosson JL, et al. Assessing pain in critically ill sedated patients 
    by using a behavioral pain scale. Crit Care Med. 2001;29(12):2258-2263.
    """
    
    facial_expression: Literal["relaxed_neutral", "tense", "grimacing"] = Field(
        ...,
        description="Facial expression assessment. Observe for muscular tension, frowning, brow lowering, and eyelid closure",
        example="tense"
    )
    
    body_movements: Literal["absence_of_movements", "protection", "restlessness"] = Field(
        ...,
        description="Body movements assessment. Observe for protective behaviors, restlessness, and movement patterns",
        example="protection"
    )
    
    muscle_tension: Literal["relaxed", "tense_rigid", "very_tense_rigid"] = Field(
        ...,
        description="Muscle tension assessment. Evaluate resistance to passive movements and overall muscle tone",
        example="tense_rigid"
    )
    
    patient_status: Literal["intubated", "extubated"] = Field(
        ...,
        description="Patient intubation status. Determines which assessment domain to use (ventilator compliance vs vocalization)",
        example="intubated"
    )
    
    ventilator_compliance: Optional[Literal["tolerating", "coughing_tolerating", "fighting_ventilator"]] = Field(
        None,
        description="Compliance with ventilator (required for intubated patients). Assess tolerance of mechanical ventilation",
        example="coughing_tolerating"
    )
    
    vocalization: Optional[Literal["normal_tone_no_sound", "sighing_moaning", "crying_sobbing"]] = Field(
        None,
        description="Vocalization assessment (required for extubated patients). Assess verbal and vocal expressions",
        example="sighing_moaning"
    )
    
    @field_validator('ventilator_compliance')
    def validate_intubated_requires_ventilator_compliance(cls, v, values):
        if values.get('patient_status') == 'intubated' and v is None:
            raise ValueError('ventilator_compliance is required when patient_status is intubated')
        if values.get('patient_status') == 'extubated' and v is not None:
            raise ValueError('ventilator_compliance should not be provided when patient_status is extubated')
        return v
    
    @field_validator('vocalization')
    def validate_extubated_requires_vocalization(cls, v, values):
        if values.get('patient_status') == 'extubated' and v is None:
            raise ValueError('vocalization is required when patient_status is extubated')
        if values.get('patient_status') == 'intubated' and v is not None:
            raise ValueError('vocalization should not be provided when patient_status is intubated')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "facial_expression": "tense",
                "body_movements": "protection",
                "muscle_tension": "tense_rigid",
                "patient_status": "intubated",
                "ventilator_compliance": "coughing_tolerating",
                "vocalization": None
            }
        }


class CpotPainObservationResponse(BaseModel):
    """
    Response model for Critical Care Pain Observation Tool (CPOT)
    
    The CPOT provides a behavioral pain assessment score ranging from 0-8 points:
    - Score ≤2: Minimal to no pain (acceptable level)
    - Score >2: Unacceptable pain level requiring intervention
    
    The tool is designed for critically ill adults who cannot self-report pain and 
    has been validated in both conscious and unconscious ICU patients. It forms 
    part of the ABCDEF bundle for comprehensive ICU pain management.
    
    Clinical Applications:
    - Pain assessment in sedated ICU patients
    - Post-surgical pain monitoring in critical care
    - Evaluation of pain management interventions
    - Quality improvement initiatives for ICU care
    
    Reference: Gélinas C, et al. Am J Crit Care. 2006;15(4):420-427.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=8,
        description="Total CPOT score calculated from behavioral pain indicators (range: 0-8 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CPOT score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with pain assessment and management recommendations",
        example="CPOT score of 4 indicates unacceptable pain level. Consider alternative analgesia, reassess pain management plan, and provide non-pharmacological comfort measures. Reassess within 30 minutes of intervention."
    )
    
    stage: str = Field(
        ...,
        description="Pain level classification (Minimal to No Pain, Unacceptable Pain)",
        example="Unacceptable Pain"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pain level category",
        example="Significant pain requiring intervention"
    )
    
    scoring_breakdown: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of scores for each assessed domain",
        example={
            "facial_expression": {
                "value": "Tense",
                "score": 1,
                "description": "Frowning, brow lowering, orbit tightening"
            },
            "body_movements": {
                "value": "Protection",
                "score": 1,
                "description": "Slow cautious movements, touching or guarding pain site"
            },
            "muscle_tension": {
                "value": "Tense Rigid",
                "score": 1,
                "description": "Resistance to passive movements"
            },
            "ventilator_compliance": {
                "value": "Coughing Tolerating",
                "score": 1,
                "description": "Coughing but tolerating ventilation"
            }
        }
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Evidence-based clinical recommendations for pain management based on the score",
        example={
            "pain_management": "Consider increasing analgesic dose or alternative medications",
            "monitoring": "Frequent pain assessments (every 30 minutes after intervention)",
            "interventions": [
                "Administer additional analgesic as ordered",
                "Non-pharmacological comfort measures (positioning, massage, distraction)",
                "Environmental modifications (noise reduction, dimmed lighting)",
                "Consider multimodal pain management approach",
                "Notify physician if score remains >2 after interventions"
            ],
            "reassessment": "Within 30 minutes of pain intervention"
        }
    )
    
    assessment_notes: List[str] = Field(
        ...,
        description="Important notes for proper CPOT assessment and clinical application",
        example=[
            "Observe patient at rest for 60 seconds before scoring",
            "Consider patient's baseline behavior and cultural expressions",
            "Use in conjunction with physiological indicators when available",
            "Document specific behaviors observed for each domain",
            "Monitor ventilator synchrony and breathing patterns",
            "Assess for appropriate sedation level",
            "Consider impact of sedatives on behavioral responses"
        ]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "CPOT score of 4 indicates unacceptable pain level. Consider alternative analgesia, reassess pain management plan, and provide non-pharmacological comfort measures. Reassess within 30 minutes of intervention.",
                "stage": "Unacceptable Pain",
                "stage_description": "Significant pain requiring intervention",
                "scoring_breakdown": {
                    "facial_expression": {
                        "value": "Tense",
                        "score": 1,
                        "description": "Frowning, brow lowering, orbit tightening"
                    },
                    "body_movements": {
                        "value": "Protection",
                        "score": 1,
                        "description": "Slow cautious movements, touching or guarding pain site"
                    },
                    "muscle_tension": {
                        "value": "Tense Rigid",
                        "score": 1,
                        "description": "Resistance to passive movements"
                    },
                    "ventilator_compliance": {
                        "value": "Coughing Tolerating",
                        "score": 1,
                        "description": "Coughing but tolerating ventilation"
                    }
                },
                "clinical_recommendations": {
                    "pain_management": "Consider increasing analgesic dose or alternative medications",
                    "monitoring": "Frequent pain assessments (every 30 minutes after intervention)",
                    "interventions": [
                        "Administer additional analgesic as ordered",
                        "Non-pharmacological comfort measures (positioning, massage, distraction)",
                        "Environmental modifications (noise reduction, dimmed lighting)",
                        "Consider multimodal pain management approach",
                        "Notify physician if score remains >2 after interventions"
                    ],
                    "reassessment": "Within 30 minutes of pain intervention"
                },
                "assessment_notes": [
                    "Observe patient at rest for 60 seconds before scoring",
                    "Consider patient's baseline behavior and cultural expressions",
                    "Use in conjunction with physiological indicators when available",
                    "Document specific behaviors observed for each domain",
                    "Monitor ventilator synchrony and breathing patterns",
                    "Assess for appropriate sedation level",
                    "Consider impact of sedatives on behavioral responses"
                ]
            }
        }
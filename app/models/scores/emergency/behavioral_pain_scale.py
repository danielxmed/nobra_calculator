"""
Behavioral Pain Scale (BPS) Models

Request and response models for BPS calculation.

References (Vancouver style):
1. Payen JF, Bru O, Bosson JL, Lagrasta A, Novel E, Deschaux I, et al. Assessing 
   pain in critically ill sedated patients by using a behavioral pain scale. 
   Crit Care Med. 2001 Dec;29(12):2258-63.
2. Ahlers SJ, van Gulik L, van der Veen AM, van Dongen HP, de Boer A, Tibboel D, et al. 
   Comparison of different pain scoring systems in critically ill patients in a general ICU. 
   Crit Care. 2008;12(1):R15.
3. Chanques G, Sebbane M, Barbotte E, Viel E, Eledjam JJ, Jaber S. A prospective 
   study of pain at rest: incidence and characteristics of an unrecognized symptom 
   in surgical and trauma versus medical intensive care unit patients. Anesthesiology. 
   2007 Nov;107(5):858-60.

The Behavioral Pain Scale (BPS) was developed in 2001 specifically for critically ill 
intubated patients who cannot self-report pain. It evaluates three behavioral domains: 
facial expression, upper limb movements, and compliance with mechanical ventilation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BehavioralPainScaleRequest(BaseModel):
    """
    Request model for Behavioral Pain Scale (BPS)
    
    The BPS is a validated pain assessment tool designed specifically for critically ill 
    intubated patients who cannot self-report their pain. It is recommended in the 2018 
    PADIS guidelines as one of the two most accurate behavioral pain scales for ICU patients.
    
    Assessment Components:
    
    1. **Facial Expression (1-4 points):**
       - 1: Relaxed - no tension visible in facial muscles
       - 2: Partially tightened (e.g., brow lowering) - slight facial muscle tension
       - 3: Fully tightened (e.g., eyelid closing) - obvious facial muscle tension
       - 4: Grimacing - severe facial distortion indicating significant distress
    
    2. **Upper Limb Movements (1-4 points):**
       - 1: No movement - arms relaxed, no defensive movements
       - 2: Partially bent - slight flexion of arms or hands
       - 3: Fully bent with finger flexion - marked flexion with defensive posturing
       - 4: Permanently retracted - severe contracture or persistent withdrawal
    
    3. **Compliance with Mechanical Ventilation (1-4 points):**
       - 1: Tolerating movement - accepts ventilator breaths without resistance
       - 2: Coughing but tolerating ventilation for most of the time - occasional resistance
       - 3: Fighting ventilator - frequent dyssynchrony with ventilator
       - 4: Unable to control ventilation - complete ventilator dyssynchrony
    
    **Clinical Guidelines:**
    - Target population: Critically ill intubated patients unable to self-report
    - Assessment timing: At rest and during noxious stimuli
    - Frequency: Once per shift or when analgesia changes
    - Pain threshold: Scores ≥6 indicate unacceptable pain requiring intervention
    
    **Validation Evidence:**
    - Validated in surgical, trauma, and medical ICU populations
    - Good psychometric properties and reliability
    - Particularly applicable to mechanically ventilated patients
    - One of two recommended scales in 2018 PADIS guidelines (with CPOT)
    
    **Clinical Context:**
    Approximately 75% of ICU patients report severe pain, with 30% experiencing pain 
    at rest and 50% during nursing procedures. The BPS helps identify and quantify 
    this pain in patients who cannot communicate verbally.
    
    References (Vancouver style):
    1. Payen JF, Bru O, Bosson JL, Lagrasta A, Novel E, Deschaux I, et al. Assessing 
    pain in critically ill sedated patients by using a behavioral pain scale. 
    Crit Care Med. 2001 Dec;29(12):2258-63.
    2. Ahlers SJ, van Gulik L, van der Veen AM, van Dongen HP, de Boer A, Tibboel D, et al. 
    Comparison of different pain scoring systems in critically ill patients in a general ICU. 
    Crit Care. 2008;12(1):R15.
    3. Chanques G, Sebbane M, Barbotte E, Viel E, Eledjam JJ, Jaber S. A prospective 
    study of pain at rest: incidence and characteristics of an unrecognized symptom 
    in surgical and trauma versus medical intensive care unit patients. Anesthesiology. 
    2007 Nov;107(5):858-60.
    """
    
    facial_expression: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Assessment of facial expression indicating pain or distress. 1=Relaxed, 2=Partially tightened (brow lowering), 3=Fully tightened (eyelid closing), 4=Grimacing",
        example=1
    )
    
    upper_limb_movements: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Assessment of upper limb movement patterns. 1=No movement, 2=Partially bent, 3=Fully bent with finger flexion, 4=Permanently retracted",
        example=2
    )
    
    compliance_with_ventilation: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Assessment of patient's compliance with mechanical ventilation. 1=Tolerating movement, 2=Coughing but tolerating most of the time, 3=Fighting ventilator, 4=Unable to control ventilation",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "No pain (BPS = 3)",
                    "value": {
                        "facial_expression": 1,
                        "upper_limb_movements": 1,
                        "compliance_with_ventilation": 1
                    }
                },
                {
                    "title": "Mild pain (BPS = 4)",
                    "value": {
                        "facial_expression": 1,
                        "upper_limb_movements": 2,
                        "compliance_with_ventilation": 1
                    }
                },
                {
                    "title": "Unacceptable pain requiring intervention (BPS = 8)",
                    "value": {
                        "facial_expression": 3,
                        "upper_limb_movements": 3,
                        "compliance_with_ventilation": 2
                    }
                },
                {
                    "title": "Maximum pain (BPS = 12)",
                    "value": {
                        "facial_expression": 4,
                        "upper_limb_movements": 4,
                        "compliance_with_ventilation": 4
                    }
                }
            ]
        }


class BehavioralPainScaleResponse(BaseModel):
    """
    Response model for Behavioral Pain Scale (BPS)
    
    Returns the calculated BPS score with detailed interpretation including:
    - Pain level classification (No Pain: 3, Mild Pain: 4-5, Unacceptable Pain: 6-11, Maximum Pain: 12)
    - Component breakdown showing specific behavioral indicators
    - Clinical management recommendations based on pain level
    - Intervention guidelines for different pain thresholds
    
    The BPS provides a systematic approach to assess pain in critically ill intubated 
    patients, helping healthcare providers make appropriate pain management decisions 
    in ICU settings where traditional pain assessment is not possible.
    
    **Clinical Thresholds:**
    - Score 3: No pain, continue current management
    - Scores 4-5: Mild pain, consider comfort measures
    - Scores 6-11: Unacceptable pain, administer analgesia/sedation
    - Score 12: Maximum pain, immediate intervention required
    
    **Assessment Guidelines:**
    - Use at rest and during noxious stimuli
    - Assess once per shift or when analgesia changes  
    - Reassess 15-30 minutes after interventions
    - More difficult to use in deeply sedated patients
    
    Reference: The BPS is particularly applicable to mechanically ventilated patients 
    as one of its three domains specifically pertains to compliance with ventilation, 
    making it uniquely suited for intubated ICU patients.
    """
    
    result: int = Field(
        ...,
        description="BPS score calculated from behavioral observations (3-12 points total)",
        ge=3,
        le=12,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BPS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including pain level, component breakdown, and specific management recommendations for critically ill intubated patients",
        example="BPS score: 4/12 points. Mild pain behaviors present in this critically ill intubated patient. Facial expression: Relaxed (1 points). Upper limb movements: Partially bent (2 points). Compliance with ventilation: Tolerating movement (1 points). Clinical management: Consider comfort measures including repositioning, environmental modifications, and reassessment in 15-30 minutes. May consider low-dose analgesics based on clinical context and individual patient factors. Monitor for progression of pain behaviors. Document interventions and response to treatment."
    )
    
    stage: str = Field(
        ...,
        description="Pain level classification (No Pain, Mild Pain, Unacceptable Pain, or Maximum Pain)",
        example="Mild Pain"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pain level with clinical significance",
        example="Mild pain behaviors present"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "BPS score: 4/12 points. Mild pain behaviors present in this critically ill intubated patient. Facial expression: Relaxed (1 points). Upper limb movements: Partially bent (2 points). Compliance with ventilation: Tolerating movement (1 points). Clinical management: Consider comfort measures including repositioning, environmental modifications, and reassessment in 15-30 minutes. May consider low-dose analgesics based on clinical context and individual patient factors. Monitor for progression of pain behaviors. Document interventions and response to treatment.",
                "stage": "Mild Pain",
                "stage_description": "Mild pain behaviors present"
            }
        }
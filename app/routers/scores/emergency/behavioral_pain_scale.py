"""
Behavioral Pain Scale (BPS) Router

Endpoint for calculating BPS to quantify pain in critically ill intubated patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.behavioral_pain_scale import (
    BehavioralPainScaleRequest,
    BehavioralPainScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/behavioral_pain_scale", response_model=BehavioralPainScaleResponse)
async def calculate_behavioral_pain_scale(request: BehavioralPainScaleRequest):
    """
    Calculates Behavioral Pain Scale (BPS) for Pain Assessment in Intubated Patients
    
    The BPS is a validated pain assessment tool specifically designed for critically ill 
    intubated patients who cannot self-report their pain. It is one of the two behavioral 
    pain scales recommended in the 2018 PADIS guidelines for ICU patients.
    
    **Target Population:**
    - Critically ill intubated patients
    - Patients unable to self-report pain
    - Mechanically ventilated patients in ICU settings
    - Sedated patients requiring pain assessment
    
    **Assessment Components (1-4 points each):**
    
    **1. Facial Expression:**
    - 1: Relaxed - no tension visible in facial muscles
    - 2: Partially tightened (e.g., brow lowering) - slight facial muscle tension
    - 3: Fully tightened (e.g., eyelid closing) - obvious facial muscle tension
    - 4: Grimacing - severe facial distortion indicating significant distress
    
    **2. Upper Limb Movements:**
    - 1: No movement - arms relaxed, no defensive movements
    - 2: Partially bent - slight flexion of arms or hands
    - 3: Fully bent with finger flexion - marked flexion with defensive posturing
    - 4: Permanently retracted - severe contracture or persistent withdrawal
    
    **3. Compliance with Mechanical Ventilation:**
    - 1: Tolerating movement - accepts ventilator breaths without resistance
    - 2: Coughing but tolerating ventilation for most of the time - occasional resistance
    - 3: Fighting ventilator - frequent dyssynchrony with ventilator
    - 4: Unable to control ventilation - complete ventilator dyssynchrony
    
    **Scoring and Interpretation:**
    - **Total Score Range:** 3-12 points
    - **No Pain (3 points):** Continue current management, routine monitoring
    - **Mild Pain (4-5 points):** Consider comfort measures, may need low-dose analgesics
    - **Unacceptable Pain (6-11 points):** Requires sedation and/or analgesia
    - **Maximum Pain (12 points):** Immediate intervention required
    
    **Clinical Assessment Guidelines:**
    - **Assessment Timing:** At rest and during noxious stimuli
    - **Frequency:** Once per shift or when analgesia changes
    - **Intervention Threshold:** Scores ≥6 warrant analgesia and/or sedation
    - **Reassessment:** 15-30 minutes after pain interventions
    
    **Validation Evidence:**
    - **Development:** Created by Payen et al. in 2001 specifically for ICU patients
    - **Populations:** Validated in surgical, trauma, and medical ICU patients
    - **Psychometric Properties:** Good reliability and validity demonstrated
    - **Guidelines:** Recommended in 2018 PADIS guidelines (with CPOT)
    - **Applicability:** Particularly suited for mechanically ventilated patients
    
    **Clinical Context:**
    Pain is highly prevalent in critically ill patients, with approximately:
    - 75% reporting severe pain overall
    - 30% experiencing pain at rest
    - 50% experiencing pain during nursing procedures
    
    The BPS addresses this critical need by providing objective pain assessment 
    when traditional self-report methods are impossible.
    
    **Advantages:**
    - Specifically designed for intubated patients
    - Includes ventilation compliance component unique to mechanically ventilated patients
    - Well-validated across diverse ICU populations
    - Simple 3-component assessment
    - Standardized scoring system
    - Excellent inter-rater reliability
    
    **Limitations:**
    - More difficult to use in patients under deep sedation
    - Requires training for consistent application
    - May be influenced by sedative medications
    - Should be used in conjunction with clinical judgment
    
    **Comparison with CPOT:**
    The BPS and Critical Care Pain Observation Tool (CPOT) are the two recommended 
    behavioral pain scales in ICU settings. BPS is particularly applicable to 
    mechanically ventilated patients due to its ventilation compliance component.
    
    Args:
        request: BPS assessment parameters (facial expression, upper limb movements, ventilation compliance)
        
    Returns:
        BehavioralPainScaleResponse: BPS score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("behavioral_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Behavioral Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BehavioralPainScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BPS calculation",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )
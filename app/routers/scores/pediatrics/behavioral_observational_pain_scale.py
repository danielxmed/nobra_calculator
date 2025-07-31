"""
Behavioral Observational Pain Scale (BOPS) Router

Endpoint for calculating BOPS to quantify post-operative pain in pediatric patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.behavioral_observational_pain_scale import (
    BehavioralObservationalPainScaleRequest,
    BehavioralObservationalPainScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/behavioral_observational_pain_scale",
    response_model=BehavioralObservationalPainScaleResponse,
    summary="Calculate Behavioral Observational Pain Scale",
    description="Quantifies post-operative pain for children aged 1-7 years using observational behavioral indicators",
    response_description="The calculated behavioral observational pain scale with interpretation",
    operation_id="behavioral_observational_pain_scale"
)
async def calculate_behavioral_observational_pain_scale(request: BehavioralObservationalPainScaleRequest):
    """
    Calculates Behavioral Observational Pain Scale (BOPS) for Post-Op Pediatric Pain
    
    The BOPS is a validated pediatric pain assessment tool specifically designed for 
    children aged 1-7 years in post-operative settings. It provides objective measurement 
    of pain through behavioral observation.
    
    **Target Population:**
    - Children aged 1-7 years
    - Post-operative patients
    - Non-verbal or limited verbal communication children
    
    **Assessment Components (0-2 points each):**
    
    **1. Facial Expression:**
    - 0: Neutral/positive facial expression, composed, calm
    - 1: Negative facial expression, concerned
    - 2: Negative facial expression, grimace, distorted face
    
    **2. Verbalization:**
    - 0: Normal conversation, laugh, crow
    - 1: Completely quiet, sobbing and/or complaining but not because of pain
    - 2: Crying, screaming and/or complaining about pain
    
    **3. Body Position:**
    - 0: Inactive, laying, relaxed with all extremities or sitting, walking
    - 1: Restless movements, shifting fashion and/or touching wound or wound area
    - 2: Lying rigid and/or drawn up with arms and legs to the body
    
    **Scoring and Interpretation:**
    - **Total Score Range:** 0-6 points
    - **Minimal Pain (0-2 points):** Continue comfort measures, no immediate analgesia needed
    - **Significant Pain (3-6 points):** Consider analgesia administration
    
    **Clinical Assessment Guidelines:**
    - **Routine Assessment:** Every 3 hours
    - **Post-IV Analgesia:** Reassess 15-20 minutes after administration
    - **Post-Oral/Rectal Analgesia:** Reassess 30-45 minutes after administration
    - **Threshold for Intervention:** Scores ≥3 warrant analgesia consideration
    
    **Validation Evidence:**
    - **Interrater Reliability:** Excellent (κw 0.86 to 0.95 for each item)
    - **Concurrent Validity:** Strong correlation with CHEOPS scale (rs = 0.871, p < 0.001)
    - **Clinical Utility:** Simple scoring system easy to incorporate in postoperative units
    - **Development:** Created in 1996 at Neurointensive Care Unit in Lund, Sweden
    
    **Clinical Applications:**
    - Post-operative pain monitoring in pediatric units
    - Pain assessment in ICU settings
    - Evaluation of analgesic effectiveness
    - Documentation for pain management protocols
    - Research studies on pediatric pain interventions
    
    **Advantages over Self-Report:**
    - Does not require verbal communication from child
    - Suitable for children with developmental delays
    - Objective behavioral indicators
    - Standardized assessment approach
    - Reliable across different healthcare providers
    
    Args:
        request: BOPS assessment parameters (facial expression, verbalization, body position)
        
    Returns:
        BehavioralObservationalPainScaleResponse: BOPS score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("behavioral_observational_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Behavioral Observational Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BehavioralObservationalPainScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BOPS calculation",
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
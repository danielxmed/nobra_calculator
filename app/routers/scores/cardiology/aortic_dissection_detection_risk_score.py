"""
Aortic Dissection Detection Risk Score (ADD-RS) Router

Endpoint for calculating ADD-RS for risk stratification of suspected acute aortic dissection.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.aortic_dissection_detection_risk_score import (
    AorticDissectionDetectionRiskScoreRequest,
    AorticDissectionDetectionRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/aortic_dissection_detection_risk_score", response_model=AorticDissectionDetectionRiskScoreResponse, summary="Calculate Aortic Dissection Detection Risk Score", description="Calculates Aortic Dissection Detection Risk Score", response_description="Risk score with clinical interpretation and recommended care level", operation_id="aortic_dissection_detection_risk_score")
async def calculate_aortic_dissection_detection_risk_score(request: AorticDissectionDetectionRiskScoreRequest):
    """
    Calculates Aortic Dissection Detection Risk Score (ADD-RS)
    
    A guideline-based clinical screening tool for identification of acute aortic dissection 
    at initial presentation. The ADD-RS stratifies patients into low, intermediate, and 
    high-risk categories based on the presence of high-risk features in three domains:
    
    **Risk Categories:**
    1. **Predisposing Conditions**: Marfan syndrome, family history of aortic disease, 
       known aortic valve disease, recent aortic manipulation, known thoracic aortic aneurysm
    2. **Pain Features**: Abrupt onset, severe intensity, ripping/tearing quality
    3. **Examination Features**: Pulse deficit/BP differential, focal neurological deficit 
       with pain, new aortic insufficiency murmur with pain, hypotension/shock
    
    **Risk Stratification:**
    - **Score 0 (Low Risk)**: Consider chest X-ray; if widened mediastinum or no alternative 
      diagnosis, consider aortic imaging
    - **Score 1 (Intermediate Risk)**: Consider D-dimer testing or proceed to aortic imaging
    - **Score 2-3 (High Risk)**: Proceed immediately to definitive aortic imaging
    
    **Performance**: 95.7% sensitivity for detecting acute aortic dissection in validation 
    study of 2538 confirmed cases from the International Registry of Acute Aortic Dissection.
    
    **Clinical Notes:**
    - Designed for bedside screening of large patient volumes
    - Should be used in conjunction with clinical judgment
    - Not validated for specificity - may result in over-testing in low-prevalence populations
    - D-dimer may be helpful in intermediate-risk patients where available
    
    Args:
        request: Clinical assessment parameters for ADD-RS calculation
        
    Returns:
        AorticDissectionDetectionRiskScoreResponse: Risk score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("aortic_dissection_detection_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Aortic Dissection Detection Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AorticDissectionDetectionRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Aortic Dissection Detection Risk Score",
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
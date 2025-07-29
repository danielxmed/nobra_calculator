"""
International Prostate Symptom Score (IPSS)/AUA Symptom Index Router

Endpoint for calculating IPSS/AUA-SI BPH symptom severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.urology.ipss_aua_si import (
    IpssAuaSiRequest,
    IpssAuaSiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ipss_aua_si", response_model=IpssAuaSiResponse)
async def calculate_ipss_aua_si(request: IpssAuaSiRequest):
    """
    Calculates International Prostate Symptom Score (IPSS)/AUA Symptom Index
    
    The IPSS/AUA-SI is the gold standard questionnaire for assessing the severity 
    of lower urinary tract symptoms in men with benign prostatic hyperplasia (BPH). 
    This validated 7-question instrument quantifies urinary symptoms to guide 
    treatment decisions and monitor therapeutic response.
    
    The questionnaire evaluates:
    - Incomplete bladder emptying sensation
    - Urinary frequency (less than 2-hour intervals)
    - Intermittent urinary stream
    - Urinary urgency and difficulty postponing urination
    - Weak urinary stream strength
    - Straining required to initiate urination
    - Nocturia (nighttime urination episodes)
    
    Each question is scored 0-5 points based on symptom frequency:
    - 0: Not at all
    - 1: Less than 1 in 5 times
    - 2: Less than half the time
    - 3: About half the time
    - 4: More than half the time
    - 5: Almost always
    
    (Nocturia scored by actual episodes: 0=none, 1=1 time, 2=2 times, etc.)
    
    Symptom severity classification and treatment guidance:
    - Mild (0-7): Watchful waiting, lifestyle modifications
    - Moderate (8-19): Medical therapy (alpha-blockers, 5-ARIs)
    - Severe (20-35): Medical therapy required, consider surgical options
    
    Args:
        request: Seven urinary symptom parameters, each scored 0-5 points
        
    Returns:
        IpssAuaSiResponse: Total symptom score with severity classification 
        and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ipss_aua_si", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating International Prostate Symptom Score (IPSS)/AUA Symptom Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return IpssAuaSiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for International Prostate Symptom Score (IPSS)/AUA Symptom Index",
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
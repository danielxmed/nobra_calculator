"""
BISAP Score for Pancreatitis Mortality Router

Endpoint for calculating BISAP Score for Pancreatitis Mortality.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.bisap_score import (
    BisapScoreRequest,
    BisapScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bisap_score",
    response_model=BisapScoreResponse,
    summary="Calculate BISAP Score for Pancreatitis Mortality",
    description="Predicts mortality risk in pancreatitis with fewer variables than Ranson's. The Bedside Index for Severity in Acute Pancreatitis (BISAP) allows for early identification of patients at increased risk for in-hospital mortality.",
    response_description="The calculated bisap score with interpretation",
    operation_id="calculate_bisap_score"
)
async def calculate_bisap_score(request: BisapScoreRequest):
    """
    Calculates BISAP Score for Pancreatitis Mortality
    
    The BISAP (Bedside Index for Severity in Acute Pancreatitis) score provides 
    early identification of patients at increased risk for in-hospital mortality 
    in acute pancreatitis, using fewer variables than Ranson's criteria.
    
    **The 5 BISAP Criteria (B-I-S-A-P):**
    - **B**: Blood Urea Nitrogen (BUN) > 25 mg/dL
    - **I**: Impaired mental status or GCS < 15
    - **S**: ≥2 SIRS criteria (pulse >90 bpm, respirations >20/min or PaCO2 <32 mmHg, 
             temperature >38°C or <36°C, WBC >12,000 or <4,000 cells/mm³ or >10% bands)
    - **A**: Age > 60 years
    - **P**: Pleural effusion on imaging
    
    **Risk Stratification:**
    - **0-2 points**: Low risk (mild pancreatitis, <2% mortality)
    - **3-5 points**: High risk (severe pancreatitis, 15-20% mortality)
    
    **Clinical Utility:**
    - Can be calculated within 24 hours of admission
    - More convenient than Ranson's criteria with fewer variables
    - Developed from ~18,000 cases across >200 hospitals
    - Validated with 56% sensitivity and 91% specificity for mortality at cutoff ≥3
    
    **Management Implications:**
    - Low risk: Standard supportive care, monitoring for complications
    - High risk: Consider ICU admission, aggressive fluid resuscitation, early nutritional support
    
    Args:
        request: BISAP criteria parameters
        
    Returns:
        BisapScoreResponse: Score with risk stratification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bisap_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BISAP Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BisapScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BISAP Score calculation",
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
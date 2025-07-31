"""
CASPAR Criteria for Psoriatic Arthritis Router

Endpoint for calculating CASPAR Criteria classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.caspar_criteria import (
    CasparCriteriaRequest,
    CasparCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/caspar_criteria",
    response_model=CasparCriteriaResponse,
    summary="Calculate CASPAR Criteria for Psoriatic Arthritis",
    description="Provides standardized classification criteria for identifying psoriatic arthritis (PsA) in patients with inflammatory arthritis. Requires presence of inflammatory articular disease plus ≥3 points from additional criteria.",
    response_description="The calculated caspar criteria with interpretation",
    operation_id="caspar_criteria"
)
async def calculate_caspar_criteria(request: CasparCriteriaRequest):
    """
    Calculates CASPAR Criteria for Psoriatic Arthritis
    
    Provides standardized classification criteria for identifying psoriatic arthritis (PsA) 
    in patients with inflammatory arthritis. The CASPAR criteria are designed primarily 
    for research and clinical trial patient selection.
    
    Requirements:
    1. MANDATORY: Inflammatory articular disease (joint, spine, or entheseal)
    2. ADDITIONAL: ≥3 points from scoring criteria
    
    Scoring System:
    - Current psoriasis (diagnosed by rheumatologist/dermatologist): 2 points
    - Personal/family history of psoriasis: 1 point
    - Nail dystrophy (onycholysis, pitting, hyperkeratosis): 1 point
    - Rheumatoid factor negative: 1 point
    - Dactylitis (current or historical): 1 point
    - Juxtaarticular new bone formation on X-ray: 1 point
    
    Clinical Performance:
    - Sensitivity: 91%
    - Specificity: 98%
    - Developed from international study of 588 PsA patients
    
    Important: CASPAR criteria are classification criteria for research purposes,
    not diagnostic criteria for individual clinical practice.
    
    Args:
        request: Parameters needed for CASPAR classification
        
    Returns:
        CasparCriteriaResponse: Classification result with detailed scoring breakdown
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("caspar_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CASPAR Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return CasparCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CASPAR Criteria",
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
"""
Overall Neuropathy Limitations Scale (ONLS) Router

Endpoint for calculating ONLS score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.onls import (
    OnlsRequest,
    OnlsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/onls",
    response_model=OnlsResponse,
    summary="Calculate Overall Neuropathy Limitations Scale (ONLS)",
    description="Calculates the Overall Neuropathy Limitations Scale (ONLS), a validated functional "
                "assessment tool that quantifies disability in patients with peripheral neuropathy by "
                "evaluating upper and lower extremity functional activities. This scale combines arms "
                "functional grade (0-5) and legs functional grade (0-7) for a total score of 0-12 points. "
                "The ONLS is widely used in clinical practice and research to monitor disease progression "
                "and treatment response in various neuropathic conditions, particularly immune-mediated "
                "polyneuropathies like CIDP and Guillain-Barré syndrome. The scale demonstrates excellent "
                "inter-rater reliability (ICC=0.97) and acceptable responsiveness for detecting functional "
                "changes over time. Higher scores indicate greater functional disability requiring more "
                "intensive interventions and support services.",
    response_description="The calculated ONLS score with comprehensive functional assessment and clinical management recommendations",
    operation_id="onls"
)
async def calculate_onls(request: OnlsRequest):
    """
    Calculates Overall Neuropathy Limitations Scale (ONLS)
    
    This validated scale quantifies functional disability in peripheral neuropathy
    patients by assessing upper and lower extremity functional activities.
    
    Args:
        request: Arms and legs functional disability grades
        
    Returns:
        OnlsResponse: Result with functional assessment and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("onls", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Overall Neuropathy Limitations Scale (ONLS)",
                    "details": {"parameters": parameters}
                }
            )
        
        return OnlsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Overall Neuropathy Limitations Scale (ONLS)",
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
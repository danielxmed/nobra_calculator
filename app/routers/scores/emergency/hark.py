"""
HARK (Humiliation, Afraid, Rape, Kick) Router

Endpoint for HARK intimate partner violence screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hark import (
    HarkRequest,
    HarkResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hark",
    response_model=HarkResponse,
    summary="Calculate HARK (Humiliation, Afraid, Rape, Kick) Score",
    description="Screens for intimate partner violence in adult women using a validated 4-question "
                "tool. The HARK instrument assesses different types of IPV in the past year: "
                "Humiliation (emotional/psychological abuse), Afraid (fear-based intimidation), "
                "Rape (sexual violence), and Kick (physical violence). Each question is scored "
                "as yes (1 point) or no (0 points), with a total range of 0-4 points. A score "
                "≥1 indicates a positive screen requiring immediate safety assessment, documentation, "
                "resource provision, and follow-up care planning. This brief screening tool is "
                "suitable for busy clinical settings and helps identify women experiencing IPV "
                "who may benefit from intervention and support services.",
    response_description="The calculated HARK score with screening result, identified abuse types, "
                        "and safety assessment requirements",
    operation_id="hark"
)
async def calculate_hark(request: HarkRequest):
    """
    Calculates HARK (Humiliation, Afraid, Rape, Kick) Score
    
    Performs intimate partner violence screening using four questions that assess 
    different types of abuse experienced in the past year by current or former partners.
    
    Args:
        request: Four yes/no questions about different types of intimate partner violence
        
    Returns:
        HarkResponse: Score (0-4) with screening result and safety assessment requirements
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hark", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HARK score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HarkResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HARK calculation",
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
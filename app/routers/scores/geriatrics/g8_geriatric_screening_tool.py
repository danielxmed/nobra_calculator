"""
G8 Geriatric Screening Tool Router

Endpoint for calculating G8 Geriatric Screening Tool.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.g8_geriatric_screening_tool import (
    G8GeriatricScreeningToolRequest,
    G8GeriatricScreeningToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/g8_geriatric_screening_tool",
    response_model=G8GeriatricScreeningToolResponse,
    summary="Calculate G8 Geriatric Screening Tool",
    description="Identifies older cancer patients who could benefit from comprehensive geriatric assessment (CGA). The G8 is a validated screening tool that evaluates multiple geriatric domains including nutrition, mobility, cognition, and functional status to determine which elderly cancer patients require full geriatric evaluation.",
    response_description="The calculated g8 geriatric screening tool with interpretation",
    operation_id="calculate_g8_geriatric_screening_tool"
)
async def calculate_g8_geriatric_screening_tool(request: G8GeriatricScreeningToolRequest):
    """
    Calculates G8 Geriatric Screening Tool
    
    Identifies older cancer patients who could benefit from comprehensive geriatric 
    assessment (CGA). The G8 is a validated 8-item screening questionnaire that evaluates 
    multiple geriatric domains including nutrition, mobility, cognition, and functional 
    status to determine which elderly cancer patients require full geriatric evaluation.
    
    The tool incorporates 7 items from the Mini Nutritional Assessment (MNA) plus patient 
    age to create a comprehensive screening instrument suitable for routine use in oncology 
    settings. A score ≤14 points indicates high risk for geriatric impairment and 
    recommends comprehensive geriatric assessment.
    
    Args:
        request: Parameters needed for G8 calculation including age, nutrition, mobility,
                cognition, medications, and self-perceived health status
        
    Returns:
        G8GeriatricScreeningToolResponse: Result with clinical interpretation and 
                                        recommendations for geriatric assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("g8_geriatric_screening_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating G8 Geriatric Screening Tool",
                    "details": {"parameters": parameters}
                }
            )
        
        return G8GeriatricScreeningToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for G8 Geriatric Screening Tool",
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
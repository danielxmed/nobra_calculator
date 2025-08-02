"""
Travis Criteria Router

Endpoint for calculating Travis Criteria to predict risk of colectomy in severe ulcerative colitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.travis_criteria import (
    TravisCriteriaRequest,
    TravisCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/travis_criteria",
    response_model=TravisCriteriaResponse,
    summary="Calculate Travis Criteria",
    description="Calculates the Travis Criteria to predict risk of needing colectomy in patients with "
                "severe ulcerative colitis. Used on day 3 of treatment for acute severe ulcerative "
                "colitis to predict failure of medical therapy. The criteria combine stool frequency "
                "and C-reactive protein (CRP) levels to stratify patients into low or high risk "
                "categories. High-risk patients (>8 stools/day OR 3-8 stools/day with CRP >45 mg/L) "
                "should be considered for early surgical consultation and intensification of therapy.",
    response_description="The calculated risk category with clinical interpretation and management recommendations",
    operation_id="travis_criteria"
)
async def calculate_travis_criteria(request: TravisCriteriaRequest):
    """
    Calculates Travis Criteria for severe ulcerative colitis
    
    The Travis Criteria helps predict which patients with acute severe ulcerative 
    colitis will fail medical therapy and require colectomy. It should be applied 
    on day 3 of inpatient treatment.
    
    Args:
        request: Parameters needed for calculation (stool frequency and CRP status)
        
    Returns:
        TravisCriteriaResponse: Risk category with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("travis_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Travis Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return TravisCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Travis Criteria",
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
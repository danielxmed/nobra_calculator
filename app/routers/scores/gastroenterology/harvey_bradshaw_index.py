"""
Harvey-Bradshaw Index (HBI) for Crohn's Disease Router

Endpoint for calculating Harvey-Bradshaw Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.harvey_bradshaw_index import (
    HarveyBradshawIndexRequest,
    HarveyBradshawIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/harvey_bradshaw_index",
    response_model=HarveyBradshawIndexResponse,
    summary="Calculate Harvey-Bradshaw Index (HBI) for Crohn's Disease",
    description="Calculates the Harvey-Bradshaw Index (HBI) to assess Crohn's disease activity using "
                "only clinical parameters. The HBI is a simplified version of the Crohn's Disease "
                "Activity Index (CDAI) that correlates 93% with CDAI but doesn't require laboratory tests. "
                "It consists of 5 domains: general well-being (0-4), abdominal pain (0-3), number of "
                "liquid stools (1 point each), abdominal mass (0-3), and complications (1 point each). "
                "Scores <5 indicate remission, 5-7 mild disease, 8-16 moderate disease, and >16 severe "
                "disease. A reduction of ≥3 points is considered a clinically significant response. "
                "This tool enables rapid bedside assessment of disease activity for treatment decisions.",
    response_description="The calculated HBI score with disease activity classification and treatment recommendations",
    operation_id="calculate_harvey_bradshaw_index"
)
async def calculate_harvey_bradshaw_index(request: HarveyBradshawIndexRequest):
    """
    Calculates Harvey-Bradshaw Index (HBI) for Crohn's Disease
    
    The HBI provides a simple clinical assessment of Crohn's disease activity
    without requiring laboratory tests, making it ideal for routine monitoring.
    
    Args:
        request: Parameters needed for HBI calculation
        
    Returns:
        HarveyBradshawIndexResponse: Result with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("harvey_bradshaw_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Harvey-Bradshaw Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return HarveyBradshawIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HBI calculation",
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
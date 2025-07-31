"""
Follicular Lymphoma International Prognostic Index (FLIPI) Router

Endpoint for calculating FLIPI score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.flipi import (
    FlipiRequest,
    FlipiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/flipi",
    response_model=FlipiResponse,
    summary="Calculate Follicular Lymphoma International Prognostic Index",
    description="Estimates overall survival in patients with follicular lymphoma based on 5 adverse prognostic factors to stratify patients into risk groups for treatment planning.",
    response_description="The calculated flipi with interpretation",
    operation_id="calculate_flipi"
)
async def calculate_flipi(request: FlipiRequest):
    """
    Calculates Follicular Lymphoma International Prognostic Index (FLIPI)
    
    FLIPI stratifies patients with follicular lymphoma into risk groups based on 
    5 adverse prognostic factors to guide treatment decisions and provide 
    prognostic information.
    
    Args:
        request: Parameters for FLIPI calculation including age, nodal sites, 
                LDH, hemoglobin, and Ann Arbor stage
        
    Returns:
        FlipiResponse: FLIPI score (0-5) with risk stratification and prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("flipi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FLIPI score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FlipiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FLIPI calculation",
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
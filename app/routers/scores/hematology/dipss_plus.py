"""
DIPSS/DIPSS Plus (Dynamic International Prognostic Scoring System) for Myelofibrosis Router

Endpoint for calculating DIPSS/DIPSS Plus score in myelofibrosis patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.dipss_plus import (
    DipssPlusRequest,
    DipssPlusResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dipss_plus",
    response_model=DipssPlusResponse,
    summary="Calculate DIPSS/DIPSS Plus",
    description="Estimates survival in patients with primary myelofibrosis using clinical and laboratory parameters",
    response_description="The calculated dipss plus with interpretation",
    operation_id="calculate_dipss_plus"
)
async def calculate_dipss_plus(request: DipssPlusRequest):
    """
    Calculates DIPSS/DIPSS Plus score for Myelofibrosis
    
    Estimates survival in patients with primary myelofibrosis using clinical 
    and laboratory parameters. DIPSS uses 5 factors while DIPSS Plus adds 
    3 additional factors including karyotype for refined risk stratification.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        DipssPlusResponse: Risk category with median survival and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dipss_plus", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DIPSS/DIPSS Plus score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DipssPlusResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DIPSS/DIPSS Plus score",
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
"""
Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS) Router

Endpoint for calculating EDSS for MS patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.edss import (
    EdssRequest,
    EdssResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/edss",
    response_model=EdssResponse,
    summary="Calculate Expanded Disability Status Scale",
    description="Describes severity of disability in MS patients based on functional systems assessment and ambulatory ability. The most widely used disability scale for multiple sclerosis.",
    response_description="The calculated edss with interpretation",
    operation_id="calculate_edss"
)
async def calculate_edss(request: EdssRequest):
    """
    Calculates Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS)
    
    The EDSS is the most widely used method of quantifying disability in multiple 
    sclerosis patients, ranging from 0 (normal neurological exam) to 10 (death due to MS).
    
    Args:
        request: Functional systems scores and ambulation status
        
    Returns:
        EdssResponse: EDSS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("edss", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EDSS",
                    "details": {"parameters": parameters}
                }
            )
        
        return EdssResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EDSS",
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
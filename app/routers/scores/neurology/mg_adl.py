"""
Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale Router

Endpoint for calculating MG-ADL scale for myasthenia gravis functional assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.mg_adl import (
    MgAdlRequest,
    MgAdlResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mg_adl",
    response_model=MgAdlResponse,
    summary="Calculate MG-ADL Scale",
    description="Calculates the Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale for assessing disease severity and functional status in patients with myasthenia gravis. This validated 8-item patient-reported outcome measure evaluates bulbar functions (talking, chewing, swallowing), respiratory function (breathing), gross motor functions (arm and leg strength), and ocular symptoms (ptosis and diplopia). Each item is scored 0-3, providing a total score of 0-24 points. The scale is based on patient recall of symptoms during the prior week and correlates well with other MG severity measures. A 2-point reduction represents clinically meaningful improvement.",
    response_description="The calculated MG-ADL score with functional impairment severity assessment and comprehensive management recommendations",
    operation_id="mg_adl"
)
async def calculate_mg_adl(request: MgAdlRequest):
    """
    Calculates Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale
    
    Patient-reported outcome measure for assessing functional impairment
    in myasthenia gravis across 8 domains of daily living activities.
    
    Args:
        request: Eight functional assessment parameters scored 0-3
        
    Returns:
        MgAdlResponse: Score with severity classification and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mg_adl", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MG-ADL Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return MgAdlResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MG-ADL Scale",
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
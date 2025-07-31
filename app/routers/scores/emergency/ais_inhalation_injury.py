"""
Abbreviated Injury Score (AIS) for Inhalation Injury Router

Endpoint for calculating AIS for Inhalation Injury.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ais_inhalation_injury import (
    AisInhalationInjuryRequest,
    AisInhalationInjuryResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ais_inhalation_injury",
    response_model=AisInhalationInjuryResponse,
    summary="Calculate Abbreviated Injury Score",
    description="Classifies inhalation injury severity based on bronchoscopic findings in adult patients with suspected inhalation injury undergoing flexible bronchoscopy",
    response_description="The calculated ais inhalation injury with interpretation",
    operation_id="ais_inhalation_injury"
)
async def calculate_ais_inhalation_injury(request: AisInhalationInjuryRequest):
    """
    Calculates Abbreviated Injury Score (AIS) for Inhalation Injury
    
    Classifies inhalation injury severity based on bronchoscopic findings in adult patients 
    with suspected inhalation injury undergoing flexible bronchoscopy. The AIS may predict 
    development of ARDS, length of mechanical ventilation, and prolonged ICU stay.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        AisInhalationInjuryResponse: Result with clinical interpretation
    """
    try:
        parameters = request.dict()
        
        result = calculator_service.calculate_score("ais_inhalation_injury", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AIS for Inhalation Injury",
                    "details": {"parameters": parameters}
                }
            )
        
        return AisInhalationInjuryResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AIS Inhalation Injury",
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
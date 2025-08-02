"""
tPA Contraindications for Ischemic Stroke Router

Endpoint for evaluating tPA eligibility in acute ischemic stroke.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.tpa_contraindications import (
    TpaContraindicationsRequest,
    TpaContraindicationsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/tpa_contraindications",
    response_model=TpaContraindicationsResponse,
    summary="Evaluate tPA Contraindications for Ischemic Stroke",
    description="Evaluates eligibility for IV tPA (alteplase) in acute ischemic stroke patients by "
                "assessing absolute and relative contraindications based on 2019 AHA/ASA guidelines. "
                "The tool checks time window eligibility (standard 0-3 hours, extended 3-4.5 hours), "
                "absolute contraindications that represent unacceptable bleeding risk, and relative "
                "contraindications that require careful risk-benefit analysis. IV tPA remains the "
                "standard thrombolytic therapy for eligible patients, with potential to significantly "
                "improve functional outcomes when administered within the appropriate time window.",
    response_description="The eligibility assessment with detailed contraindications and clinical recommendations",
    operation_id="tpa_contraindications"
)
async def calculate_tpa_contraindications(request: TpaContraindicationsRequest):
    """
    Evaluates tPA eligibility for acute ischemic stroke
    
    This tool systematically reviews contraindications to IV tPA based on
    current AHA/ASA guidelines, helping clinicians make time-sensitive
    treatment decisions while minimizing bleeding risk.
    
    Args:
        request: Clinical parameters for contraindication assessment
        
    Returns:
        TpaContraindicationsResponse: Eligibility status with specific contraindications
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("tpa_contraindications", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating tPA contraindications",
                    "details": {"parameters": parameters}
                }
            )
        
        return TpaContraindicationsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for tPA contraindications assessment",
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
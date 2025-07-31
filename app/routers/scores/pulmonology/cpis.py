"""
Clinical Pulmonary Infection Score (CPIS) Router

Endpoint for calculating CPIS for Ventilator-Associated Pneumonia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.cpis import (
    CpisRequest,
    CpisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cpis",
    response_model=CpisResponse,
    summary="Calculate Clinical Pulmonary Infection Score",
    description="Evaluates objective data in mechanically ventilated patients suspected of ventilator-associated pneumonia (VAP) and stratifies risk of positive diagnosis. The score assists clinicians in determining when to pursue pulmonary cultures and guides antibiotic management decisions.",
    response_description="The calculated cpis with interpretation",
    operation_id="calculate_cpis"
)
async def calculate_cpis(request: CpisRequest):
    """
    Calculates Clinical Pulmonary Infection Score (CPIS)
    
    Evaluates objective data in mechanically ventilated patients suspected of 
    ventilator-associated pneumonia (VAP) and stratifies risk of positive diagnosis.
    The score assists in determining when to pursue pulmonary cultures and guides 
    antibiotic management decisions.
    
    Args:
        request: Parameters including temperature, WBC count, secretions, 
                oxygenation, chest X-ray findings, and culture results
        
    Returns:
        CpisResponse: CPIS score (0-12) with VAP likelihood and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cpis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CPIS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CpisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CPIS score",
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
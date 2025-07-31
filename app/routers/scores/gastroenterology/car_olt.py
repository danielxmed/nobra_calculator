"""
Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT) Router

Endpoint for calculating CAR-OLT score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.car_olt import (
    CarOltRequest,
    CarOltResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/car_olt",
    response_model=CarOltResponse,
    summary="Calculate Cardiovascular Risk in Orthotopic Liver Transpl...",
    description="Predicts cardiovascular risk in orthotopic liver transplantation. The CAR-OLT score predicts the 1-year risk for death or hospitalization related to a major CVD event (myocardial infarction, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation.",
    response_description="The calculated car olt with interpretation",
    operation_id="calculate_car_olt"
)
async def calculate_car_olt(request: CarOltRequest):
    """
    Calculates Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT)
    
    Predicts 1-year risk of death or hospitalization related to major cardiovascular 
    events (MI, cardiac revascularization, heart failure, atrial fibrillation, 
    cardiac arrest, pulmonary embolism, or stroke) after liver transplantation.
    
    Args:
        request: Parameters needed for calculation including demographics, 
                socioeconomic factors, and medical conditions
        
    Returns:
        CarOltResponse: Result with risk score and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("car_olt", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAR-OLT score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CarOltResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAR-OLT score",
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
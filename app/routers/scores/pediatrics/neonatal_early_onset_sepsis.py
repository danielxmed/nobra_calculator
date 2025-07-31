"""
Neonatal Early-Onset Sepsis Calculator Router

Endpoint for calculating Neonatal Early-Onset Sepsis risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.neonatal_early_onset_sepsis import (
    NeonatalEarlyOnsetSepsisRequest,
    NeonatalEarlyOnsetSepsisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/neonatal_early_onset_sepsis",
    response_model=NeonatalEarlyOnsetSepsisResponse,
    summary="Calculate Neonatal Early-Onset Sepsis Calculator",
    description="Calculates risk of early-onset neonatal sepsis based on maternal intrapartum risk factors for newborns ≥34 weeks gestation. Uses multivariate predictive model to estimate probability of culture-positive sepsis within 72 hours of birth.",
    response_description="The calculated neonatal early onset sepsis with interpretation",
    operation_id="calculate_neonatal_early_onset_sepsis"
)
async def calculate_neonatal_early_onset_sepsis(request: NeonatalEarlyOnsetSepsisRequest):
    """
    Calculates Neonatal Early-Onset Sepsis risk
    
    Estimates the probability of culture-positive sepsis within 72 hours of birth
    in newborns ≥34 weeks gestation based on maternal intrapartum risk factors.
    Uses a multivariate predictive model to guide antibiotic management decisions.
    
    Args:
        request: Parameters needed for calculation including gestational age,
                maternal temperature, ROM duration, GBS status, and antibiotics
        
    Returns:
        NeonatalEarlyOnsetSepsisResponse: Result with risk interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("neonatal_early_onset_sepsis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Neonatal Early-Onset Sepsis risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return NeonatalEarlyOnsetSepsisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Neonatal Early-Onset Sepsis Calculator",
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
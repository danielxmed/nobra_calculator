"""
Bicarbonate Deficit Calculator Router

Endpoint for calculating bicarbonate deficit in metabolic acidosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.bicarbonate_deficit import (
    BicarbonateDeficitRequest,
    BicarbonateDeficitResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bicarbonate_deficit",
    response_model=BicarbonateDeficitResponse,
    summary="Calculate Bicarbonate Deficit",
    description="Calculates total body bicarbonate deficit for assessment of metabolic acidosis severity and bicarbonate replacement therapy planning.",
    response_description="The calculated bicarbonate deficit with interpretation",
    operation_id="calculate_bicarbonate_deficit"
)
async def calculate_bicarbonate_deficit(request: BicarbonateDeficitRequest):
    """
    Calculates Bicarbonate Deficit for metabolic acidosis assessment
    
    The Bicarbonate Deficit calculator estimates total body bicarbonate deficit using 
    the standard formula: **Deficit = 0.4 × Weight (kg) × (Target HCO3 - Current HCO3)**
    
    **Clinical Applications:**
    - Assessment of metabolic acidosis severity
    - Planning bicarbonate replacement therapy
    - Monitoring response to treatment
    
    **Normal Values:**
    - Bicarbonate range: 23-28 mEq/L
    - Default target level: 24 mEq/L
    
    **Severity Classification:**
    - Normal: ≥23 mEq/L
    - Mild acidosis: 18-22 mEq/L
    - Moderate acidosis: 15-17 mEq/L  
    - Severe acidosis: <15 mEq/L
    
    **Clinical Pearls:**
    - Consider bicarbonate replacement primarily for severe acidosis (HCO3 <15 mEq/L)
    - Give 50% of calculated deficit initially, then reassess
    - Always treat underlying cause of acidosis
    - Avoid overly rapid correction (complications: paradoxical CNS acidosis, hypokalemia)
    - Monitor with serial arterial blood gases
    
    Args:
        request: Parameters including weight, current bicarbonate level, and optional target level
        
    Returns:
        BicarbonateDeficitResponse: Calculated deficit with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict(exclude_none=True)
        
        # Execute calculation
        result = calculator_service.calculate_score("bicarbonate_deficit", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bicarbonate Deficit",
                    "details": {"parameters": parameters}
                }
            )
        
        return BicarbonateDeficitResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bicarbonate Deficit calculation",
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
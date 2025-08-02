"""
Ideal Body Weight and Adjusted Body Weight Router

Endpoint for calculating Ideal Body Weight and Adjusted Body Weight using Devine formula.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.ideal_body_weight_adjusted import (
    IdealBodyWeightAdjustedRequest,
    IdealBodyWeightAdjustedResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ideal_body_weight_adjusted",
    response_model=IdealBodyWeightAdjustedResponse,
    summary="Calculate Ideal Body Weight and Adjusted Body Weight",
    description="Calculates ideal body weight using the validated Devine formula and adjusted body weight "
                "for clinical applications, particularly medication dosing and physiological calculations. "
                "The Devine formula (1974) is the most widely used method for ideal body weight calculation "
                "in clinical practice. For men: IBW = 50 kg + 2.3 kg × (height in inches - 60). "
                "For women: IBW = 45.5 kg + 2.3 kg × (height in inches - 60). When actual weight is provided, "
                "the calculator also determines adjusted body weight using the formula: "
                "AdjBW = IBW + 0.4 × (Actual Weight - IBW). This is particularly useful for medication dosing "
                "in overweight or obese patients. The calculator is widely used for drug dosing decisions, "
                "mechanical ventilation tidal volume calculations (6-8 mL/kg IBW), nutritional assessments, "
                "and clinical research. Hydrophilic medications typically use ideal body weight while "
                "lipophilic medications may use adjusted body weight. The formula is most accurate for "
                "heights ≥60 inches; for shorter patients, consider subtracting 2-5 lbs per inch below 60 inches.",
    response_description="The calculated ideal body weight and adjusted body weight with clinical dosing recommendations",
    operation_id="ideal_body_weight_adjusted"
)
async def calculate_ideal_body_weight_adjusted(request: IdealBodyWeightAdjustedRequest):
    """
    Calculates Ideal Body Weight and Adjusted Body Weight
    
    Calculates ideal body weight using the Devine formula and adjusted body weight 
    for clinical use in medication dosing and physiological calculations.
    
    Args:
        request: Patient demographics including sex, height, and optional actual weight
        
    Returns:
        IdealBodyWeightAdjustedResponse: Calculated weights with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ideal_body_weight_adjusted", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ideal Body Weight and Adjusted Body Weight",
                    "details": {"parameters": parameters}
                }
            )
        
        return IdealBodyWeightAdjustedResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ideal Body Weight calculation",
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
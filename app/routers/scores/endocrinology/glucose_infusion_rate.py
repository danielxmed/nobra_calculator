"""
Glucose Infusion Rate (GIR) Router

Endpoint for calculating Glucose Infusion Rate.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.glucose_infusion_rate import (
    GlucoseInfusionRateRequest,
    GlucoseInfusionRateResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glucose_infusion_rate",
    response_model=GlucoseInfusionRateResponse,
    summary="Calculate Glucose Infusion Rate (GIR)",
    description="Calculates the rate at which glucose is administered intravenously, particularly important in neonatal and pediatric care to maintain appropriate blood glucose levels. Used to monitor and adjust dextrose infusions to prevent hypoglycemia while avoiding excessive glucose administration.",
    response_description="The calculated glucose infusion rate with interpretation",
    operation_id="calculate_glucose_infusion_rate"
)
async def calculate_glucose_infusion_rate(request: GlucoseInfusionRateRequest):
    """
    Calculates Glucose Infusion Rate (GIR)
    
    The Glucose Infusion Rate (GIR) is a critical calculation in neonatal and pediatric 
    care that quantifies the rate at which glucose is administered intravenously. This 
    measurement is essential for maintaining appropriate blood glucose levels, preventing 
    hypoglycemia, and optimizing nutritional support in vulnerable pediatric populations.
    
    The GIR calculation uses the standard formula:
    GIR (mg/kg/min) = [Infusion rate (mL/hr) × Dextrose concentration (%) × 10] / [Weight (kg) × 60]
    
    Key Clinical Applications:
    - Neonatal intensive care glucose management
    - Pediatric parenteral nutrition protocols
    - Prevention of neonatal hypoglycemia
    - Guidance for insulin therapy decisions
    - Monitoring and adjustment of IV dextrose therapy
    
    Clinical Ranges:
    - Normal/Physiologic: 4-8 mg/kg/min (baseline glucose needs)
    - Therapeutic: 8-12 mg/kg/min (enhanced delivery for growth)
    - High Therapeutic: 12-18 mg/kg/min (full parenteral nutrition)
    - Excessive: >18 mg/kg/min (risk of metabolic complications)
    
    Args:
        request: Parameters including infusion rate, dextrose concentration, and patient weight
        
    Returns:
        GlucoseInfusionRateResponse: Calculated GIR with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glucose_infusion_rate", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glucose Infusion Rate",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlucoseInfusionRateResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glucose Infusion Rate",
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
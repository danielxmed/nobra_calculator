"""
BeAM Value Router

Endpoint for calculating BeAM Value to guide prandial insulin therapy decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.beam_value import (
    BeamValueRequest,
    BeamValueResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/beam_value",
    response_model=BeamValueResponse,
    summary="Calculate BeAM Value",
    description="Calculates the difference between bedtime and morning fasting blood glucose to guide prandial insulin therapy decisions in patients with type 2 diabetes",
    response_description="The calculated beam value with interpretation",
    operation_id="beam_value"
)
async def calculate_beam_value(request: BeamValueRequest):
    """
    Calculates BeAM Value (Bedtime-Morning Glucose Difference)
    
    The BeAM value is a simple calculation that helps guide diabetes management decisions,
    particularly regarding insulin therapy in patients with type 2 diabetes.
    
    **How it works:**
    - BeAM Value = Bedtime glucose - Morning fasting glucose
    - Simple SMBG (self-monitoring blood glucose) measurements
    - Requires consistent timing of measurements
    
    **Clinical Interpretation:**
    - **High BeAM (≥30 mg/dL)**: Indicates postprandial glucose excursions and need for 
      prandial insulin supplementation rather than advancing basal insulin dose
    - **Medium/Low BeAM (0-29 mg/dL)**: Prandial insulin supplementation may be of little 
      benefit; focus on basal insulin optimization
    - **Negative BeAM (<0 mg/dL)**: Morning glucose higher than bedtime glucose; 
      contraindication for prandial insulin intensification; suggests dawn phenomenon
    
    **Clinical Significance:**
    - Helps identify patients with T2DM using basal insulin who need targeting of 
      postprandial control rather than advancing basal insulin dose
    - High BeAM indicates well-controlled fasting glucose but postprandial excursions
    - Negative BeAM suggests inadequate basal insulin coverage or dawn phenomenon
    
    **Research Background:**
    The BeAM value was developed to help clinicians decide when patients with type 2 diabetes
    on basal insulin therapy might benefit from adding prandial (mealtime) insulin rather 
    than continuing to increase their basal insulin dose. Studies show that patients with 
    large BeAM values have less time in range and higher HbA1c levels.
    
    Args:
        request: BeAM Value calculation parameters (bedtime and morning glucose)
        
    Returns:
        BeamValueResponse: BeAM value with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("beam_value", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BeAM Value",
                    "details": {"parameters": parameters}
                }
            )
        
        return BeamValueResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BeAM Value calculation",
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
"""
2023 Emergency Medicine Coding Guide Router

Endpoint for calculating 2023 Emergency Medicine Coding Guide.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.emergency_medicine_coding_guide_2023 import (
    EmergencyMedicineCodingGuide2023Request,
    EmergencyMedicineCodingGuide2023Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/emergency_medicine_coding_guide_2023",
    response_model=EmergencyMedicineCodingGuide2023Response,
    summary="Calculate 2023 Emergency Medicine Coding Guide",
    description="Rates the level of service required in emergency medicine based on 2023 AMA CPT Evaluation and Management (E/M) coding changes. Determines appropriate emergency department service level (99281-99285) based on medical decision making components.",
    response_description="The calculated emergency medicine coding guide 2023 with interpretation",
    operation_id="calculate_emergency_medicine_coding_guide_2023"
)
async def calculate_emergency_medicine_coding_guide_2023(request: EmergencyMedicineCodingGuide2023Request):
    """
    Calculates 2023 Emergency Medicine Coding Guide
    
    Rates the level of service required in emergency medicine based on 2023 AMA CPT 
    Evaluation and Management (E/M) coding changes. Determines appropriate emergency 
    department service level (99281-99285) based on medical decision making components:
    number/complexity of problems, amount/complexity of data, and risk level.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        EmergencyMedicineCodingGuide2023Response: Result with ED service level and CPT code
    """
    try:
        parameters = request.dict()
        
        result = calculator_service.calculate_score("emergency_medicine_coding_guide_2023", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 2023 Emergency Medicine Coding Guide",
                    "details": {"parameters": parameters}
                }
            )
        
        return EmergencyMedicineCodingGuide2023Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 2023 Emergency Medicine Coding Guide",
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
"""
Intraoperative Fluid Dosing in Adult Patients Router

Endpoint for calculating intraoperative fluid requirements during surgery.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.intraoperative_fluid_dosing import (
    IntraoperativeFluidDosingRequest,
    IntraoperativeFluidDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/intraoperative_fluid_dosing",
    response_model=IntraoperativeFluidDosingResponse,
    summary="Calculate Intraoperative Fluid Dosing",
    description="Calculates intraoperative IV fluid requirements for adult patients during surgery, providing hourly fluid requirement, fluid deficit replacement, and hour-by-hour fluid requirements based on surgical trauma severity. This evidence-based calculator uses patient weight, NPO (nothing by mouth) time, and surgical trauma classification to guide perioperative fluid management and optimize patient outcomes. The tool provides structured fluid dosing with initial NPO deficit replacement (distributed over first 3 hours), continuous maintenance fluid requirements, and additional surgical trauma-related losses. Essential for anesthesiologists, surgeons, and perioperative teams managing fluid balance during surgical procedures. Not recommended for patients with fluid overload risks such as heart failure, COPD, or kidney failure.",
    response_description="Structured intraoperative fluid dosing plan with hourly requirements, deficit replacement schedule, and surgical trauma considerations",
    operation_id="intraoperative_fluid_dosing"
)
async def calculate_intraoperative_fluid_dosing(request: IntraoperativeFluidDosingRequest):
    """
    Calculates Intraoperative Fluid Dosing for Adult Patients
    
    Provides evidence-based fluid management plan for adult surgical patients based on 
    weight, NPO time, and surgical trauma severity.
    
    Args:
        request: Patient and surgical parameters for fluid dosing calculation
        
    Returns:
        IntraoperativeFluidDosingResponse: Structured fluid plan with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("intraoperative_fluid_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Intraoperative Fluid Dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return IntraoperativeFluidDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Intraoperative Fluid Dosing",
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
                "message": "Internal error in fluid dosing calculation",
                "details": {"error": str(e)}
            }
        )
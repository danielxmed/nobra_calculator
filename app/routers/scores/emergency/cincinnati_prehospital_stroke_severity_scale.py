"""
Cincinnati Prehospital Stroke Severity Scale (CP-SSS) Router

Endpoint for calculating Cincinnati Prehospital Stroke Severity Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.cincinnati_prehospital_stroke_severity_scale import (
    CincinnatiPrehospitalStrokeSeverityScaleRequest,
    CincinnatiPrehospitalStrokeSeverityScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cincinnati_prehospital_stroke_severity_scale",
    response_model=CincinnatiPrehospitalStrokeSeverityScaleResponse,
    summary="Calculate Cincinnati Prehospital Stroke Severity Scale",
    description="Predicts large vessel occlusion (LVO) and severe stroke in patients with stroke symptoms",
    response_description="The calculated cincinnati prehospital stroke severity scale with interpretation",
    operation_id="cincinnati_prehospital_stroke_severity_scale"
)
async def calculate_cincinnati_prehospital_stroke_severity_scale(request: CincinnatiPrehospitalStrokeSeverityScaleRequest):
    """
    Calculates Cincinnati Prehospital Stroke Severity Scale (CP-SSS)
    
    The Cincinnati Prehospital Stroke Severity Scale is a validated tool designed 
    to predict large vessel occlusion (LVO) and severe stroke in patients presenting 
    with acute stroke symptoms. This scale was specifically developed for use by 
    emergency medical services personnel to enhance prehospital stroke triage and 
    guide transport decisions to appropriate stroke care facilities.
    
    Args:
        request: CP-SSS parameters for stroke severity assessment
        
    Returns:
        CincinnatiPrehospitalStrokeSeverityScaleResponse: Score with risk stratification and transport recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cincinnati_prehospital_stroke_severity_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cincinnati Prehospital Stroke Severity Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return CincinnatiPrehospitalStrokeSeverityScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cincinnati Prehospital Stroke Severity Scale",
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
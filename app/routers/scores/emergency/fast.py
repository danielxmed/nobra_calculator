"""
Focused Assessment with Sonography for Trauma (FAST) Router

Endpoint for calculating FAST examination results.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.fast import (
    FastRequest,
    FastResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fast",
    response_model=FastResponse,
    summary="Calculate Focused Assessment with Sonography for Trauma",
    description="Predicts presence of pericardial or intra-abdominal injury after penetrating or blunt trauma based on ultrasound findings.",
    response_description="The calculated fast with interpretation",
    operation_id="calculate_fast"
)
async def calculate_fast(request: FastRequest):
    """
    Evaluates FAST examination findings
    
    The Focused Assessment with Sonography for Trauma (FAST) is a rapid 
    bedside ultrasound examination performed to identify free fluid (blood) 
    in the peritoneal, pericardial, and pleural spaces in trauma patients.
    
    FAST evaluates four anatomical windows:
    - Pericardial view
    - Right upper quadrant (Morison's pouch)
    - Left upper quadrant (splenorenal recess)
    - Suprapubic/pelvic view
    
    Management depends on findings and patient stability:
    - Pericardial fluid → immediate surgical intervention
    - Abdominal fluid + unstable → emergent laparotomy
    - Abdominal fluid + stable → CT scan for further evaluation
    
    Args:
        request: FAST examination findings and patient stability
        
    Returns:
        FastResponse: FAST result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fast", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating FAST examination",
                    "details": {"parameters": parameters}
                }
            )
        
        return FastResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FAST evaluation",
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
                "message": "Internal error in FAST evaluation",
                "details": {"error": str(e)}
            }
        )
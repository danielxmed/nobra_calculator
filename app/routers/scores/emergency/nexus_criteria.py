"""
NEXUS Criteria for C-Spine Imaging Router

Endpoint for calculating NEXUS Criteria for C-Spine Imaging.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.nexus_criteria import (
    NexusCriteriaRequest,
    NexusCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nexus_criteria",
    response_model=NexusCriteriaResponse,
    summary="Calculate NEXUS Criteria for C-Spine Imaging",
    description="Clinically clears cervical spine fracture without imaging in alert, stable trauma patients. The NEXUS (National Emergency X-Radiography Utilization Study) criteria help determine which blunt trauma patients do not require cervical spine imaging.",
    response_description="The calculated nexus criteria with interpretation",
    operation_id="calculate_nexus_criteria"
)
async def calculate_nexus_criteria(request: NexusCriteriaRequest):
    """
    Calculates NEXUS Criteria for C-Spine Imaging
    
    The NEXUS (National Emergency X-Radiography Utilization Study) criteria are used to 
    determine which blunt trauma patients do not require cervical spine imaging. The 
    criteria help reduce unnecessary radiation exposure while maintaining high sensitivity 
    (99.6%) for detecting clinically significant cervical spine injuries.
    
    All five criteria must be met for low risk classification:
    1. No midline cervical spine tenderness
    2. No focal neurologic deficit
    3. Normal alertness/level of consciousness  
    4. No evidence of intoxication
    5. No painful distracting injury
    
    Performance characteristics:
    - Sensitivity: 99.6% (95% CI: 98.6-100%)
    - Specificity: 12.9%
    - Validated in over 34,000 patients
    
    Important limitations:
    - Less reliable in patients >65 years of age
    - Use caution in pediatric patients (<18 years)
    - Validated in blunt trauma patients only
    
    Args:
        request: Parameters needed for NEXUS criteria assessment
        
    Returns:
        NexusCriteriaResponse: Risk assessment with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nexus_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NEXUS Criteria for C-Spine Imaging",
                    "details": {"parameters": parameters}
                }
            )
        
        return NexusCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NEXUS Criteria for C-Spine Imaging",
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
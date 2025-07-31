"""
CEDOCS Score for Emergency Department Overcrowding Router

Endpoint for calculating CEDOCS Score for ED overcrowding assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.cedocs_score import (
    CedocsScoreRequest,
    CedocsScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cedocs_score",
    response_model=CedocsScoreResponse,
    summary="Calculate CEDOCS Score for Emergency Department Overcrowding",
    description="Community Emergency Department Overcrowding Scale (CEDOCS) estimates the severity of overcrowding in community emergency departments. Provides objective quantification for resource allocation, patient flow management, and real-time assessment of ED crowding levels across varying patient volumes.",
    response_description="The calculated cedocs score with interpretation",
    operation_id="cedocs_score"
)
async def calculate_cedocs_score(request: CedocsScoreRequest):
    """
    Calculates CEDOCS Score for Emergency Department Overcrowding
    
    The Community Emergency Department Overcrowding Scale (CEDOCS) estimates the 
    severity of overcrowding in community emergency departments. This validated tool 
    provides objective quantification for resource allocation, patient flow management, 
    and real-time assessment of ED crowding levels.
    
    The CEDOCS formula incorporates 6 key parameters:
    
    CORE ED STATUS PARAMETERS:
    - Critical care patients: Number requiring ICU-level interventions
    - Longest wait time: Boarding time of longest admitted patient (minutes)
    - Waiting room patients: Census of patients awaiting assessment
    - Total ED patients: Complete departmental census
    - ED beds: Licensed bed capacity
    
    VOLUME CONTEXT:
    - Annual ED visits: Used for volume-based score adjustments
    - Scaling factor: Optional institutional calibration (default 2.0)
    
    OVERCROWDING LEVELS:
    - Level 1 (1-20): Not busy - Normal operations
    - Level 2 (21-60): Busy - Monitor patient flow  
    - Level 3 (61-100): Extremely busy but not overcrowded
    - Level 4 (101-140): Overcrowded - Implement protocols
    - Level 5 (141-180): Severely overcrowded - Emergency measures
    - Level 6 (181-200): Dangerously overcrowded - Crisis intervention
    
    Clinical Applications:
    - **Resource Allocation**: Objective basis for staffing and resource decisions
    - **Quality Improvement**: Standardized overcrowding measurement across institutions
    - **Operational Management**: Real-time decision support for diversion protocols
    - **Research Tool**: Validated instrument for studying ED operations
    
    Validation Features:
    - Developed specifically for community EDs with varying patient volumes
    - More broadly applicable than NEDOCS (designed for academic centers)
    - Validated across EDs with annual volumes ≥18,000 patients
    - Uses complex cubic spline adjustments for different volume ranges
    - Overcrowding threshold defined as score > 100
    
    The formula includes sophisticated volume-based adjustments using cubic splines
    to account for different ED sizes, patient complexity, and operational patterns.
    
    Args:
        request: Parameters needed for CEDOCS Score calculation
        
    Returns:
        CedocsScoreResponse: Score with overcrowding level and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cedocs_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CEDOCS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CedocsScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CEDOCS Score",
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
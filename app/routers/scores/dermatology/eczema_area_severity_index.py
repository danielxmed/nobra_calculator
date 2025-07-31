"""
Eczema Area and Severity Index (EASI) Router

Endpoint for calculating EASI score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.dermatology.eczema_area_severity_index import (
    EczemaAreaSeverityIndexRequest,
    EczemaAreaSeverityIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/eczema_area_severity_index",
    response_model=EczemaAreaSeverityIndexResponse,
    summary="Calculate Eczema Area and Severity Index (EASI)",
    description="Stratifies eczema severity by assessing area involvement and severity signs across four body regions (head/neck, upper extremities, trunk, lower extremities) with validated clinical scoring.",
    response_description="The calculated eczema area severity index with interpretation",
    operation_id="calculate_eczema_area_severity_index"
)
async def calculate_eczema_area_severity_index(request: EczemaAreaSeverityIndexRequest):
    """
    Calculates Eczema Area and Severity Index (EASI)
    
    The EASI is the most validated and widely used assessment tool for atopic dermatitis 
    severity in clinical practice and research. It evaluates eczema severity across four 
    body regions (head/neck, upper extremities, trunk, lower extremities) by assessing 
    both area involvement (0-6 scale) and four severity signs (0-3 scale each): erythema, 
    edema/papulation, excoriation, and lichenification.
    
    Key Clinical Features:
    - Total score range: 0-72 points
    - Assessment time: ~6 minutes by trained investigator
    - Validated severity categories with treatment recommendations
    - Substantial inter-rater reliability (κ = 0.75)
    - Correlates with patient-reported outcomes (pruritus, sleep, QoL)
    - Recommended primary endpoint for clinical trials
    
    Age-Based Regional Multipliers:
    - Children (0-7 years): Head/neck=0.2, Upper extremities=0.2, Trunk=0.3, Lower extremities=0.4
    - Adults (8+ years): Head/neck=0.1, Upper extremities=0.2, Trunk=0.3, Lower extremities=0.4
    
    Assessment Considerations:
    - Perform in good lighting for accurate erythema assessment
    - Consider skin pigmentation when grading erythema (may need higher score in darker skin)
    - Complete independently of previous assessments (static tool)
    - Does not assess dryness/scaling (limitation of tool)
    
    Args:
        request: Parameters for all body regions including area involvement and severity signs
        
    Returns:
        EczemaAreaSeverityIndexResponse: EASI score with severity category and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("eczema_area_severity_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Eczema Area and Severity Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return EczemaAreaSeverityIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Eczema Area and Severity Index",
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
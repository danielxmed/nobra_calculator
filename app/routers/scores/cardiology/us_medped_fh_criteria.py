"""
US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia (FH) Router

Endpoint for calculating US MEDPED diagnostic criteria for familial hypercholesterolemia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.us_medped_fh_criteria import (
    UsMedpedFhCriteriaRequest,
    UsMedpedFhCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/us_medped_fh_criteria",
    response_model=UsMedpedFhCriteriaResponse,
    summary="Calculate US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia",
    description="Applies the US MEDPED (Make Early Diagnosis to Prevent Early Death) diagnostic criteria for "
                "familial hypercholesterolemia. This simplified diagnostic tool uses only age-specific total "
                "cholesterol cutoffs that vary based on family history of FH. The MEDPED criteria were designed "
                "for population screening and early diagnosis to prevent premature cardiovascular death. Unlike "
                "more complex scoring systems, MEDPED uses only cholesterol levels and family history, making it "
                "practical for clinical use. Positive diagnosis indicates need for genetic testing, family screening, "
                "and intensive lipid-lowering therapy. The criteria have high specificity but may be less sensitive "
                "than Dutch Lipid Clinic Network criteria.",
    response_description="Diagnostic result (Positive/Negative) with clinical interpretation, specific cholesterol cutoff used, and treatment recommendations",
    operation_id="us_medped_fh_criteria"
)
async def calculate_us_medped_fh_criteria(request: UsMedpedFhCriteriaRequest):
    """
    Calculates US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia
    
    Applies age-specific total cholesterol cutoffs that vary based on family history 
    to diagnose familial hypercholesterolemia using the simplified MEDPED criteria.
    
    Args:
        request: Patient age, total cholesterol level, and family history of FH
        
    Returns:
        UsMedpedFhCriteriaResponse: Diagnostic result with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("us_medped_fh_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating US MEDPED FH criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return UsMedpedFhCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for US MEDPED FH criteria",
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
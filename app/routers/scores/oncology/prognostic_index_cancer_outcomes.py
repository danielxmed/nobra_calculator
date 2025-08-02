"""
Prognostic Index for Cancer Outcomes Router

Endpoint for calculating Prognostic Index for Cancer Outcomes.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.prognostic_index_cancer_outcomes import (
    PrognosticIndexCancerOutcomesRequest,
    PrognosticIndexCancerOutcomesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/prognostic_index_cancer_outcomes",
    response_model=PrognosticIndexCancerOutcomesResponse,
    summary="Calculate Prognostic Index for Cancer Outcomes",
    description="Calculates the Prognostic Index for Cancer Outcomes, a validated tool that predicts "
                "cancer mortality using two readily available serum biomarkers: C-reactive protein (CRP) "
                "and white blood cell (WBC) count. This simple yet effective scoring system provides "
                "essential prognostic information across multiple cancer types by assessing systemic "
                "inflammatory burden. The index helps clinicians stratify patients into distinct risk "
                "groups (low, intermediate, high) based on inflammatory markers, supporting clinical "
                "decision-making, treatment planning, and prognostic discussions. Higher scores indicate "
                "greater inflammatory burden and are associated with worse outcomes, while lower scores "
                "suggest better prognosis and treatment tolerance. This tool is particularly valuable "
                "for its simplicity, using only two standard laboratory values that are routinely "
                "available in clinical practice.",
    response_description="The calculated Prognostic Index with detailed risk stratification and clinical management guidance",
    operation_id="prognostic_index_cancer_outcomes"
)
async def calculate_prognostic_index_cancer_outcomes(request: PrognosticIndexCancerOutcomesRequest):
    """
    Calculates Prognostic Index for Cancer Outcomes
    
    This validated tool helps predict cancer mortality and stratify patients
    based on inflammatory markers (CRP and WBC count).
    
    Args:
        request: CRP and WBC count categories for calculation
        
    Returns:
        PrognosticIndexCancerOutcomesResponse: Result with prognostic stratification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("prognostic_index_cancer_outcomes", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Prognostic Index for Cancer Outcomes",
                    "details": {"parameters": parameters}
                }
            )
        
        return PrognosticIndexCancerOutcomesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Prognostic Index for Cancer Outcomes",
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
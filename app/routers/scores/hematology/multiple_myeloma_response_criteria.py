"""
Multiple Myeloma Response Criteria (IMWG) Router

Endpoint for evaluating treatment response in multiple myeloma patients according to
International Myeloma Working Group (IMWG) criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.multiple_myeloma_response_criteria import (
    MultipleMyelomaResponseCriteriaRequest,
    MultipleMyelomaResponseCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/multiple_myeloma_response_criteria",
    response_model=MultipleMyelomaResponseCriteriaResponse,
    summary="Evaluate Multiple Myeloma Response Criteria (IMWG)",
    description="Evaluates treatment response in multiple myeloma according to International Myeloma Working Group "
                "(IMWG) consensus criteria. This standardized assessment tool categorizes patient response into six "
                "levels: Stringent Complete Response (sCR), Complete Response (CR), Very Good Partial Response (VGPR), "
                "Partial Response (PR), Stable Disease (SD), and Progressive Disease (PD). The criteria use laboratory "
                "parameters including immunofixation results, bone marrow plasma cell percentage, M protein levels, "
                "free light chain ratios, and plasmacytoma status to provide uniform response evaluation across "
                "clinical trials and treatment settings. This tool is essential for treatment monitoring, clinical "
                "decision-making, and prognostic assessment in multiple myeloma management.",
    response_description="IMWG response category with detailed clinical interpretation and management recommendations",
    operation_id="multiple_myeloma_response_criteria"
)
async def calculate_multiple_myeloma_response_criteria(request: MultipleMyelomaResponseCriteriaRequest):
    """
    Evaluates Multiple Myeloma Response Criteria (IMWG)
    
    The International Myeloma Working Group (IMWG) response criteria provide standardized
    assessment of treatment response in multiple myeloma, enabling uniform evaluation
    across clinical trials and treatment settings worldwide.
    
    Args:
        request: Clinical and laboratory parameters including immunofixation results,
                bone marrow findings, M protein levels, and other response indicators
        
    Returns:
        MultipleMyelomaResponseCriteriaResponse: Response category with clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("multiple_myeloma_response_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating Multiple Myeloma Response Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return MultipleMyelomaResponseCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Multiple Myeloma Response Criteria",
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
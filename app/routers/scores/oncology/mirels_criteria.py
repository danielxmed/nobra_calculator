"""
Mirels' Criteria for Prophylactic Fixation Router

Endpoint for calculating Mirels' Criteria pathologic fracture risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.mirels_criteria import (
    MirelsCriteriaRequest,
    MirelsCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mirels_criteria",
    response_model=MirelsCriteriaResponse,
    summary="Calculate Mirels' Criteria for Prophylactic Fixation",
    description="Predicts risk of pathologic fracture in patients with long bone metastases to guide prophylactic "
                "fixation decisions. The Mirels score evaluates four parameters: site of lesion, size of lesion, "
                "nature of lesion (radiographic appearance), and pain level. Scores range from 4-12 points, with "
                "≤7 indicating low risk (0-4% fracture risk) suitable for radiation alone, 8 indicating intermediate "
                "risk (15% fracture risk) requiring clinical judgment, and ≥9 indicating high risk (>33% fracture risk) "
                "warranting prophylactic fixation prior to radiation. This validated tool helps prevent pathologic "
                "fractures and maintains patient function while optimizing treatment timing.",
    response_description="Mirels score with fracture risk stratification and prophylactic fixation recommendations",
    operation_id="mirels_criteria"
)
async def calculate_mirels_criteria(request: MirelsCriteriaRequest):
    """
    Calculates Mirels' Criteria for Prophylactic Fixation
    
    Assesses pathologic fracture risk in patients with long bone metastases
    to determine need for prophylactic surgical fixation prior to radiation.
    
    Args:
        request: Lesion characteristics and clinical parameters
        
    Returns:
        MirelsCriteriaResponse: Risk score with fixation recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mirels_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mirels' Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return MirelsCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mirels' Criteria",
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
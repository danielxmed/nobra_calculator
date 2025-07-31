"""
ASAS Criteria for Axial Spondyloarthritis (SpA) Router

Endpoint for calculating ASAS classification criteria for axial spondyloarthritis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.asas_axial_spa_criteria import (
    AsasAxialSpaCriteriaRequest,
    AsasAxialSpaCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/asas_axial_spa_criteria",
    response_model=AsasAxialSpaCriteriaResponse,
    summary="Calculate ASAS Criteria for Axial Spondyloarthritis (SpA)",
    description="Classifies axial spondyloarthritis according to Assessment of Spondyloarthritis International Society (ASAS) criteria. This classification system allows for early diagnosis of axial SpA by incorporating both clinical and imaging features.",
    response_description="The calculated asas axial spa criteria with interpretation",
    operation_id="calculate_asas_axial_spa_criteria"
)
async def calculate_asas_axial_spa_criteria(request: AsasAxialSpaCriteriaRequest):
    """
    Calculates ASAS Criteria for Axial Spondyloarthritis (SpA)
    
    Classifies axial spondyloarthritis according to Assessment of Spondyloarthritis 
    International Society (ASAS) criteria. This classification system allows for early 
    diagnosis of axial SpA by incorporating both clinical and imaging features.
    
    Entry criterion: Back pain ≥3 months AND age at onset <45 years
    
    If entry criterion met:
    - Imaging arm: Sacroiliitis on imaging + ≥1 SpA feature
    - Clinical arm: HLA-B27 positive + ≥2 SpA features
    
    SpA features include inflammatory back pain, arthritis, enthesitis, uveitis, 
    dactylitis, psoriasis, inflammatory bowel disease, good response to NSAIDs, 
    family history, and elevated CRP.
    
    Args:
        request: Parameters needed for ASAS classification
        
    Returns:
        AsasAxialSpaCriteriaResponse: Classification result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asas_axial_spa_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASAS Criteria for Axial Spondyloarthritis",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsasAxialSpaCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASAS Criteria for Axial Spondyloarthritis",
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

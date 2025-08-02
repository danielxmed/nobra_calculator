"""
Swede Score Router

Endpoint for calculating Swede Score colposcopy assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.swede_score import (
    SwedeScoreRequest,
    SwedeScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/swede_score",
    response_model=SwedeScoreResponse,
    summary="Calculate Swede Score",
    description="Calculates the Swede Score for colposcopic assessment of cervical lesions. "
                "This standardized scoring system evaluates five key characteristics "
                "(acetowhite uptake, margins/surface, vessels, lesion size, and iodine staining) "
                "to predict the likelihood of high-grade cervical intraepithelial neoplasia (CIN 2+). "
                "The score ranges from 0-10 points and guides clinical decision-making regarding "
                "surveillance, biopsy, or immediate treatment using 'see and treat' protocols.",
    response_description="The calculated Swede Score with risk stratification and clinical management recommendations",
    operation_id="swede_score"
)
async def calculate_swede_score(request: SwedeScoreRequest):
    """
    Calculates Swede Score for colposcopic assessment
    
    The Swede Score is a validated clinical prediction tool that standardizes 
    colposcopic evaluation of cervical lesions to predict high-grade disease. 
    It helps reduce inter-observer variability and guides appropriate 
    management decisions in cervical cancer screening programs.
    
    Args:
        request: Parameters needed for calculation including aceto uptake,
                margins/surface characteristics, vascular pattern, lesion size,
                and iodine staining pattern
        
    Returns:
        SwedeScoreResponse: Score with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("swede_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Swede Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return SwedeScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Swede Score",
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
"""
ATLAS Score Router

Endpoint for calculating ATLAS Score for Clostridium Difficile Infection.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.atlas_score import (
    AtlasScoreRequest,
    AtlasScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/atlas_score",
    response_model=AtlasScoreResponse,
    summary="Calculate ATLAS Score for Clostridium Difficile Infection",
    description="Predicts response to therapy in C. diff patients",
    response_description="The calculated atlas score with interpretation",
    operation_id="atlas_score"
)
async def calculate_atlas_score(request: AtlasScoreRequest):
    """
    Calculates ATLAS Score for Clostridium Difficile Infection
    
    Predicts response to vancomycin therapy in patients with C. difficile infection (CDI).
    The ATLAS score helps identify patients at high risk for treatment failure who may 
    benefit from alternative therapeutic approaches.
    
    The score uses 5 clinical parameters:
    - Age ≥65 years: +1 point
    - Treatment with Systemic Antibiotics: +2 points (highest weight)
    - Leukocytosis >15,000/μL: +1 point
    - Albumin <2.5 g/dL: +1 point
    - Serum Creatinine >1.5× baseline: +1 point
    
    Score Interpretation:
    - 0-2 points: Low Risk (Good response to vancomycin therapy expected)
    - 3-6 points: High Risk (Poor response to vancomycin therapy expected)
    
    High-risk patients may benefit from alternative therapies such as fidaxomicin 
    or fecal microbiota transplantation rather than standard vancomycin treatment.
    
    Args:
        request: Parameters including age, antibiotic use, lab values
        
    Returns:
        AtlasScoreResponse: Score with risk level and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("atlas_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ATLAS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AtlasScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ATLAS Score",
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

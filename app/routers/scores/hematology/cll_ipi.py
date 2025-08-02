"""
International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI) Router

Endpoint for calculating CLL-IPI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.cll_ipi import (
    CllIpiRequest,
    CllIpiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cll_ipi",
    response_model=CllIpiResponse,
    summary="Calculate International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI)",
    description="Calculates the International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI) to stratify "
                "CLL patients into four risk categories based on five independent prognostic factors. This validated "
                "prognostic model combines genetic (TP53 status, IGHV mutational status), biochemical (β2-microglobulin), "
                "and clinical parameters (age, clinical stage) to predict overall survival. The CLL-IPI discriminates four "
                "risk groups with significantly different 5-year overall survival rates: Low Risk (0-1 points, 93.2% OS), "
                "Intermediate Risk (2-3 points, 79.3% OS), High Risk (4-6 points, 63.3% OS), and Very High Risk (7-10 points, "
                "23.3% OS). Scoring includes: TP53 abnormal (del(17p) and/or TP53 mutation, 4 points), IGHV unmutated "
                "(≥98% homology, 2 points), β2-microglobulin >3.5 mg/L (2 points), advanced clinical stage (Binet B-C or "
                "Rai I-IV, 1 point), and age >65 years (1 point). This prognostic tool enables targeted patient management, "
                "treatment intensity selection, and clinical trial stratification. It should be used for risk stratification "
                "and patient counseling, while treatment decisions should be based on iwCLL criteria. The CLL-IPI remains "
                "prognostically relevant in the era of targeted therapies and has been validated across multiple geographic "
                "regions and treatment eras.",
    response_description="The calculated CLL-IPI score with risk stratification and survival predictions",
    operation_id="cll_ipi"
)
async def calculate_cll_ipi(request: CllIpiRequest):
    """
    Calculates CLL-IPI for risk stratification in chronic lymphocytic leukemia
    
    Predicts overall survival using five independent prognostic factors to stratify 
    CLL patients into four risk categories for personalized treatment planning.
    
    Args:
        request: Clinical and laboratory parameters for CLL-IPI calculation (5 factors)
        
    Returns:
        CllIpiResponse: CLL-IPI score with risk category and survival predictions
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cll_ipi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CLL-IPI",
                    "details": {"parameters": parameters}
                }
            )
        
        return CllIpiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CLL-IPI",
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
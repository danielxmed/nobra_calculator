"""
MSKCC/Motzer Score Router

Endpoint for calculating MSKCC/Motzer Score for Metastatic RCC.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.mskcc_motzer_score import (
    MskccMotzerScoreRequest,
    MskccMotzerScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mskcc_motzer_score",
    response_model=MskccMotzerScoreResponse,
    summary="Calculate MSKCC/Motzer Score for Metastatic RCC",
    description="Calculates the Memorial Sloan-Kettering Cancer Center (MSKCC/Motzer) Score "
                "to predict survival in metastatic renal cell carcinoma. This prognostic model "
                "uses five independent risk factors: time from diagnosis to treatment <1 year, "
                "hemoglobin below normal (Men <13.5, Women <12.0 g/dL), corrected calcium "
                ">10 mg/dL, LDH >1.5x upper limit of normal, and Karnofsky Performance Status "
                "<80%. The score stratifies patients into three risk groups: Good (0 factors, "
                "median survival 20 months), Intermediate (1-2 factors, median survival 10 months), "
                "and High (≥3 factors, median survival 4 months). Originally developed for patients "
                "treated with interferon-alpha, it remains valuable for prognostication and clinical "
                "trial stratification. Note: The IMDC model is now preferred for patients receiving "
                "targeted therapy. Always use corrected calcium and baseline values before treatment.",
    response_description="The calculated MSKCC score with risk stratification and survival prognosis",
    operation_id="mskcc_motzer_score"
)
async def calculate_mskcc_motzer_score(request: MskccMotzerScoreRequest):
    """
    Calculates MSKCC/Motzer Score for Metastatic RCC
    
    This foundational prognostic tool helps stratify metastatic RCC patients by survival
    risk using readily available clinical and laboratory parameters.
    
    Args:
        request: Clinical and laboratory parameters for score calculation
        
    Returns:
        MskccMotzerScoreResponse: Risk category and survival prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mskcc_motzer_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MSKCC/Motzer Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MskccMotzerScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MSKCC/Motzer Score",
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
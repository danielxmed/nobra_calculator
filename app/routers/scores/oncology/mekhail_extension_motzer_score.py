"""
Mekhail Extension of the Motzer Score Router

Endpoint for calculating Mekhail Extension of the Motzer Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.mekhail_extension_motzer_score import (
    MekhailExtensionMotzerScoreRequest,
    MekhailExtensionMotzerScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mekhail_extension_motzer_score",
    response_model=MekhailExtensionMotzerScoreResponse,
    summary="Calculate Mekhail Extension of the Motzer Score",
    description="Calculates the Mekhail Extension of the Motzer Score for metastatic renal "
                "cell carcinoma (mRCC) survival prediction. This extended version of the "
                "original MSKCC/Motzer score incorporates 6 risk factors: elevated LDH "
                "(>1.5x ULN), low hemoglobin (<LLN), high corrected calcium (>10 mg/dL), "
                "time from diagnosis to treatment <1 year, prior radiotherapy, and ≥2 "
                "metastatic sites. The score stratifies patients into three risk categories: "
                "Favorable (0-1 points, median survival 28 months), Intermediate (2 points, "
                "median survival 14 months), and Poor (≥3 points, median survival 5 months). "
                "While historically important, this score was developed before the era of "
                "modern targeted therapies and immunotherapy, limiting its current clinical "
                "applicability. Best used for clinical trial stratification and providing "
                "general prognostic context.",
    response_description="The calculated Mekhail score with risk stratification and survival prognosis",
    operation_id="mekhail_extension_motzer_score"
)
async def calculate_mekhail_extension_motzer_score(request: MekhailExtensionMotzerScoreRequest):
    """
    Calculates Mekhail Extension of the Motzer Score
    
    This prognostic tool helps stratify metastatic RCC patients by survival risk,
    incorporating additional factors beyond the original Motzer score for improved accuracy.
    
    Args:
        request: Clinical and laboratory parameters for score calculation
        
    Returns:
        MekhailExtensionMotzerScoreResponse: Risk category and survival prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mekhail_extension_motzer_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mekhail Extension of the Motzer Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MekhailExtensionMotzerScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mekhail Extension of the Motzer Score",
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
"""
Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score Router

Endpoint for calculating PE-SARD Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.pe_sard_score import (
    PeSardScoreRequest,
    PeSardScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/pe_sard_score",
    response_model=PeSardScoreResponse,
    summary="Calculate Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score",
    description="Estimates risk of early major bleeding in patients with acute pulmonary embolism (PE) "
                "using three simple clinical variables: syncope, anemia (Hgb <12 g/dL), and renal "
                "dysfunction (GFR <60 mL/min). This validated clinical decision tool helps identify "
                "PE patients at higher risk for bleeding complications within 30 days of diagnosis, "
                "enabling evidence-based decisions about anticoagulation management and monitoring "
                "intensity. The score stratifies patients into three risk categories: Low Risk "
                "(0 points, 0.6% bleeding incidence), Intermediate Risk (1-2.5 points, 1.5% bleeding "
                "incidence), and High Risk (>2.5 points, 2.5% bleeding incidence). Developed by "
                "Barrios et al. in 2021 and externally validated in multiple large registries "
                "(RIETE, COMMAND VTE), the PE-SARD score demonstrates superior performance compared "
                "to existing bleeding risk assessment tools in the PE setting. Low-risk patients "
                "may be suitable for standard anticoagulation with routine monitoring, while "
                "intermediate and high-risk patients may benefit from enhanced monitoring, modified "
                "anticoagulation strategies, or specialist consultation. The tool supports shared "
                "decision-making by providing objective bleeding risk estimates that can be balanced "
                "against thrombotic risk to optimize individual patient management.",
    response_description="The calculated PE-SARD score with bleeding risk category and comprehensive management recommendations",
    operation_id="pe_sard_score"
)
async def calculate_pe_sard_score(request: PeSardScoreRequest):
    """
    Calculates Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score
    
    This validated clinical tool estimates 30-day major bleeding risk in acute PE patients
    to guide anticoagulation management and monitoring decisions.
    
    Args:
        request: Clinical parameters including syncope history, anemia status (Hgb <12 g/dL),
                and renal dysfunction (GFR <60 mL/min) for PE-SARD calculation
        
    Returns:
        PeSardScoreResponse: Result with bleeding risk category and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("pe_sard_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PE-SARD Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return PeSardScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PE-SARD Score",
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
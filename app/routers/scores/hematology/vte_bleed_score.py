"""
VTE-BLEED Score Router

Endpoint for calculating VTE-BLEED Score for bleeding risk assessment on anticoagulation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.vte_bleed_score import (
    VteBleedScoreRequest,
    VteBleedScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/vte_bleed_score",
    response_model=VteBleedScoreResponse,
    summary="Calculate VTE-BLEED Score",
    description="Assesses bleeding risk on anticoagulation therapy in patients with venous thromboembolism (VTE). "
                "The VTE-BLEED Score is the most validated bleeding risk score specifically designed for VTE patients, "
                "unlike scores derived from atrial fibrillation populations (HAS-BLED, HEMORR2HAGES, ATRIA). "
                "This score enables better stratification of bleeding risk during stable anticoagulation after "
                "a first VTE episode, accounting for the different comorbidity profile of VTE patients who are "
                "typically younger and have higher prevalence of cancer versus renal dysfunction. The score uses "
                "6 clinical criteria with weighted point values: age ≥60 years (1.5 points), active cancer "
                "(2.0 points), male with uncontrolled hypertension (1.0 point), anemia (1.5 points), history "
                "of bleeding (1.5 points), and renal dysfunction (1.5 points). Scores <2 indicate low bleeding "
                "risk suitable for standard anticoagulation, while scores ≥2 indicate elevated risk requiring "
                "enhanced monitoring, potential dose adjustments, and individualized risk-benefit assessment. "
                "The score has good prediction power for major bleeding events, including intracranial and fatal "
                "bleeding, and is validated for direct oral anticoagulants and vitamin K antagonists. Clinical "
                "applications include treatment duration decisions, anticoagulant selection, monitoring frequency, "
                "and patient counseling in VTE management.",
    response_description="VTE-BLEED score with bleeding risk stratification, detailed component breakdown, and tailored clinical recommendations",
    operation_id="vte_bleed_score"
)
async def calculate_vte_bleed_score(request: VteBleedScoreRequest):
    """
    Calculates VTE-BLEED Score for bleeding risk assessment
    
    Assesses bleeding risk on anticoagulation therapy in VTE patients using 
    validated clinical criteria to guide treatment decisions and monitoring.
    
    Args:
        request: Clinical criteria including age, cancer status, hypertension, anemia, bleeding history, and renal function
        
    Returns:
        VteBleedScoreResponse: VTE-BLEED score with risk stratification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("vte_bleed_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VTE-BLEED Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return VteBleedScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VTE-BLEED Score",
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
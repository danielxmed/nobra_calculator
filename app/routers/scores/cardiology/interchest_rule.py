"""
INTERCHEST Clinical Prediction Rule Router

Endpoint for calculating INTERCHEST Clinical Prediction Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.interchest_rule import (
    InterchestRuleRequest,
    InterchestRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/interchest_rule",
    response_model=InterchestRuleResponse,
    summary="Calculate INTERCHEST Clinical Prediction Rule for Chest Pain in Primary Care",
    description="Calculates the INTERCHEST Clinical Prediction Rule for ruling out coronary artery disease (CAD) in primary care patients ≥30 years "
                "presenting with chest pain. This validated clinical prediction rule uses 6 clinical variables to identify patients with very low "
                "likelihood of chest pain due to unstable CAD. The scoring system ranges from -1 to +5 points: History of CAD (+1), Age/Gender risk "
                "Female ≥65 or Male ≥55 (+1), Effort-related pain (+1), Pressure sensation (+1), Physician suspected serious condition (+1), and "
                "Pain reproducible by palpation (-1 - protective). Scores ≤1 indicate low CAD risk (2.1% probability, 98% NPV) allowing safe "
                "discharge without urgent evaluation, while scores ≥2 indicate higher risk (43% probability) requiring further workup with ECG, "
                "biomarkers, and possible cardiology consultation. This tool is specifically designed for primary care settings and should NOT be "
                "used in emergency departments, for positive CAD diagnosis, or in patients with obvious cardiac findings.",
    response_description="The calculated INTERCHEST score with CAD risk stratification and primary care management recommendations",
    operation_id="interchest_rule"
)
async def calculate_interchest_rule(request: InterchestRuleRequest):
    """
    Calculates INTERCHEST Clinical Prediction Rule for CAD screening in primary care
    
    Rules out coronary artery disease in primary care patients with chest pain using 
    validated clinical variables. Helps identify low-risk patients safe for discharge.
    
    Args:
        request: Clinical parameters for INTERCHEST rule calculation (6 variables)
        
    Returns:
        InterchestRuleResponse: INTERCHEST score with CAD risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("interchest_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating INTERCHEST Clinical Prediction Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return InterchestRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for INTERCHEST Clinical Prediction Rule",
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
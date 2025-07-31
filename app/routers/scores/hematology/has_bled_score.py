"""
HAS-BLED Score for Major Bleeding Risk Router

Endpoint for calculating HAS-BLED Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.has_bled_score import (
    HasBledScoreRequest,
    HasBledScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/has_bled_score",
    response_model=HasBledScoreResponse,
    summary="Calculate HAS-BLED Score for Major Bleeding Risk",
    description="Calculates the HAS-BLED Score to estimate 1-year risk of major bleeding in patients "
                "with atrial fibrillation on anticoagulation therapy. The score uses 9 clinical factors: "
                "Hypertension (uncontrolled >160 mmHg), Abnormal renal/liver function (1 point each), "
                "Stroke history, Bleeding history or predisposition, Labile INR (TTR <60%), Elderly (>65), "
                "and Drugs/Alcohol (1 point each). Scores range from 0-9, with ≥3 indicating high bleeding "
                "risk (5.8% to >10% annual risk). Major bleeding is defined as intracranial hemorrhage, "
                "hospitalization for bleeding, hemoglobin drop >2 g/L, or transfusion. Use alongside "
                "CHA2DS2-VASc score to balance stroke and bleeding risks in anticoagulation decisions.",
    response_description="The calculated HAS-BLED score with bleeding risk stratification and management recommendations",
    operation_id="has_bled_score"
)
async def calculate_has_bled_score(request: HasBledScoreRequest):
    """
    Calculates HAS-BLED Score for Major Bleeding Risk
    
    The HAS-BLED score helps assess bleeding risk in anticoagulated patients with
    atrial fibrillation, identifying modifiable risk factors and guiding monitoring.
    
    Args:
        request: Parameters needed for HAS-BLED calculation
        
    Returns:
        HasBledScoreResponse: Result with bleeding risk assessment and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("has_bled_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HAS-BLED Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HasBledScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HAS-BLED calculation",
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
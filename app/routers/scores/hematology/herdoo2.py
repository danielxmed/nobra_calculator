"""
HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE Router

Endpoint for calculating HERDOO2 score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.herdoo2 import (
    Herdoo2Request,
    Herdoo2Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/herdoo2",
    response_model=Herdoo2Response,
    summary="Calculate HERDOO2 Rule",
    description="Calculates the HERDOO2 rule for identifying low-risk women who can safely "
                "discontinue anticoagulation after treatment for unprovoked venous thromboembolism. "
                "This validated clinical decision tool is specifically designed for women with first "
                "unprovoked VTE who have completed 5-12 months of anticoagulation therapy. The rule "
                "uses four clinical variables (post-thrombotic signs, D-dimer level, BMI, and age) "
                "to stratify patients into low risk (0-1 points, 3.0% annual recurrence) or not low "
                "risk (2-4 points, 7.4% annual recurrence) categories. Women scoring 0-1 points can "
                "safely discontinue anticoagulation with close follow-up.",
    response_description="The calculated HERDOO2 score with risk stratification and anticoagulation recommendations",
    operation_id="herdoo2"
)
async def calculate_herdoo2(request: Herdoo2Request):
    """
    Calculates HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE
    
    This rule helps identify women at low risk of VTE recurrence who can safely
    stop anticoagulation after completing initial treatment for unprovoked VTE.
    
    Args:
        request: Clinical parameters for HERDOO2 calculation
        
    Returns:
        Herdoo2Response: Score with risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("herdoo2", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HERDOO2 score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Herdoo2Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HERDOO2 calculation",
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
                "message": "Internal error in HERDOO2 calculation",
                "details": {"error": str(e)}
            }
        )